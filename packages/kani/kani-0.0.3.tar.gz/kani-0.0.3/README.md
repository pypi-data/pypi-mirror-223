# kani (カニ)

[![Test Package](https://github.com/zhudotexe/kani/actions/workflows/pytest.yml/badge.svg)](https://github.com/zhudotexe/kani/actions/workflows/pytest.yml)
[![Documentation Status](https://readthedocs.org/projects/kani/badge/?version=latest)](https://kani.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/kani)](https://pypi.org/project/kani/)
[![Quickstart in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zhudotexe/kani/blob/main/examples/colab_quickstart.ipynb)

kani (カニ) is a lightweight and highly hackable harness for chat-based language models with tool usage/function calling.

Compared to other LM harnesses, kani is less opinionated and offers more fine-grained customizability
over the parts of the control flow that matter, making it the perfect choice for NLP researchers, hobbyists, and
developers alike.

kani comes with support for OpenAI models and LLaMA v2 out of the box, with a model-agnostic framework to add support
for many more.

[Read the docs on ReadTheDocs!](http://kani.readthedocs.io/)

## Features

- **Lightweight and high-level** - kani implements common boilerplate to interface with language models without forcing
  you to use opinionated prompt frameworks or complex library-specific tooling.
- **Model agnostic** - kani provides a simple interface to implement: token counting and completion generation.
  Implement these two, and kani can run with any language model.
- **Automatic chat memory management** - Allow chat sessions to flow without worrying about managing the number of
  tokens in the history - kani takes care of it.
- **Function calling with model feedback and retry** - Give models access to functions in just one line of code.
  kani elegantly provides feedback about hallucinated parameters and errors and allows the model to retry calls.
- **You control the prompts** - There are no hidden prompt hacks. We will never decide for you how to format your own
  data, unlike other popular language model libraries.
- **Fast to iterate and intuitive to learn** - With kani, you only write Python - we handle the rest.
- **Asynchronous design from the start** - kani can scale to run multiple chat sessions in parallel easily, without
  having to manage multiple processes or programs.

## Quickstart

kani requires Python 3.10 or above.

First, install the library. In this quickstart, we'll use the OpenAI engine, though kani
is [model-agnostic](https://kani.readthedocs.io/en/latest/engines.html).

```shell
$ pip install "kani[openai]"
```

Then, let's use kani to create a simple chatbot using ChatGPT as a backend.

```python
# import the library
from kani import Kani, chat_in_terminal
from kani.engines.openai import OpenAIEngine

# Replace this with your OpenAI API key: https://platform.openai.com/account/api-keys
api_key = "sk-..."

# kani uses an Engine to interact with the language model. You can specify other model 
# parameters here, like temperature=0.7.
engine = OpenAIEngine(api_key, model="gpt-3.5-turbo")

# The kani manages the chat state, prompting, and function calling. Here, we only give 
# it the engine to call ChatGPT, but you can specify other parameters like 
# system_prompt="You are..." here.
ai = Kani(engine)

# kani comes with a utility to interact with a kani through your terminal! Check out 
# the docs for how to use kani programmatically.
chat_in_terminal(ai)
```

kani makes the time to set up a working chat model short, while offering the programmer deep customizability over
every prompt, function call, and even the underlying language model.

## Docs

To learn more about how
to [customize kani with your own prompt wrappers](https://kani.readthedocs.io/en/latest/customization.html),
[function calling](https://kani.readthedocs.io/en/latest/function_calling.html), and
more, [read the docs!](http://kani.readthedocs.io/)

Or take a look at the hands-on examples [in this repo](https://github.com/zhudotexe/kani/tree/main/examples).

## Demo

Want to see kani in action? Using 4-bit quantization to shrink the model, we run LLaMA v2 as part of our test suite
right on GitHub Actions:

https://github.com/zhudotexe/kani/actions/workflows/pytest.yml?query=branch%3Amain

Simply click on the latest build to see LLaMA's output!

<!--
For developers:

## Build and Publish

`fastlmi` uses Hatchling to build.

Make sure to bump the version in pyproject.toml before publishing.

```shell
rm -r dist/
python -m build
python -m twine upload dist/*
```
-->
