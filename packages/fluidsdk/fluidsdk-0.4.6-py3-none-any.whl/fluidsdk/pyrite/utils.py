from _ast import ListComp
import ast
import inspect
from copy import deepcopy
from functools import partial
from inspect import Parameter, Signature
from typing import Any, Callable

import astor

from fluidsdk.message import Message
from fluidsdk.pyrite.consts import PYTHON_BUILTINS
import fluidsdk.pyrite.regex_library as regex_library

constants_library = {k: v for k, v in regex_library.__dict__.items() if not k.startswith("__")}


class PyriteSyntaxError(SyntaxError):
    ...


class PyriteTypeError(SyntaxError):
    ...


class PyriteTemplateError(SyntaxError):
    ...

class PyriteContextError(SyntaxError):
    ...

def insert(context, idx, intent):
    if idx is None:
        context.flow_steps[context.prefix] = intent
    else:
        context.flow_steps[f"{context.prefix}-{idx}"] = intent
    for ctx in context.step_contexts.values():
        ctx.add_step(f"{context.prefix}-{idx}", intent)


def insert_then_increment(context, idx, intent):
    insert(context, idx, intent)
    context.idx += 1


def raise_error(error_class, source_lines, filename, node, error_message):
    error = error_class(error_message)
    error.filename = filename
    error.lineno = node.lineno
    error.end_lineno = node.end_lineno
    error.offset = node.col_offset + 1
    error.end_offset = node.end_col_offset
    error.text = source_lines[node.sourcelineno - 1]
    raise error from None


raise_syntax_error = partial(raise_error, PyriteSyntaxError)
raise_type_error = partial(raise_error, PyriteTypeError)
raise_template_error = partial(raise_error, PyriteTemplateError)
raise_context_error = partial(raise_error, PyriteTemplateError)


def build_expression(expression_node, prefix, old_context) -> str:
    context = deepcopy(old_context)
    context.builder = old_context.builder
    context.step_contexts = old_context.step_contexts
    context.flow_steps = {}
    context.idx = 0
    context.prefix = f"{prefix}-expression-{context.idx}"
    syntax_error = partial(raise_syntax_error, context.source_lines, context.filename)

    class RewriteName(ast.NodeTransformer):
        def __init__(self) -> None:
            super().__init__()
            self.temp_names = []

        def visit_Lambda(self, node):
            for arg in zip(node.args.args, node.args.posonlyargs, node.args.kwonlyargs):
                self.temp_names.append(arg.arg)
            return node

        def visit_ListComp(self, node: ListComp) -> Any:
            for generator in node.generators:
                assert_node_type(
                    generator.target,
                    ast.Name,
                    syntax_error,
                    "You can only use one variable for list comprehensions.",
                )
                self.temp_names.append(generator.target.id)
            return node

        def visit_Name(self, node):
            # If name is a global variable, use as is.
            if node.id in context.global_names or node.id in self.temp_names:
                return node
            # Else If, name is a local, index into data_stack
            elif node.id in context.local_names:
                return ast.copy_location(
                    ast.Subscript(
                        value=ast.Subscript(
                            value=ast.Name(id="data_stack", ctx=ast.Load()),
                            slice=ast.UnaryOp(
                                op=ast.USub(), operand=ast.Constant(value=1)
                            ),
                            ctx=ast.Load(),
                        ),
                        slice=ast.Constant(value=node.id),
                        ctx=node.ctx,
                    ),
                    node,
                )
            # Else If, its a python built in. Return as is. (Example "int")
            elif node.id in PYTHON_BUILTINS:
                return node
            # Else name error
            elif node.id in constants_library:
                return ast.Constant(value=constants_library[node.id])
            else:
                syntax_error(node, f"Undefined variable `{node.id}`")

    transformed_node = RewriteName().visit(expression_node)
    return astor.to_source(transformed_node)[:-1]


def get_context_name(context_manager, error_callable):
    if len(context_manager.args) < 1:
        error_callable(
            context_manager,
            'Context name required. Did you mean `with Context("context_name"):`?',
        )
    if len(context_manager.args) > 1:
        error_callable(
            context_manager,
            'Only one context name can be passed. Did you mean `with Context("context_name"):`?',
        )
    context_name_node = context_manager.args[0]
    if not isinstance(context_name_node, ast.Constant) or not isinstance(
        context_name_node.value, str
    ):
        raise_syntax_error(
            context_name_node,
            'Context name must be a of type `str`. Did you mean `with Context("context_name"):`?',
        )
    return context_name_node.value


def make_signature(names):
    return Signature(Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in names)


def test_signature(signature, args, kwargs, error_callable):
    try:
        bound_args = signature.bind(*args, **{i.arg: i.value for i in kwargs})
        bound_args.apply_defaults()
        return bound_args
    except TypeError as e:
        error_callable(str(e))


def assert_node_type(node, type, error_callable, message=None):
    if not isinstance(node, type):
        error_callable(
            node,
            message or f"This must be a {type}.",
        )


def assert_constant_type(node, type, error_callable, message=None):
    if isinstance(node, type):
        return node
    assert_node_type(node, ast.Constant, error_callable, message)
    if not isinstance(node.value, type):
        error_callable(
            node,
            message or f"This must be a {type}.",
        )
    return node.value


def get_builder(f: Callable):
    return f(*([None] * len(inspect.signature(f).parameters)))


def one_of(options):
    replace_of_backtick = "\`"
    return (
        "[{one_of(["
        + ",".join(
            f"`{option.replace('`', replace_of_backtick)}`" for option in options
        )
        + "])}]"
    )
