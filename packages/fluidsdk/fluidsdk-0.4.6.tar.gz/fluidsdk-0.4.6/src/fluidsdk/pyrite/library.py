import ast
import inspect
from copy import deepcopy
from functools import partial
from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field
from fluidsdk.conversational_modules import OpenAIGPTConfig

from fluidsdk.intents import (
    AskDefiniteConfig,
    AskDefiniteIntent,
    AskOpenIntent,
    ConditionIntent,
    ExpressionIntent,
    GPTGenerateIntent,
    HTTPBody,
    HTTPRequestConfig,
    HTTPRequestIntent,
    JumpIntent,
    SayIntent,
)
from fluidsdk.message import Message
from fluidsdk.pyrite import utils
from fluidsdk.pyrite.consts import ASK_AND_ACK_PRE_PROMPT
from fluidsdk.pyrite.message import parse_message, parse_messages
from fluidsdk.status_webhook import StatusIntentData
from fluidsdk.templates import GPTGenerateTemplate


def say(*messages: Message) -> None:
    """
    Say a list of messages.

    :param messages: One or more messages to say.
    """

    def builder(context, node):
        # Raises an error if the keyword arguments are present.
        if node.keywords:
            utils.raise_type_error(
                context.source_lines,
                context.filename,
                node.keywords,
                "`say` does not take any keyword arguments.",
            )

        utils.insert_then_increment(
            context,
            context.idx,
            SayIntent(text=list(parse_messages(context, node.args))),
        )

    return builder


def ask(
    *messages: Message,
    validation_regex: str = None,
    list_only=False,
    messages_on_validation_fail: Message | list[Message] = None,
) -> str:
    """
    Send a list of messages, and return the user's response.

    :param messages: One or more messages to say.

    :return: The user's response
    """

    def builder(context, node, target_field):
        raise_syntax_error = partial(
            utils.raise_syntax_error, context.source_lines, context.filename
        )

        raise_type_error = partial(
            utils.raise_type_error, context.source_lines, context.filename
        )

        signature = inspect.signature(ask)
        args = utils.test_signature(
            signature,
            node.args,
            node.keywords,
            partial(raise_type_error, node),
        ).arguments

        list_only = utils.assert_constant_type(
            args["list_only"],
            bool,
            raise_type_error,
            "list_only must be of type bool.",
        )
        if args["validation_regex"] is None:
            validation_regex = None
        else:
            validation_regex = "!py>" + utils.build_expression(
                args["validation_regex"], context.prefix, context
            )

        if args["messages_on_validation_fail"] is None:
            messages_on_validation_fail = [
                "Hmmm... Can you send it in the correct format?"
            ]
        elif isinstance(args["messages_on_validation_fail"], ast.List):
            messages_on_validation_fail = list(
                parse_messages(context, args["messages_on_validation_fail"].elts)
            )
        else:
            messages_on_validation_fail = [
                parse_message(context, args["messages_on_validation_fail"])
            ]

        utils.insert_then_increment(
            context,
            context.idx,
            AskDefiniteIntent(
                question=list(parse_messages(context, args["messages"])),
                config=AskDefiniteConfig(
                    re=validation_regex,
                    match_not_found_message=messages_on_validation_fail,
                    not_in_list_message=messages_on_validation_fail,
                ),
                list_only=list_only,
                answer_field=target_field,
            ),
        )

    return builder


class Context:
    def __init__(self):
        """
        Flow Step Context Manager.
        """
        pass

    def __call__(self, context_manager, body, context, context_name):
        self.context_manager = context_manager
        self.body = body
        self.context = context
        self.context.step_contexts[context_name] = self
        self.steps = []
        self.active = False
        return self

    def with_body(self, body, context):
        self.body = body
        self.context = context
        return self

    def __enter__(self) -> "Context":
        self.active = True
        body_context = deepcopy(self.context)
        body_context.builder = self.context.builder
        body_context.step_contexts = self.context.step_contexts
        body_context.idx = 1
        self.body_context = body_context
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.active = False

        self.context.idx += 1

        self.context
        self.context.global_names.update(self.body_context.global_names)
        self.context.local_names.update(self.body_context.local_names)
        self.context.step_contexts.update(self.body_context.step_contexts)

        self.context.flow_steps.update(self.body_context.flow_steps)

    def add_step(self, step, intent):
        if self.active:
            self.steps.append(step)

    def acknowledge(self):
        def builder(context, node):
            target_field = "acknowledgement-" + context.prefix + "-" + str(context.idx)
            utils.insert_then_increment(
                context,
                context.idx,
                GPTGenerateIntent(
                    template=GPTGenerateTemplate(
                        template_id="pyrite_acknowledge",
                        re="([\s\S]*)Person B:([\s\S]*)",
                        results=["reasoning", "acknowledgement"],
                        default_on_failure={
                            "reasoning": "I didn't understand :/",
                            "acknowledgement": utils.one_of(
                                [
                                    "Oo, Understood!",
                                    "That’s quite something really.",
                                    "Got it",
                                ]
                            ),
                        },
                        pre_prompt=ASK_AND_ACK_PRE_PROMPT,
                        user_prefix="Person A:",
                        bot_prefix="Person B:",
                        post_prompt="Explanation:",
                        gpt_config=OpenAIGPTConfig(
                            engine="text-davinci-003",
                            temperature=0.2,
                            max_tokens=120,
                            stop=["###", "Tip", "Acknowledgment", "\n\n"],
                            # logit_bias={"50256": -25},
                        ),
                    ),
                    collect=self.steps,
                    answer_field="data_stack.[{py>len(data_stack)-1}]." + target_field,
                ),
            )
            utils.insert_then_increment(
                context,
                context.idx,
                SayIntent(
                    text=[
                        '[{py>data_stack[-1]["'
                        + target_field
                        + '"]["acknowledgement"]}]'
                    ]
                ),
            )

        return builder

    @property
    def exports(self):
        return {
            "statement_library": ["acknowledge"],
        }


class AutoSkip(Context):
    def __init__(self, after: int = 300):
        super().__init__()

    def __call__(self, context_manager, body, context, context_name):
        super().__call__(context_manager, body, context, context_name)
        self.used_up = False
        return self

    def __enter__(self) -> "Context":
        if self.used_up:
            utils.raise_context_error(
                error_message="AutoSkip contexts cannot be resued.",
                filename=self.context.filename,
                source_lines=self.context.source_lines,
                node=self.context_manager
            )
        super().__enter__()
        raise_type_error = partial(
            utils.raise_type_error,
            self.context.source_lines,
            self.context.filename,
        )
        signature = inspect.signature(AutoSkip)
        args = utils.test_signature(
            signature,
            self.context_manager.args,
            self.context_manager.keywords,
            partial(raise_type_error, self.context_manager),
        ).arguments
        skip_time = utils.assert_constant_type(
            args["after"],
            int,
            raise_type_error,
            "template must be of type str.",
        )
        self.used_up = True
        self.job_name = self.body_context.prefix + "-autoskip"
        self.context.builder.schedule_jobs_times[
            self.job_name
        ] = "py>time()+" + str(skip_time)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        steps = self.steps
        # Insert a noop at the end of the context
        utils.insert_then_increment(
            self.body_context,
            self.body_context.idx,
            ExpressionIntent(expression="null", answer_field="null"),
        )

        utils.insert_then_increment(
            self.context.builder.jobs_context,
            self.context.builder.jobs_context.idx,
            ConditionIntent(
                condition=(
                    "py>current_message.get('type') == 'scheduled-job' and current_message.get('data', {}).get('state') == state and current_message.get('data', {}).get('kind') == '"
                    + self.job_name
                    + "' and previous_step in " + str(steps)
                ),
                if_=self.context.builder.jobs_context.prefix
                + "-"
                + str(self.context.builder.jobs_context.idx + 1),
                else_=self.body_context.builder.jobs_context.prefix
                + "-"
                + str(self.body_context.builder.jobs_context.idx + 2),
            ),
        )
        utils.insert_then_increment(
            self.body_context.builder.jobs_context,
            self.body_context.builder.jobs_context.idx,
            JumpIntent(
                next_step=self.body_context.prefix
                + "-"
                + str(self.body_context.idx - 1),
                next_state="INTENT_NOT_STARTED"
            ),
        )
        utils.insert_then_increment(
            self.context.builder.jobs_context,
            self.context.builder.jobs_context.idx,
            ExpressionIntent(expression="null", answer_field="null"),
        )
        super().__exit__(exc_type, exc_value, exc_traceback)


def GPTGenerate(
    template: str, context: Optional[Context] = None, args: Dict[str, str] = None
) -> Dict:
    """
    Use a Large Language Model to generate text.

    :param template: The name of the template to use. Must be a valid Python identifier in the context's templates dictionary.
    :param context: The context in which the template is to be generated.
    :param args: A dictionary of arguments to pass to the template.

    :return: The results of the generation as a dictionary
    """

    def builder(context, node, target_field):
        raise_syntax_error = partial(
            utils.raise_syntax_error, context.source_lines, context.filename
        )

        raise_type_error = partial(
            utils.raise_type_error, context.source_lines, context.filename
        )

        signature = inspect.signature(GPTGenerate)
        args = utils.test_signature(
            signature,
            node.args,
            node.keywords,
            partial(raise_type_error, node),
        ).arguments
        # Check that template argument is a constant

        utils.assert_constant_type(
            args["template"],
            str,
            raise_type_error,
            "template must be of type str.",
        )
        template_id = args["template"].value
        # Check if the template_id is valid.
        if template_id not in context.builder.templates:
            utils.raise_template_error(
                context.source_lines,
                context.filename,
                args["template"],
                f"Invalid template {template_id}. Did you include this template?",
            )

        # Check that the context argument is a variable name.
        if args["context"] is None:
            steps = []
        else:
            utils.assert_node_type(
                args["context"],
                ast.Name,
                raise_syntax_error,
                "context must be a variable name.",
            )
            context_name = args["context"].id
            # Raise syntax error if the context is undefined.
            if context_name not in context.step_contexts:
                raise_syntax_error(
                    args["context"],
                    f"Undefined context {context_name}.",
                )
            steps = context.step_contexts[context_name].steps

        gpt_generate_args = {}
        if args["args"] is not None:
            utils.assert_node_type(
                args["args"],
                ast.Dict,
                raise_syntax_error,
                "args must be a dictionary.",
            )
            for k, v in zip(args["args"].keys, args["args"].values):
                utils.assert_constant_type(
                    k,
                    str,
                    raise_syntax_error,
                    "args keys must be strings.",
                )
                gpt_generate_args[k.value] = (
                    "[{py>" + utils.build_expression(v, context.prefix, context) + "}]"
                )
        utils.insert_then_increment(
            context,
            context.idx,
            GPTGenerateIntent(
                template=template_id,
                collect=steps,
                answer_field=target_field,
                args=gpt_generate_args,
            ),
        )

    return builder


def AskOpen(
    question: str,
    turns: int,
    template: str,
    dynamic_stop_regex: Optional[str] = None,
    args: Dict[str, str] = None,
) -> List:
    """
    Use a Large Language Model hold a short conversation
    Variables can be added to the prompt using {var} format.
    They are replaced based on `args`, and then based on the values in `conversation.data`.

    :param question: First message.
    :param turns: Number of turns this conversation should last.
    :param template: The name of the AskOpen template to use.
    :param dynamic_stop_regex: Regex to stop the conversaion once bot generates this trigger.
    :param args: Key value pair of arguments to feed to the template.

    :return: The turns of the conversation as a list. Includes the question, user's response, and the bot's inference,
    """

    def builder(context, node, target_field):
        raise_syntax_error = partial(
            utils.raise_syntax_error, context.source_lines, context.filename
        )

        raise_type_error = partial(
            utils.raise_type_error, context.source_lines, context.filename
        )

        signature = inspect.signature(AskOpen)
        args = utils.test_signature(
            signature,
            node.args,
            node.keywords,
            partial(raise_type_error, node),
        ).arguments
        # Check that template_id is of type str.
        utils.assert_constant_type(
            args["template"],
            str,
            raise_type_error,
            "template must be of type str.",
        )

        template_id = args["template"].value

        utils.assert_constant_type(
            args["turns"],
            int,
            raise_type_error,
            "turns must be of type int.",
        )
        turns = args["turns"].value
        if args["dynamic_stop_regex"] is not None:
            utils.assert_constant_type(
                args["dynamic_stop_regex"], Optional[str], raise_type_error
            )
            dynamic_stop_regex = args["dynamic_stop_regex"].value
        else:
            dynamic_stop_regex = None

        # Check if the template_id is valid.
        if template_id not in context.builder.templates:
            utils.raise_template_error(
                context.source_lines,
                context.filename,
                args["template"],
                f"Invalid template {template_id}. Did you include this template?",
            )

        ask_open_args = {}
        if args["args"] is not None:
            utils.assert_node_type(
                args["args"],
                ast.Dict,
                raise_type_error,
                "args must be a dictionary.",
            )
            for k, v in zip(args["args"].keys, args["args"].values):
                utils.assert_constant_type(
                    k,
                    str,
                    raise_type_error,
                    "args keys must be strings.",
                )
                ask_open_args[k.value] = (
                    "[{py>" + utils.build_expression(v, context.prefix, context) + "}]"
                )
        utils.insert_then_increment(
            context,
            context.idx,
            AskOpenIntent(
                template=template_id,
                followups=turns,
                question=parse_message(context, args["question"]),
                answer_field=target_field,
                dynamic_stop_regex=dynamic_stop_regex,
                args=ask_open_args,
            ),
        )

    return builder


def Expression(
    expression: str,
):
    """
    Make an HTTP Request

    :param expression: Expression string.
    """

    def builder(context, node, target_field):
        raise_type_error = partial(
            utils.raise_type_error, context.source_lines, context.filename
        )

        signature = inspect.signature(Expression)
        args = utils.test_signature(
            signature,
            node.args,
            node.keywords,
            partial(raise_type_error, node),
        ).arguments

        utils.assert_constant_type(args["expression"], str, raise_type_error)
        expression = args["expression"].value

        utils.insert_then_increment(
            context,
            context.idx,
            ExpressionIntent(
                expression=expression,
                answer_field=target_field,
            ),
        )

    return builder


def HTTPRequest(
    url: str,
    body: HTTPBody = None,
    config: HTTPRequestConfig = None,
    method: Literal["GET", "POST"] = None,
    headers: Dict[str, str] = None,
    params: Dict[str, str] = None,
    response_type: Literal["text", "json"] = None,
):
    """
    Make an HTTP Request

    :param url: URL to make the request to
    :param method: HTTP method to send the request with. Default "GET"
    :param headers: Headers to include in the request
    :param params: URL Encoded Parameters to be included in the request
    :param body: Body to be included in the request
    :param response_type: Type to interpret the response body as. Default "json"
    :param config: Config options for HTTP Request
    """

    def builder(context, node, target_field):
        raise_type_error = partial(
            utils.raise_type_error, context.source_lines, context.filename
        )

        signature = inspect.signature(HTTPRequest)
        args = utils.test_signature(
            signature,
            node.args,
            node.keywords,
            partial(raise_type_error, node),
        ).arguments

        url = "!py>" + utils.build_expression(args["url"], context.prefix, context)

        if args["response_type"] is not None:
            utils.assert_constant_type(
                args["response_type"],
                str,
                raise_type_error,
                '`response_type` must be a string, and one of "text" or "json".',
            )
            response_type = args["response_type"].value
            if response_type not in ["text", "json"]:
                raise_type_error(
                    args["response_type"],
                    '`response_type` must be a string, and one of "text" or "json".',
                )
        else:
            response_type = "json"

        if args["method"] is not None:
            utils.assert_constant_type(
                args["method"],
                str,
                raise_type_error,
                '`method` must be a string, and one of "GET" or "POST".',
            )
            method = args["method"].value
            if method not in ["GET", "POST"]:
                raise_type_error(
                    args["method"],
                    '`method` must be a string, and one of "GET" or "POST".',
                )
        else:
            method = "GET"

        headers = {}
        if args["headers"] is not None:
            utils.assert_node_type(
                args["headers"],
                ast.Dict,
                raise_type_error,
                "headers must be a dictionary.",
            )
            for k, v in zip(args["headers"].keys, args["headers"].values):
                utils.assert_constant_type(
                    k,
                    str,
                    raise_type_error,
                    "headers keys must be strings.",
                )
                headers[k.value] = "!py>" + utils.build_expression(
                    v, context.prefix, context
                )

        params = {}
        if args["params"] is not None:
            utils.assert_node_type(
                args["params"],
                ast.Dict,
                raise_type_error,
                "params must be a dictionary.",
            )
            for k, v in zip(args["params"].keys, args["params"].values):
                utils.assert_constant_type(
                    k,
                    str,
                    raise_type_error,
                    "params keys must be strings.",
                )
                params[k.value] = "!py>" + utils.build_expression(
                    v, context.prefix, context
                )

        utils.insert_then_increment(
            context,
            context.idx,
            HTTPRequestIntent(
                url=url,
                answer_field=target_field,
                method=method,
                params=params,
                headers=headers,
            ),
        )

    return builder


_exports = {
    "context_library": [Context, AutoSkip],
    "statement_library": [say],
    "assignment_library": [ask, GPTGenerate, AskOpen, Expression, HTTPRequest],
}
