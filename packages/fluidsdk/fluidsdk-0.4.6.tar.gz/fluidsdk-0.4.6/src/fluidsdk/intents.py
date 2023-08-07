from typing import TYPE_CHECKING, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field

from fluidsdk.message import BotMessageUnion
from fluidsdk.status_webhook import StatusIntentData
from fluidsdk.templates import AskOpenAgentTemplate, AskOpenTemplate, GPTGenerateTemplate, ImageGenerateTemplate

if TYPE_CHECKING:
    from dataclasses import dataclass as _basemodel_decorator
else:
    _basemodel_decorator = lambda x: x


@_basemodel_decorator
class MixTrack(BaseModel):
    event: str = Field(
        "Event Tracked", title="Event", description="Name of the event tracked"
    )
    data: Dict[str, str] = Field(
        {}, title="Data", description="Data to be attached to the mixpanel event."
    )


@_basemodel_decorator
class Intent(BaseModel):
    intent_type: str = Field(
        ..., alias="type", title="Type", description="Type of Intent."
    )
    mixtrack: MixTrack = Field(None)
    status: StatusIntentData = Field(
        None,
        title="Status",
        description="Set the status of the conversation. This will be shown on the dashboard, and pushed to the status webhook of it is present in the flow.",
    )
    next_: str = Field(
        None, alias="next", title="Next", description="Next step to jump to."
    )
    data: Optional[dict] = Field(
        None, title="Data", description="Extra Data for the intent."
    )

    def __add__(self, other):
        if isinstance(other, NextConfig):
            output = self.dict(exclude_unset=True)
            output["next"] = other.next
            return type(self).parse_obj(output)
        elif isinstance(other, StatusIntentData):
            output = self.dict(exclude_unset=True)
            output["status"] = other
            return type(self).parse_obj(output)
        elif isinstance(other, MixTrack):
            output = self.dict(exclude_unset=True)
            output["mixtrack"] = other
            return type(self).parse_obj(output)
        else:
            raise TypeError

    class Config:
        fields = {"mixtrack": {"exclude": True}}
        allow_population_by_field_name = True
        copy_on_model_validation = "none"


@_basemodel_decorator
class NextConfig(BaseModel):
    next: str


@_basemodel_decorator
class AskDefiniteConfig(BaseModel):
    re: str = Field(
        None,
        title="Match Regular Expression",
        description="Regular Expression to run on the answer. If the results is not found, `match_not_found_message` is sent. If it is found, the match is saved in the answer field.",
    )
    match_not_found_message: List[BotMessageUnion] = Field(
        ["Hmmm... Can you send it in the correct format?"],
        title="Match not found message",
        description="A List of messages to send to the user if the answer doesn't have the regex provided in `re`.",
    )
    not_in_list_message: List[BotMessageUnion] = Field(
        ["You must pick from the options above"],
        title="Not in list message",
        description="A List of messages to send to the user if the answer is not in the lists provided.",
    )
    await_for_reply: str = Field(
        "`true`",
        title="Await for reply",
        description="If True, the bot will wait for the user to reply before going to next step.",
    )

    # config for accepting multiple messages

    single: bool = Field(
        True,
        title="Single or wait for multiple messages before moving to next step",
        description="If True, the bot will only accept one answer.",
    )
    done_message: str = Field(
        "When you are done, say, 'done', or click on this button.",
        title="Done Message",
        description="Message to send instructing the user on how to end the step.",
    )
    done_button: str = Field(
        "Done",
        title="Done Button",
        description="Button text to use with the done message. Detection is case insensitive.",
    )
    keep_sending_message: str = Field(
        "Keep sending more, or say 'done'",
        title="Keep Sending Message",
        description="Message sent to the user each time they upload an attachment.",
    )


@_basemodel_decorator
class AskDefiniteIntent(Intent):
    intent_type: Literal["ask-definite"] = Field("ask-definite")
    question: Union[str, List[BotMessageUnion]] = Field(
        ..., title="Question", description="A List of questions to ask the user."
    )
    answer_field: str = Field(
        ...,
        title="Answer Field",
        description="Field in the user's Conversation_Model.data to store the answer in.",
    )
    list_only: bool = Field(
        False,
        title="List Only",
        description="If True, and InteractiveMessage present in questions, the response must be of the options.",
    )
    mirror: bool = Field(
        False,
        title="Mirror",
        description="Whether to mirror, i.e. acknowledge the user's response.",
    )
    config: AskDefiniteConfig = Field(
        AskDefiniteConfig(), title="Config", description="Ask Definite Config"
    )
    # TODO Add mirror settings field, to add custom prompts

    def __add__(self, other):
        if isinstance(other, AskDefiniteConfig):
            config = self.config.dict(exclude_unset=True)
            config.update(other.dict(exclude_unset=True))
            output = self.dict(exclude_unset=True)
            output["config"] = config
            return AskDefiniteIntent.parse_obj(output)
        elif isinstance(other, SayIntent):
            questions = self.question + other.text
            output = self.dict(exclude_unset=True)
            output["question"] = questions
            return AskDefiniteIntent.parse_obj(output)
        else:
            return super().__add__(other)


@_basemodel_decorator
class AskOpenIntent(Intent):
    intent_type: Literal["ask-open"] = Field("ask-open")
    template: Union[str, AskOpenTemplate] = Field(
        ...,
        title="Template",
        description="Template to use from intentsdb, or template object.",
    )
    question: BotMessageUnion = Field(
        None,
        title="Question",
        description="Question to ask the user, instead of the one in template. This does not get added to the prompt to generate the followup.",
    )
    answer_field: str = Field(
        ...,
        title="Answer Field",
        description="Field in the user's Conversation_Model.data to store the answer in.",
    )
    followups: int = Field(
        ...,
        title="Followups",
        description="Number of followups.",
    )
    dynamic_stop_regex: Optional[str] = Field(
        None,
        title="Dynamic Stop Regex",
        description="Regex to stop the conversaion once bot generates this trigger",
    )
    args: Dict[str, str] = Field(
        {},
        title="Arguments",
        description="Key value pair of arguments to feed to the template.",
    )


@_basemodel_decorator
class SayIntent(Intent):
    intent_type: Literal["say"] = Field("say")
    text: Union[str, List[BotMessageUnion]] = Field(
        ..., title="Question", description="A list of messages to send to the user."
    )

    def __add__(self, other):
        if isinstance(other, AskDefiniteIntent):
            questions = self.text + other.question
            output = other.dict(exclude_unset=True)
            output["question"] = questions
            return AskDefiniteIntent.parse_obj(output)
        elif isinstance(other, SayIntent):
            text = self.text + other.text
            output = other.dict(exclude_unset=True)
            output["text"] = text
            return SayIntent.parse_obj(output)
        else:
            return super().__add__(other)


@_basemodel_decorator
class ConditionIntent(Intent):
    intent_type: Literal["condition"] = Field("condition")
    condition: str = Field(
        ...,
        title="Condition",
        description="A JMESPath expression to be run on the user data. Returns a `bool`.",
    )
    if_: str = Field(
        ...,
        alias="if",
        title="If",
        description="Step to go to if condition is True",
    )

    else_: str = Field(
        None,
        alias="else",
        title="Else",
        description="Step to go to if condition is False",
    )


@_basemodel_decorator
class GPTGenerateIntent(Intent):
    intent_type: Literal["gpt-generate"] = Field("gpt-generate")
    template: Union[str, GPTGenerateTemplate] = Field(
        ...,
        title="Template",
        description="Template to use from intentsdb, or template object.",
    )
    args: Dict[str, str] = Field(
        {},
        title="Arguments",
        description="Key value pair of arguments to feed to the template.",
    )
    collect: List[str] = Field(
        [],
        title="Collect",
        description="An array of step names to collect answers from to feed to the template.",
    )
    answer_field: str = Field(
        ...,
        title="Answer Field",
        description="Field in the user's Conversation_Model.data to store the answer in.",
    )


@_basemodel_decorator
class GPTSearchIntent(Intent):
    intent_type: Literal["gpt-search"] = Field("gpt-search")
    engine: Literal[
        "davinci",
        "curie",
        "babbage",
        "ada",
    ] = Field(
        "davinci",
        title="Engine",
        description="Name of the large language model to use.",
    )
    query: str = Field(
        ...,
        title="Query",
        description="Query to run the search on.",
    )
    documents: Union[str, List[str]] = Field(
        ...,
        title="Documents",
        description="Documents or The ID of an uploaded file that contains documents to search over.",
    )
    purpose: str = Field(
        ..., title="Purpose", description="Purpose to use for mixpanel tracking."
    )
    max_rerank: int = Field(
        200,
        title="Max Rerank",
        description="The maximum number of documents to be re-ranked and returned by search.",
    )
    return_metadata: bool = Field(
        True,
        title="Return Metadata",
        description="A special boolean flag for showing metadata. If set to true, each document entry in the returned JSON will contain a 'metadata' field.",
    )
    answer_field: str = Field(
        ...,
        title="Answer Field",
        description="Field in the user's Conversation_Model.data to store the answer in.",
    )


@_basemodel_decorator
class CollectAttachmentsConfig(BaseModel):
    done_message: str = Field(
        "When you are done, say, 'done', or click on this button.",
        title="Done Message",
        description="Message to send instructing the user on how to end the step.",
    )
    done_button: str = Field(
        "Done",
        title="Done Button",
        description="Button text to use with the done message. Detection is case insensitive.",
    )
    non_file_error_message: str = Field(
        "Please upload a file.",
        title="Not File Error Message",
        description="Message sent to the user when they don't upload a file.",
    )
    wrong_file_type_error_message: str = Field(
        "Please upload only a {file_types} file.",
        title="Wrong File Type Error Message",
        description="Message sent to the user when they upload a file of the wrong type. `{file_types}` is replaced with the list of valid file types.",
    )
    keep_sending_message: str = Field(
        "Keep sending more, or say 'done'",
        title="Keep Sending Message",
        description="Message sent to the user each time they upload an attachment.",
    )


@_basemodel_decorator
class CollectAttachmentsIntent(Intent):
    intent_type: Literal["collect-attachments"] = Field("collect-attachments")
    attachment_types: List[
        Literal["image", "video", "document", "voice", "audio"]
    ] = Field(
        [],
        min_items=1,
        title="Attachment Types",
        description="List of allowed attachments.",
    )
    text: List[BotMessageUnion] = Field(
        ..., title="Text", description="A list of messages to send to the user."
    )
    answer_field: str = Field(
        ...,
        title="Answer Field",
        description="Field in the user's Conversation_Model.data to store the answer in.",
    )
    optional: bool = Field(
        False, title="Optional", description="Whether this step is optional."
    )
    single: bool = Field(
        True,
        title="Single",
        description="Whether this step takes only one attachment, or multiple.",
    )
    config: CollectAttachmentsConfig = Field(
        CollectAttachmentsConfig(), title="Config", description="Message Configuration."
    )

    def __add__(self, other):
        if isinstance(other, SayIntent):
            text = self.text + other.text
            output = self.dict(exclude_unset=True)
            output["text"] = text
            return CollectAttachmentsIntent.parse_obj(output)
        else:
            return super().__add__(other)


@_basemodel_decorator
class ExpressionIntent(Intent):
    intent_type: Literal["expression"] = Field("expression")
    expression: str = Field(
        ...,
        title="Expression",
        description="A JMESPath expression to be run on the user data.",
    )
    answer_field: str = Field(
        ...,
        title="Answer Field",
        description="Field in the user's Conversation_Model.data to store the answer in.",
    )


@_basemodel_decorator
class HTTPBody(BaseModel):
    body_type: Literal["text", "json", "form"] = Field(
        "text",
        alias="type",
        title="Body Type",
        description="Type of request body. Changes how `data` is parsed and adds relevant `Content-Type` Header.",
    )
    data: Union[str, dict, list, int, float] = Field(
        None, title="Data", description="HTTP Body Data."
    )

    class Config:
        allow_population_by_field_name = True


http_request_cache = {}


@_basemodel_decorator
class HTTPRequestConfig(BaseModel):
    cache: bool = Field(
        False, title="Cache", description="Whether or not to cache the responses"
    )
    cache_size: int = Field(
        180, title="Cache Size", description="Number of items to store in the cache"
    )
    cache_ttl: int = Field(
        3600, title="Cache TTL", description="Time to Live to use for the cache"
    )
    cache_type: Literal["TTLCache", "FIFOCache", "LFUCache", "LRUCache"] = Field(
        "LRUCache", title="Cache Type", description="Type of cache to use"
    )
    cache_save: str = Field(
        "`true`",
        title="Cache Save",
        description="Whether or not to add the result to cache.",
    )
    cache_skip: str = Field(
        "`false`",
        title="Cache Skip",
        description="Whether or not to skip checking the cache for the response.",
    )


@_basemodel_decorator
class HTTPRequestIntent(Intent):
    intent_type: Literal["http"] = Field("http")
    url: str = Field(
        ...,
        title="URL",
        description="URL to send the request to.",
    )
    method: Literal["GET", "POST"] = Field(
        "GET", title="Method", description="HTTP Method to use for making the request."
    )
    headers: Dict[str, str] = Field(
        {}, title="Headers", description="HTTP headers to include in the request"
    )
    params: Dict[str, str] = Field(
        {},
        title="Parameters",
        description="URL Encoded Parameters to be included in the requested.",
    )
    body: HTTPBody = Field(
        None, title="Body", description="HTTP Body to be included in the request."
    )
    response_type: Literal["text", "json"] = Field(
        "json",
        title="Response Type",
        description="Type to interpret the response body as.",
    )
    answer_field: str = Field(
        ...,
        title="Answer Field",
        description="Field in the user's Conversation_Model.data to store the answer in.",
    )
    config: HTTPRequestConfig = Field(
        HTTPRequestConfig(),
        title="HTTP Request Config",
        description="Config options for HTTP Request Intent",
    )


@_basemodel_decorator
class TextOnImageConfig(BaseModel):
    text: str = Field(
        ...,
        title="Text to be added on the image",
        description="Text to be displayed on the image",
    )
    font_size: int = Field(
        14,
        title="Font size",
        description="Font size of the text to be displayed on the image",
    )
    font_color: Union[str, tuple] = Field(
        "#000000",
        title="Font color in hex #rrggbb or #rrggbbaa, or color name",
        description="Example: #ffffff, red, etc.",
    )
    font_family: str = Field(
        "static/Advent_Pro/AdventPro-Regular.ttf",
        title="Font family ttf file path",
        description="Example: static/Advent_Pro/AdventPro-Regular.ttf",
    )
    position: List[float] = Field(
        [
            0.5,
            0.5,
        ],  # http://griddrawingtool.com/ in step 5 use at least 10x10 grid lines with Keep boxes square checked off
        title="Fractional position similar to viewport width and height in css. ex. [5/16, 6/15]",
        description="Example: [0.5, 0.5] will put the text right on center of image",
    )


class DynamicImage(Intent):
    intent_type: Literal["generate-image"] = Field("generate-image")
    template_path: str = Field(  # local file path, TODO: add expression/remote urls
        ...,
        title="Image path",
        description="Local Path to the image.",
    )
    text_config: List[TextOnImageConfig] = Field(
        [], title="Text on image and its style and position config"
    )
    caption: str = Field(
        "",
        title="Caption",
        description="Caption to be displayed along with the image",
    )


def one_of(options: List[str]):
    """
    Randomly select one of the list of options given

    Args:
        options (List[str]): List of options (strings) pool to select one.

    Returns:
        option (str): A randomly selected option string from the pool

    Example:
        $ one_of(["Apple", "Banana", "Carrot", "Date"])
    """
    replace_of_backtick = "\`"  # noqa: W605
    clean_and_join_options = ",".join(
        f"`{option.replace('`', replace_of_backtick)}`" for option in options
    )
    return "[{one_of([" + clean_and_join_options + "])}]"


KB_ASK_QUESTION = one_of(
    [
        "I'm ready to answer your questions.",
        "I'm happy to answer any questions you may have.",
        "Just ask, I'll answer anything.",
        "I'll answer any question, just ask.",
        "Anything you want to know, just ask.",
        "Feel free to ask me anything.",
        "I'm an open book, ask away.",
        "Don't be shy, ask me anything.",
        "Ask me anything, I don't mind.",
        "You can ask me anything you want.",
        "I don't mind answering questions, go ahead and ask.",
        "Ask away, I don't mind answering.",
    ]
)
class KnowledgeBaseSearchConfig(BaseModel):
    question: str = Field(KB_ASK_QUESTION, title="Question to ask")
    search_threshold: float = Field(
        0.5,
        title="Search Result Limit",
        description="Number of search results to be displayed",
    )
    limit_turns: Union[int, None] = Field(
        None,
        title="Limit Turns",
        description="Number of turns to limit the search and FAQ intent to",
    )


class KnowledgeBaseSearch(Intent):
    intent_type: Literal["knowledge-base-search"] = Field("knowledge-base-search")
    collection: str = Field(
        ..., title="Knowledge Base's Collection name", description="Collection name"
    )
    answer_field: str = Field(..., title="Answer field", description="Answer field")
    context: Union[str, None] = Field(
        None, title="Context", description="Context for the knowledge base paraphrasing"
    )
    config: KnowledgeBaseSearchConfig = Field(
        KnowledgeBaseSearchConfig(), title="Search Config"
    )


class ImageGenerateIntent(Intent):
    intent_type: Literal["dalle-generate"] = Field("dalle-generate")
    template: Union[str, ImageGenerateTemplate] = Field(
        ...,
        title="Template",
        description="Template to use from intentsdb, or template object.",
    )
    answer_field: str = Field(
        ...,
        title="Answer Field",
        description="Field in the user's Conversation_Model.data to store the answer in.",
    )

@_basemodel_decorator
class AskOpenAgentIntent(Intent):
    intent_type: Literal["ask-agent-open"] = Field("ask-agent-open")
    template: Union[str, AskOpenAgentTemplate] = Field(
        ...,
        title="Template",
        description="Template to use from intentsdb, or template object.",
    )
    question: BotMessageUnion = Field(
        None,
        title="Question",
        description="Question to ask the user, instead of the one in template. This does not get added to the prompt to generate the followup.",
    )
    answer_field: str = Field(
        ...,
        title="Answer Field",
        description="Field in the user's Conversation_Model.data to store the answer in.",
    )
    followups: int = Field(
        ...,
        title="Followups",
        description="Number of followups.",
    )
    dynamic_stop_regex: Optional[str] = Field(
        None,
        title="Dynamic Stop Regex",
        description="Regex to stop the conversaion once bot generates this trigger",
    )
    args: Dict[str, str] = Field(
        {},
        title="Arguments",
        description="Key value pair of arguments to feed to the template.",
    )


@_basemodel_decorator
class JumpIntent(Intent):
    intent_type: Literal["jump"] = Field("jump")
    next_step: str = Field(None, title="Next Step", description="Next step to jump to.")
    next_state: str = Field(
        "INTENT_NOT_STARTED", title="Next State", description="State to be in after jumping."
    )
    stop_processing: bool = Field(
        False,
        title="Stop Processing",
        description="Whether or not to stop processing intents after the jump",
    )

@_basemodel_decorator
class ScheduleJobIntent(Intent):
    intent_type: Literal["schedule-job"] = Field("schedule-job")
    trigger_time: str = Field(...)
    data: dict = Field(
        {}, title="Next State", description="State to be in after jumping."
    )