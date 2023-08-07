ENGINE_GLOBALS = ["math", "pcre", "random", "json"]


PYTHON_BUILTINS = [
    "abs",
    "all",
    "any",
    "ascii",
    "bin",
    "bool",
    "bytearray",
    "bytes",
    "callable",
    "chr",
    "complex",
    "dict",
    "divmod",
    "enumerate",
    "filter",
    "float",
    "format",
    "frozenset",
    "getattr",
    "hasattr",
    "hash",
    "int",
    "isinstance",
    "issubclass",
    "iter",
    "len",
    "list",
    "map",
    "max",
    "min",
    "next",
    "object",
    "oct",
    "ord",
    "pow",
    "range",
    "repr",
    "reversed",
    "round",
    "set",
    "slice",
    "sorted",
    "str",
    "sum",
    "tuple",
    "type",
    "zip",
]


ASK_AND_ACK_PRE_PROMPT = """Acknowledgment means showing that you’ve heard and understood. Acknowledgment is all about understanding others and showing empathy in words rather than what would be a cold robotic conversation.

Acknowledgments in critical conversations help improve interpersonal trust, show empathy towards the speaker and make the conversation natural and engaging to let the speaker share more.

Use emojis minimally. It is very very important and necessary that all the acknowledgements are only sentences. No Questions! Only sentences.
Let's go through some examples where Person B has to just acknowledge Person A's reply after thinking step by step carefully:

Question: What's your age?
Person A says: What's your age?
Explanation: Now person A just repeated the question asked, so they are being sarcastic or they don't want to share their age. Either way, the best acknowledgment in this case would be a soft opaque indirect clever reply.
Person B: You're quite curious huh 🧐

###

(Tip: This is a survey for employees in the organization. If the response indicates poor employee experience acknowledge it very detailedly and caring way or else vibe along cheerfully)
Question: I like the people I work with at this organization.
Person A: no they bully me and make fun of me
Explanation: Person A explicitly says they are bullied and made fun of at their organization, which is a very terrible thing to go through. This is a very emotional conversation so the acknowledgment per tip should be caring, very detailed, and empathetic.
Person B: That sounds like it must be really tough for you to deal with that every day 🙁. I hope you've talked to someone about it and they're helping you out.

###

(Tip: Assure if the person feels like they didn't study that much or compliment them)
Question: What is your highest level of education?
Person A says: I did a Ph.D. in quantum computing, but I couldn't continue in academia
Explanation: Person A has a Ph.D. but they couldn't continue in academia. This is a sad and regretful state to be in. The best acknowledgment as per the tip would be a soft transparent acknowledgment like:
Person B: 😮 That's still really impressive! I'm sure you've done a lot with your knowledge. 🤘

###

(Tip: acknowledge either super happily or empathize positively and assuringly that the future is gonna look good)
Question: How often do you express your love or desire for them in a non-sexual manner?
Person A says: I don't have any partner
Explanation: Person A doesn't have any partner to express their love to in a non-sexual way. This is a sad and lonely state to be in. The best acknowledgment as per the tip would be a strong empathizing acknowledgment like:
Person B: That sounds really tough🫂. I'm sure you'll find someone special soon who appreciates your love 🤞

###

Question: How actively fit are you?
Person A says: I ate biryani yesterday
Explanation: The question is asking about fitness levels and person A replied with Biryani which is a high-calorie food. This is an indirect response and even though person A might not be fit they are being funny and making a joke. The best acknowledgment, in this case, would be an appreciative acknowledgment.
Person B: 😂 You have a great sense of humor! But, I am sure you are fit enough

###

"""
