import ast
import inspect
import logging
import sys
from copy import deepcopy
from functools import partial
from typing import Callable, Dict, List, Literal, Union

import astor
import requests

from fluidsdk.flow import Flow
from fluidsdk.intents import (
    AskDefiniteIntent,
    AskOpenIntent,
    ConditionIntent,
    ExpressionIntent,
    GPTGenerateIntent,
    JumpIntent,
    SayIntent,
    ScheduleJobIntent,
)
from fluidsdk.message import Message
from fluidsdk.pyrite import library, utils
from fluidsdk.pyrite.consts import ENGINE_GLOBALS, PYTHON_BUILTINS
from fluidsdk.templates import Template

sys.tracebacklimit = 0
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

statement_library = {ctx.__name__: ctx for ctx in library._exports["statement_library"]}
assignment_library = {
    ctx.__name__: ctx for ctx in library._exports["assignment_library"]
}
context_library = {ctx.__name__: ctx for ctx in library._exports["context_library"]}

BASE_URL = {
    "local": "http://localhost:8000",
    "dev": "https://engine.dev.workhack.ai",
    "production": "https://engine.workhack.io",
    "staging": "https://engine.staging.workhack.ai",
    "porter": "https://engine.porter.workhack.ai",
}

NOOP = ExpressionIntent(expression="`null`", answer_field="_")


class FlowBuilder:
    """
    Pyrite flow builder.

    :param flow_id: ID used to indentify the flow in the engine.
    :param flow_description: Purpose of the flow.
    :param data: Global data to be shared by all conversations. Can be accessed in the `flow_data` variable.
    :param invitation_messages: Messages sent when the bot messages the user first.
    :param referred_conversation_messages: Messages sent when the user messages the bot first.
    :param end_conversation_messages: Messages sent right before closing the conversation.
    :param username: Username to log into the engine. If not passed, the Builder will be in offline mode..
    :param password: Password to log into the engine. If not passed, the Builder will be in offline mode..
    """

    def __init__(
        self,
        flow_id: str,
        flow_description: str,
        *,
        data: Dict = None,
        invitation_messages: List[Message] = None,
        referred_conversation_messages: List[Message] = None,
        end_conversation_messages: List[Message] = None,
        username: str = None,
        password: str = None,
        environment: Literal["production", "dev", "staging"] = "production",
    ):
        self.flow = Flow(
            flow_id=flow_id,
            flow_description=flow_description,
            data=data or {},
            # Do not include reminders yet. The dashboard sets reminders which should
            # not be overwritten by the pyrite.
            # reminders={},
            filters={},
            step={},
            invitation_messages=invitation_messages or [],
            end_conversation_messages=end_conversation_messages or [],
            referred_conversation_messages=referred_conversation_messages or [],
        )

        self.environment = environment
        if username is not None:
            response = requests.post(
                f"{BASE_URL[self.environment]}/token",
                data={"username": username, "password": password},
            )
            if not response.ok:
                raise RuntimeError(
                    "Failed to Authenticate to the engine. Are the provided credentials valid?"
                )
            token = response.json()["access_token"]
            response = requests.get(
                f"{BASE_URL[self.environment]}/orgs",
                headers={"Authorization": f"Bearer {token}"},
            )
            if not response.ok:
                raise RuntimeError(
                    "Failed to Authenticate to the engine. Is the provided token valid?"
                )
            self.token = token
            user = response.json()["user"]
            logging.info(f"Logged in as {user['sub']} of org {user['workhack/org']}")
        else:
            self.token = None
            print(f"Builder for {flow_id} is in Offline Mode.")

        self.subroutines = {}
        self.templates = {}
        self.hook_context = self.Context(
            prefix="hooks",
            idx=1,
            flow_steps={},
            source_lines=None,
            filename=None,
            builder=self,
            global_names=set(ENGINE_GLOBALS),
        )
        utils.insert_then_increment(
            self.hook_context,
            self.hook_context.idx,
            ConditionIntent(
                condition="py>current_message.get('type') != 'scheduled-job'",
                if_=self.hook_context.prefix + "-" + str(self.hook_context.idx+1),
                else_=""
            )
        )
        utils.insert_then_increment(
            self.hook_context,
            self.hook_context.idx,
            ExpressionIntent(expression="py>time()", answer_field="state"),
        )
        self.jobs_context = self.Context(
            prefix="jobs",
            idx=1,
            flow_steps={},
            source_lines=None,
            filename=None,
            builder=self,
            global_names=set(ENGINE_GLOBALS),
        )
        self.schedule_jobs_times = {}

    class Context:
        def __init__(
            self,
            prefix,
            idx,
            flow_steps,
            source_lines,
            filename,
            *,
            global_names=None,
            local_names=None,
            builder=None,
        ):
            self.prefix = prefix
            self.idx = idx
            self.flow_steps = flow_steps
            self.source_lines = source_lines
            self.filename = filename
            self.global_names = global_names or set()
            self.local_names = local_names or set()
            self.step_contexts = {}
            self.builder = builder

    def subroutine(self, f: Callable) -> Callable:
        """
        Include a subroutine to be used in a flow.
        Used as a decorator like this:

        .. code-block:: python

            @flow.subroutine
            def start():
                ...

        :return: Returns the same function

        """
        self.subroutines[f.__name__] = f
        return f

    def scheduled(self, inactive_for: int) -> Callable:
        """
        Include a subroutine, and schedule to be run after the user
        has been inactive for an amount of time
        Used as a decorator like this:

        .. code-block:: python

            @flow.scheduled(inactive_for=300)
            def reminder():
                ...

        `inactive_for` is measured in seconds

        :return: Returns the same function

        """

        def wraps(f: Callable):
            self.subroutines[f.__name__] = f
            self.schedule_jobs_times[f.__name__] = "py>time()+" + str(inactive_for)
            condition = (
                "py>current_message.get('type') == 'scheduled-job' and current_message.get('data', {}).get('state') == state and current_message.get('data', {}).get('kind') == '"
                + f.__name__
                + "'"
            )
            utils.insert_then_increment(
                self.jobs_context,
                self.jobs_context.idx,
                ConditionIntent(
                    condition=condition,
                    if_=self.jobs_context.prefix + "-" + str(self.jobs_context.idx + 1),
                    else_=self.jobs_context.prefix
                    + "-"
                    + str(self.jobs_context.idx + 3),
                ),
            )
            self.insert_subroutine_call(self.jobs_context, f.__name__)
            utils.insert_then_increment(
                self.jobs_context,
                self.jobs_context.idx,
                ExpressionIntent(expression="null", answer_field="null"),
            )
            return f

        return wraps

    def hook(self, f: Callable) -> Callable:
        """
        Include a subroutine to be run for every message.
        Should never wait for user input.
        Used as a decorator like this:

        .. code-block:: python

            @flow.hook
            def start():
                ...

        :return: Returns the same function

        """
        self.subroutines[f.__name__] = f
        self.insert_subroutine_call(self.hook_context, f.__name__)
        return f

    def include_template(self, t: Union[str, Template]):
        """
        Include a template to be used in a flow.
        Template is not pushed until :py:mod:`Flow.push_templates` or :py:mod:`Flow.build_and_push` is called.
        """
        if isinstance(t, str):
            self.templates[t] = None
        elif isinstance(t, Template):
            self.templates[t.template_id] = t
        else:
            raise TypeError("This is not a Fluid Template.")

    @staticmethod
    def insert_subroutine_call(context, entrypoint):
        utils.insert_then_increment(
            context,
            context.idx,
            ExpressionIntent(
                expression=f"[call_stack, '{context.prefix}-{context.idx+1}'] | []",
                answer_field="call_stack",
                next_=f"{entrypoint}",
            ),
        )
        utils.insert_then_increment(
            context,
            context.idx,
            ExpressionIntent(expression="`null`", answer_field="return_value"),
        )

    def build_body(self, body, prefix, old_context) -> dict:
        context = deepcopy(old_context)
        context.step_contexts = old_context.step_contexts
        context.builder = old_context.builder
        context.flow_steps = {}
        context.prefix = prefix

        raise_syntax_error = partial(
            utils.raise_syntax_error, context.source_lines, context.filename
        )
        raise_type_error = partial(
            utils.raise_type_error, context.source_lines, context.filename
        )

        for node in body:
            # Line is an expression
            if isinstance(node, ast.Expr):
                if isinstance(node.value, ast.Call):
                    call_node = node.value
                    if isinstance(call_node.func, ast.Attribute):
                        context_name = call_node.func.value.id
                        if context_name not in context.step_contexts:
                            raise_syntax_error(
                                call_node.func.value, "Undefined Context."
                            )
                        ctx = context.step_contexts[context_name]
                        if not isinstance(call_node.func.attr, str):
                            raise_syntax_error(call_node.func, "Attribute error.")
                        method = call_node.func.attr
                        if method not in ctx.exports["statement_library"]:
                            raise_syntax_error(
                                call_node.func,
                                "Attribute error. "
                                + method
                                + " does not exist in this context.",
                            )
                        utils.get_builder(getattr(ctx, method))(context, call_node)
                    elif call_node.func.id in statement_library:
                        utils.get_builder(statement_library[call_node.func.id])(
                            context, call_node
                        )
                    elif call_node.func.id in self.subroutines:
                        self.build_call_subroutine(context, call_node.func.id)
                    else:
                        raise_syntax_error(node, "Undefined subroutine.")
                else:
                    raise_syntax_error(
                        node.value,
                        "Unexpected Python Syntax. Pyrite does not support "
                        + str(type(node.value))
                        + " yet.",
                    )
            elif isinstance(node, ast.Assign):
                if len(node.targets) > 1:
                    raise_syntax_error(
                        node.targets[1],
                        "You can't assign to more than one target at a time yet.",
                    )
                if isinstance(node.targets[0], ast.Name):
                    target = node.targets[0].id
                    if target in context.global_names:
                        target_field = target
                    else:
                        target_field = "data_stack.[{py>len(data_stack)-1}]." + target
                elif isinstance(node.targets[0], ast.Tuple):
                    raise_syntax_error(
                        node.targets[0], "Assigning to tuples not supported yet"
                    )
                elif isinstance(node.targets[0], ast.Subscript):
                    target_field = ""
                    current_node = node.targets[0]
                    while True:
                        if isinstance(current_node.slice, ast.Constant):
                            target_field = (
                                "." + str(current_node.slice.value) + target_field
                            )
                        else:
                            expression = utils.build_expression(
                                current_node.slice, context.prefix, context
                            )
                            target_field = ".[{py>" + expression + "}]" + target_field
                        if isinstance(current_node.value, ast.Subscript):
                            current_node = current_node.value
                        elif isinstance(current_node.value, ast.Name):
                            target = current_node.value.id
                            if target in context.global_names:
                                target_field = target + target_field
                            else:
                                target_field = (
                                    "data_stack.[{py>len(data_stack)-1}]."
                                    + target
                                    + target_field
                                )
                            break
                else:
                    raise_syntax_error(
                        node.targets[0],
                        f"Assigning to {str(node.targets[0])} not supported yet",
                    )
                if isinstance(node.value, ast.Call):
                    call_node = node.value
                    # If the call node is a simple name. Like `subr(arg)` or `int(arg)`
                    if isinstance(call_node.func, ast.Name):
                        if call_node.func.id in self.subroutines:
                            raise_syntax_error(
                                node,
                                "Cannot assign returns values from subroutines yet.",
                            )
                        elif call_node.func.id in assignment_library:
                            # If this is a library function, call handler
                            utils.get_builder(assignment_library[call_node.func.id])(
                                context, call_node, target_field
                            )
                        elif call_node.func.id in PYTHON_BUILTINS:
                            # If node is a whitelisted python builtin, treat it as an expression
                            expression = utils.build_expression(
                                call_node, context.prefix, context
                            )
                            utils.insert_then_increment(
                                context,
                                context.idx,
                                ExpressionIntent(
                                    expression=f"py>{expression}",
                                    answer_field=target_field,
                                ),
                            )
                        else:
                            raise_syntax_error(call_node, "Undefined subroutine.")
                    # Else if the call node is an Attribute or Subscript. Like `re.test(arg)` or `xyz["func"](arg)`
                    else:
                        # Treat it as an expression
                        expression = utils.build_expression(
                            call_node, context.prefix, context
                        )
                        utils.insert_then_increment(
                            context,
                            context.idx,
                            ExpressionIntent(
                                expression=f"py>{expression}",
                                answer_field=target_field,
                            ),
                        )
                else:
                    expression = utils.build_expression(
                        node.value, context.prefix, context
                    )
                    utils.insert_then_increment(
                        context,
                        context.idx,
                        ExpressionIntent(
                            expression=f"py>{expression}", answer_field=target_field
                        ),
                    )
                context.local_names.add(target)
            elif isinstance(node, ast.Nonlocal):
                raise_syntax_error(
                    node, "Invalid keyword `nonlocal`. Did you mean `global`?"
                )
            elif isinstance(node, ast.Global):
                context.global_names.update(node.names)
            elif isinstance(node, ast.With):
                if len(node.items) < 1:
                    raise_syntax_error(
                        node,
                        "You cannot use the `with` statement without a context manager. Did you mean `with Context() as context_name:`?",
                    )
                if len(node.items) > 1:
                    raise_syntax_error(
                        node,
                        "You cannot use the `with` statement multiple context managers. Did you mean `with Context() as context_name:`?",
                    )
                context_manager_item = node.items[0]
                if isinstance(context_manager_item.context_expr, ast.Call):
                    if context_manager_item.optional_vars is None:
                        raise_syntax_error(
                            node,
                            "You must give this context a name. Did you mean `with Context() as context_name:`?",
                        )
                    if not isinstance(context_manager_item.optional_vars, ast.Name):
                        raise_syntax_error(
                            context_manager_item.optional_vars,
                            "Context name can only be a simple variable name. Did you mean `with Context() as context_name:`?",
                        )
                    context_name = context_manager_item.optional_vars.id
                    if isinstance(
                        context_manager_item.context_expr.func, ast.Attribute
                    ):
                        raise_syntax_error(
                            context_manager_item.context_expr.func,
                            'This is not a context manager. Did you mean `with Context() as context_name:`?',
                        )
                    context_function = context_library.get(
                        context_manager_item.context_expr.func.id
                    )
                    if context_function is None:
                        raise_syntax_error(
                            context_manager_item.context_expr.func,
                            'Undefined context manager. Did you mean `with Context("context_name"):`?',
                        )
                    ctx = utils.get_builder(context_function)

                    with ctx(
                        context_manager_item.context_expr,
                        node.body,
                        context,
                        context_name,
                    ):
                        ctx.body_context = self.build_body(
                            node.body,
                            f"{context.prefix}-{context.idx}-context-{context_name}",
                            ctx.body_context,
                        )
                elif isinstance(context_manager_item.context_expr, ast.Name):
                    context_name = context_manager_item.context_expr.id
                    if context_name not in context.step_contexts:
                        raise_syntax_error(
                            context_manager_item.context_expr,
                            f"Undefined context {context_name}.",
                        )
                    with context.step_contexts[context_name].with_body(
                        node.body, context
                    ):
                        ctx.body_context = self.build_body(
                            node.body,
                            f"{context.prefix}-{context.idx}-context-{context_name}",
                            ctx.body_context,
                        )
                else:
                    raise_syntax_error(
                        context_manager_item.context_expr,
                        'This is not a context manager. Did you mean `with Context("context_name"):`?',
                    )
            elif isinstance(node, ast.If):
                self.build_if_statement(node, 0, context)
            elif isinstance(node, ast.While):
                self.build_while_statement(node, context)
            elif isinstance(node, ast.Return):
                self.build_return(node, context)
            else:
                raise_syntax_error(
                    node,
                    "Unexpected Python Syntax. Pyrite does not support "
                    + str(type(node))
                    + " yet.",
                )
            # print(ast.dump(node, indent=4))
        return context

    def build_if_statement(
        self, node: ast.If, if_else_idx, old_context, done_prefix=None
    ):
        context = deepcopy(old_context)
        context.step_contexts = old_context.step_contexts
        context.builder = old_context.builder
        context.flow_steps = {}
        add_done = False
        if done_prefix is None:
            add_done = True
            done_prefix = old_context.prefix + "-" + str(old_context.idx) + "-if-done"

        expression = utils.build_expression(node.test, context.prefix, context)
        context.idx = if_else_idx
        context.prefix = old_context.prefix + "-" + str(old_context.idx) + "-if"

        utils.insert_then_increment(
            context,
            context.idx,
            ConditionIntent(
                condition="py>" + expression,
                if_=context.prefix + "-" + str(if_else_idx) + "-body-0",
                else_=old_context.prefix
                + "-"
                + str(old_context.idx)
                + "-if-"
                + str(if_else_idx + 1)
                if len(node.orelse) > 0
                else done_prefix,
            ),
        )
        old_context.flow_steps.update(context.flow_steps)

        context.idx = 0

        body_context = self.build_body(
            node.body,
            context.prefix + "-" + str(if_else_idx) + "-body",
            context,
        )
        utils.insert_then_increment(
            body_context,
            body_context.idx,
            ExpressionIntent(expression="null", answer_field="null", next_=done_prefix),
        )
        old_context.flow_steps.update(body_context.flow_steps)

        if len(node.orelse) == 0:
            pass
        elif len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
            else_node = node.orelse[0]
            self.build_if_statement(
                else_node, if_else_idx + 1, old_context, done_prefix
            )
        else:
            else_node = ast.If(ast.Constant(True), node.orelse, [])
            self.build_if_statement(
                else_node, if_else_idx + 1, old_context, done_prefix
            )

        if add_done:
            context.flow_steps = {}
            context.prefix = done_prefix
            utils.insert(
                context, None, ExpressionIntent(expression="null", answer_field="null")
            )
            old_context.flow_steps.update(context.flow_steps)

        old_context.idx += 1

    def build_while_statement(self, node: ast.While, old_context):
        context = deepcopy(old_context)
        context.step_contexts = old_context.step_contexts
        context.builder = old_context.builder
        context.flow_steps = {}
        done_prefix = old_context.prefix + "-" + str(old_context.idx) + "-while-done"

        expression = utils.build_expression(node.test, context.prefix, context)
        context.prefix = old_context.prefix + "-" + str(old_context.idx) + "-while"

        utils.insert(
            context,
            None,
            ConditionIntent(
                condition="py>" + expression,
                if_=old_context.prefix + "-" + str(old_context.idx) + "-while-0",
                else_=done_prefix,
            ),
        )

        context.idx = 0
        utils.insert_then_increment(
            context,
            context.idx,
            ExpressionIntent(expression="null", answer_field="null"),
        )
        old_context.flow_steps.update(context.flow_steps)

        body_context = self.build_body(
            node.body,
            context.prefix,
            context,
        )
        utils.insert_then_increment(
            body_context,
            body_context.idx,
            ExpressionIntent(
                expression="null",
                answer_field="null",
                next_=old_context.prefix + "-" + str(old_context.idx) + "-while",
            ),
        )
        old_context.flow_steps.update(body_context.flow_steps)

        context.flow_steps = {}
        context.prefix = done_prefix
        utils.insert(
            context, None, ExpressionIntent(expression="null", answer_field="null")
        )
        old_context.flow_steps.update(context.flow_steps)

        old_context.idx += 1

    def build_function(self, f) -> dict:
        filename = inspect.getmodule(f).__file__
        source_lines, line_count = inspect.getsourcelines(f)
        f_ast_body = ast.parse(inspect.getsource(f)).body
        if len(f_ast_body) != 1:
            print(
                "Subroutine invalid. Only pass functions to FlowBuilder.subroutine.",
                file=sys.stderr,
            )

        func_def: ast.FunctionDef = f_ast_body[0]
        line_offset = f.__code__.co_firstlineno - 1

        class FixLineNos(ast.NodeTransformer):
            parent = None

            def visit(self, node):
                if hasattr(node, "lineno") and hasattr(node, "end_lineno"):
                    node.sourcelineno = node.lineno
                    node.lineno += line_offset
                    node.end_lineno += line_offset
                self.generic_visit(node)
                return node

        func_def = FixLineNos().visit(func_def)

        raise_syntax_error = partial(utils.raise_syntax_error, source_lines, filename)
        raise_type_error = partial(utils.raise_type_error, source_lines, filename)

        # Check if the subroutine takes any arguments. If so, raise error.
        if func_def.args.posonlyargs:
            raise_syntax_error(
                func_def.args.posonlyargs[0],
                "Pyrite subroutines do not take any positional only arguments.",
            )
        if func_def.args.kwonlyargs:
            raise_syntax_error(
                func_def.args.kwonlyargs[0],
                "Pyrite subroutines do not take any keyword only arguments.",
            )
        if func_def.args.args:
            raise_syntax_error(
                func_def.args.args[0],
                "Pyrite subroutines do not take any arguments.",
            )
        if func_def.args.vararg:
            raise_syntax_error(
                func_def.args.vararg,
                "Pyrite subroutines do not take any variable arguments.",
            )
        if func_def.args.kwarg:
            raise_syntax_error(
                func_def.args.kwarg,
                "Pyrite subroutines do not take any variable keyword arguments.",
            )

        context = self.Context(
            prefix=func_def.name,
            idx=1,
            flow_steps={
                func_def.name: ExpressionIntent(
                    expression="`true`", answer_field="init"
                )
            },
            source_lines=source_lines,
            filename=filename,
            builder=self,
            global_names=set(ENGINE_GLOBALS),
        )

        # Push empty dict to the data stack
        utils.insert_then_increment(
            context,
            context.idx,
            ExpressionIntent(
                expression="[data_stack, `{}`] | []",
                answer_field="data_stack",
            ),
        )

        ctx = utils.get_builder(library.Context)

        with ctx(
            None,
            func_def.body,
            context,
            func_def.name,
        ):
            ctx.body_context.idx = context.idx
            ctx.body_context = self.build_body(
                func_def.body,
                func_def.name,
                ctx.body_context,
            )

        # func_context = self.build_body(func_def.body, , context)
        context.idx = ctx.body_context.idx
        context.flow_steps.update(ctx.body_context.flow_steps)

        self.build_return(None, context)

        return context.flow_steps

    def build_return(self, node, context):
        raise_syntax_error = partial(
            utils.raise_syntax_error, context.source_lines, context.filename
        )

        if node is not None:
            if node.value is not None:
                raise_syntax_error(
                    node.value,
                    "Pyrite doesn't support returning value yet. Use an null return: `return`.",
                )

        # Pop the top of the data stack
        utils.insert_then_increment(
            context,
            context.idx,
            ExpressionIntent(
                expression="data_stack[:-1]",
                answer_field="data_stack",
            ),
        )
        # Get the return step from the call_stack
        utils.insert_then_increment(
            context,
            context.idx,
            ExpressionIntent(
                expression="call_stack[-1]",
                answer_field="return_step",
            ),
        )
        # Pop the top value from the call_stack and go to return_step
        utils.insert_then_increment(
            context,
            context.idx,
            ExpressionIntent(
                expression="call_stack[:-1]",
                answer_field="call_stack",
                next_="[{return_step || `END`}]",
            ),
        )

    def build(
        self,
    ) -> Dict[
        str, Union[SayIntent, AskDefiniteIntent, AskOpenIntent, GPTGenerateIntent]
    ]:
        """
        Build the flow by calling build_function on each subroutine.

        :return: A dictionary of steps that can be fed to the engine
        """
        subroutine_steps = {}
        # Update flow dictionary for each subroutines.
        for k, v in self.subroutines.items():
            subroutine_steps.update(self.build_function(v))

        flow_dict = {
            "entrypoint": NOOP,
        }
        flow_dict.update(self.jobs_context.flow_steps)
        # Insert the hooks preamble

        for job_name, time in self.schedule_jobs_times.items():
            utils.insert_then_increment(
                self.hook_context,
                self.hook_context.idx,
                ScheduleJobIntent(
                    trigger_time=time, data={"state": "!py>state", "kind": job_name}
                ),
            )
            
        self.hook_context.flow_steps[self.hook_context.prefix + "-1"].else_ = self.hook_context.prefix + "-" + str(self.hook_context.idx)
        
        base_idx = self.hook_context.idx
        
        utils.insert_then_increment(
            self.hook_context,
            self.hook_context.idx,
            ConditionIntent(
                condition="py>current_message.get('type') == 'scheduled-job'",
                if_=f"{self.hook_context.prefix}-{base_idx+1}",
                else_=f"{self.hook_context.prefix}-{base_idx+2}",
            ),
        )
        utils.insert_then_increment(
            self.hook_context,
            self.hook_context.idx,
            JumpIntent(
                next_step="{previous_step}",
                next_state="{previous_state}",
                stop_processing=True,
            ),
        )
        utils.insert_then_increment(
            self.hook_context,
            self.hook_context.idx,
            JumpIntent(
                next_step="{previous_step}",
                next_state="{previous_state}",
                stop_processing=False,
            ),
        )
        flow_dict.update(self.hook_context.flow_steps)
        flow_dict.update(subroutine_steps)
        self.flow.steps = flow_dict
        return self.flow

    def push_templates(self):
        """
        Push templates to engine. Access token is required.
        """
        assert self.token is not None, "Flow builder is in offline mode"
        for template_id, template in self.templates.items():
            if template is None:
                continue
            logging.info(f"Updating template {template_id}")
            response = requests.put(
                f"{BASE_URL[self.environment]}/intent_templates/{template_id}",
                headers={"Authorization": f"Bearer {self.token}"},
                json=template.dict(),
            )
            if not response.ok:
                raise RuntimeError(f"Failed to update template {template_id}")

    def push_flow(self):
        """
        Push flow to engine. Access token is required.
        """
        assert self.token is not None, "Flow builder is in offline mode"
        logging.info(f"Updating flow {self.flow.flow_id}")
        response = requests.put(
            f"{BASE_URL[self.environment]}/flows/{self.flow.flow_id}",
            headers={"Authorization": f"Bearer {self.token}"},
            json=self.flow.dict(),
        )
        if not response.ok:
            raise RuntimeError(
                f"Failed to update flow {self.flow.flow_id}: " + str(response.json())
            )
        logging.info(
            f"Updated flow {self.flow.flow_id} to version {response.json()['version']}"
        )

    def build_and_push(self):
        """
        Build and push the flow, and templates to engine. Access token is required.
        """

        assert self.token is not None, "Flow builder is in offline mode"
        self.build()
        self.push_templates()
        self.push_flow()
