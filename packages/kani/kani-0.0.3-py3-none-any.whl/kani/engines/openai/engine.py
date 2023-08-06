from kani.ai_function import AIFunction
from kani.exceptions import MissingModelDependencies
from kani.models import ChatMessage
from .client import OpenAIClient
from .models import FunctionSpec, ChatCompletion
from ..base import BaseEngine

try:
    import tiktoken
except ImportError as e:
    raise MissingModelDependencies(
        'The OpenAIEngine requires extra dependencies. Please install kani with "pip install kani[openai]".'
    ) from None

# https://platform.openai.com/docs/models
CONTEXT_SIZES_BY_PREFIX = [
    ("gpt-3.5-turbo-16k", 16384),
    ("gpt-3.5-turbo", 4096),
    ("gpt-4-32k", 32768),
    ("gpt-4", 8192),
    ("text-davinci-", 4096),
    ("code-", 8000),
    ("", 2048),  # e.g. aba/babbage/curie/davinci
]


class OpenAIEngine(BaseEngine):
    """Engine for using the OpenAI API.

    .. caution::

        Due to having to track "hidden" tokens for the function spec, it is not recommended to reuse an OpenAIEngine
        instance in multiple kani. To take advantage of reuse, construct a shared :class:`.OpenAIClient` and
        initialize OpenAIEngine with ``client=the_client_instance`` rather than ``api_key="..."``.
    """

    def __init__(
        self,
        api_key: str = None,
        model="gpt-3.5-turbo",
        max_context_size: int = None,
        organization: str = None,
        retry: int = 5,
        *,
        client: OpenAIClient = None,
        **hyperparams,
    ):
        """
        :param api_key: Your OpenAI API key.
        :param model: The key of the model to use.
        :param max_context_size: The maximum amount of tokens allowed in the chat prompt. If None, uses the given
            model's full context size.
        :param organization: The OpenAI organization to use in requests (defaults to the API key's default org).
        :param retry: How many times the engine should retry failed HTTP calls with exponential backoff (default 5).
        :param client: An instance of :class:`.OpenAIClient` (for reusing the same client in multiple engines). You must
            specify exactly one of (api_key, client). If this is passed the ``organization`` and ``retry`` params will
            be ignored.
        :param hyperparams: Any additional parameters to pass to
            :meth:`.OpenAIClient.create_chat_completion`.
        """
        if (api_key is None and client is None) or (api_key and client):
            raise ValueError("You must supply exactly one of (api_key, client).")
        if max_context_size is None:
            max_context_size = next(size for prefix, size in CONTEXT_SIZES_BY_PREFIX if model.startswith(prefix))
        self.client = client or OpenAIClient(api_key)
        self.model = model
        self.max_context_size = max_context_size
        self.hyperparams = hyperparams
        self.tokenizer = None  # tiktoken caches a tokenizer globally in module, so we can unconditionally load it
        self.token_reserve = 0
        self._load_tokenizer()

    def _load_tokenizer(self):
        try:
            self.tokenizer = tiktoken.encoding_for_model(self.model)
        except KeyError:
            self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def message_len(self, message: ChatMessage) -> int:
        mlen = 5  # ChatML = 4, role = 1
        if message.content:
            mlen += len(self.tokenizer.encode(message.content))
        if message.name:
            mlen += len(self.tokenizer.encode(message.name))
        if message.function_call:
            mlen += len(self.tokenizer.encode(message.function_call.name))
            mlen += len(self.tokenizer.encode(message.function_call.arguments))
        return mlen

    async def predict(
        self, messages: list[ChatMessage], functions: list[AIFunction] | None = None, **hyperparams
    ) -> ChatCompletion:
        if functions:
            function_spec = [FunctionSpec(name=f.name, description=f.desc, parameters=f.json_schema) for f in functions]
        else:
            function_spec = None
        completion = await self.client.create_chat_completion(
            model=self.model, messages=messages, functions=function_spec, **self.hyperparams, **hyperparams
        )
        # calculate function calling reserve tokens on first run
        if functions and self.token_reserve == 0:
            self.token_reserve = max(completion.prompt_tokens - sum(self.message_len(m) for m in messages), 0)
        return completion

    async def close(self):
        await self.client.close()
