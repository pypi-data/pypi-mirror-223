import ast
from typing import Literal, Optional
from fluidsdk.message import InteractiveMessageOption, InteractiveMessage, Message
import inspect
from functools import partial
from fluidsdk.pyrite.utils import (
    assert_node_type,
    assert_constant_type,
    build_expression,
    get_builder,
    test_signature,
    raise_type_error,
    raise_syntax_error,
)


def Option(
    title: str,
    description: Optional[str] = None,
    id: Optional[str] = None,
):
    def builder(context, node):
        syntax_error = partial(
            raise_syntax_error,
            context.source_lines,
            context.filename,
        )
        type_error = partial(
            raise_type_error,
            context.source_lines,
            context.filename,
        )
        if not isinstance(node, ast.Call) or not node.func.id == "Option":
            if isinstance(node, ast.Constant):
                if isinstance(node.value, str):
                    return node.value
                else:
                    type_error(
                        node,
                        f"{type(node.value)} is not a valid option type. Try using a `str` or `Option` instead.",
                    )
            elif isinstance(node, ast.Name):
                if node.id in context.global_names:
                    return "{" + node.id + "}"
                elif node.id in context.local_names:
                    return '!py>data_stack[-1]["' + node.id + '"]'
                else:
                    syntax_error(node, f"Undefined variable `{node.id}`")
            elif isinstance(node, ast.Starred):
                syntax_error(node, "Starred objects are not suppored yet.")
            else:
                expression = build_expression(node, context.prefix, context)
                return "!py>" + expression

        assert_node_type(
            node, ast.Call, type_error, 'This must be an Option. Try: Option("title")'
        )

        signature = inspect.signature(Option)
        args = test_signature(
            signature,
            node.args,
            node.keywords,
            partial(raise_type_error, node),
        ).arguments

        assert_constant_type(args["title"], str, type_error)
        title = args["title"].value
        if args["id"] is not None:
            assert_constant_type(args["id"], Optional[str], type_error)
            id = args["id"].value
        else:
            id = None
        if args["description"] is not None:
            assert_constant_type(args["description"], Optional[str], type_error)
            description = args["description"].value
        else:
            description = None

        return InteractiveMessageOption(
            **{
                k: v
                for k, v in {
                    "id": id,
                    "title": title,
                    "description": description,
                }.items()
                if v is not None
            }
        )

    return builder


def Interactive(
    body: str,
    footer: str = None,
    options: list = None,
    type: Literal["button", "list"] = None,
) -> InteractiveMessage:
    """
    Interactive Message.

    :param body: Body of the message
    :param footer: Footer of the message
    :param options: Options of the message
    :param type: Type of interactive message. Defaults to "list"

    :return: Interactive Message
    """

    def builder(context, node):
        signature = inspect.signature(Interactive)
        args = test_signature(
            signature,
            node.args,
            node.keywords,
            partial(raise_type_error, node),
        ).arguments
        syntax_error = partial(
            raise_syntax_error,
            context.source_lines,
            context.filename,
        )
        type_error = partial(
            raise_type_error,
            context.source_lines,
            context.filename,
        )
        if isinstance(args["body"], ast.Constant):
            if isinstance(args["body"].value, str):
                body = args["body"].value
            else:
                type_error(
                    node,
                    f"{type(args['body'].value)} is not a valid message type. Try using a `str` instead.",
                )
        else:
            body = "!py>" + build_expression(args["body"], context.prefix, context)
        if args["footer"] is not None:
            assert_constant_type(args["footer"], Optional[str], type_error)
            footer = args["footer"].value
        else:
            footer = None
        if args["type"] is not None:
            if args["type"].value is not None:
                assert_constant_type(args["type"], str, type_error)
                if args["type"].value not in ["button", "list"]:
                    type_error(args["type"], '`type` must be one of "button" or "list"')
            type = args["type"].value
        else:
            type = None
        if args["options"] is not None:
            if isinstance(args["options"], ast.List):
                options = list(
                    map(
                        lambda node: get_builder(Option)(context, node),
                        args["options"].elts,
                    )
                )
            else:
                options = "py>" + build_expression(
                    args["options"], context.prefix, context
                )
        else:
            options = None

        return InteractiveMessage(
            **{
                k: v
                for k, v in {
                    "body": body,
                    "footer": footer,
                    "type": type,
                    "options": options,
                }.items()
                if v is not None
            }
        )

    return builder


def parse_message(context, node):
    syntax_error = partial(
        raise_syntax_error,
        context.source_lines,
        context.filename,
    )
    type_error = partial(
        raise_type_error,
        context.source_lines,
        context.filename,
    )
    if isinstance(node, ast.Constant):
        if isinstance(node.value, str):
            return Message(message=node.value)
        else:
            type_error(
                node,
                f"{type(node.value)} is not a valid message type. Try using a `str` instead.",
            )
    elif isinstance(node, ast.Name):
        if node.id in context.global_names:
            return Message(message="{node.id}")
        elif node.id in context.local_names:
            return Message(message='[{py>data_stack[-1]["' + node.id + '"]}]')
        else:
            syntax_error(node, f"Undefined variable `{node.id}`")
    elif isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in ["Interactive"]:
            builder = get_builder(Interactive)
            return builder(context, node)
        else:
            expression = build_expression(node, context.prefix, context)
            return Message(message="[{py>" + expression + "}]")
    else:
        expression = build_expression(node, context.prefix, context)
        return Message(message="[{py>" + expression + "}]")


def parse_messages(context, nodes):
    return map(partial(parse_message, context), nodes)
