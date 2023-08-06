# EasyLLM - 

EasyLLM is an open source project that provides helpful tools and methods for working with large language models (LLMs), both open source and closed source. Get immediataly started or check out the [documentation](https://philschmid.github.io/easyllm/).

EasyLLM implements clients that are compatible with OpenAI's Completion API. This means you can easily replace `openai.ChatCompletion`, `openai.Completion`, `openai.Embedding` with, for example, `huggingface.ChatCompletion`, `huggingface.Completion` or `huggingface.Embedding` by changing one line of code.

### Supported Clients 

* `huggingface` - [HuggingFace](https://huggingface.co/) models
  * `huggingface.ChatCompletion` - Chat with LLMs
  * `huggingface.Completion` - Text completion with LLMs
  * `huggingface.Embedding` - Create embeddings with LLMs

Check out the [Examples](./examples) to get started.

## 🚀 Getting Started

Install EasyLLM via pip:

```bash
pip install easyllm
```

Then import and start using the clients:

```python

from easyllm.clients import huggingface

# helper to build llama2 prompt
huggingface.prompt_builder = "llama2"

response = huggingface.ChatCompletion.create(
    model="meta-llama/Llama-2-70b-chat-hf",
    messages=[
        {"role": "system", "content": "\nYou are a helpful assistant speaking like a pirate. argh!"},
        {"role": "user", "content": "What is the sun?"},
    ],
    temperature=0.9,
    top_p=0.6,
    max_tokens=256,
)

print(response)
```
the result will look like 

```bash
{
  "id": "hf-lVC2iTMkFJ",
  "object": "chat.completion",
  "created": 1690661144,
  "model": "meta-llama/Llama-2-70b-chat-hf",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": " Arrrr, the sun be a big ol' ball o' fire in the sky, me hearty! It be the source o' light and warmth for our fair planet, and it be a mighty powerful force, savvy? Without the sun, we'd be sailin' through the darkness, lost and cold, so let's give a hearty \"Yarrr!\" for the sun, me hearties! Arrrr!"
      },
      "finish_reason": null
    }
  ],
  "usage": {
    "prompt_tokens": 111,
    "completion_tokens": 299,
    "total_tokens": 410
  }
}
```

Check out other examples:
* [Detailed ChatCompletion Example](notebooks/chat-completion-api.ipynb)
* [Example how to stream chat requests](notebooks/stream-chat-completions.ipynb)
* [Example how to stream text requests](notebooks/stream-text-completions.ipynb)
* [Detailed Completion Example](notebooks/text-completion-api.ipynb)
* [Create Embeddings](notebooks/get-embeddings)

See the [documentation](https://philschmid.github.io/easyllm/) for more detailed usage and examples.

## 💪🏻 Migration from OpenAI to HuggingFace

Migrating from OpenAI to HuggingFace is easy. Just change the import statement and the client you want to use and optionally the prompt builder.

```diff
- import openai
+ from easyllm.clients import huggingface
+ huggingface.prompt_builder = "llama2"


- response = openai.ChatCompletion.create(
+ response = huggingface.ChatCompletion.create(
-    model="gpt-3.5-turbo",
+    model="meta-llama/Llama-2-70b-chat-hf",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Knock knock."},
    ],
)
```

Make sure when you switch your client that your hyperparameters are still valid. For example, `temperature` of GPT-3 might be different than `temperature` of `Llama-2`.

## ☑️ Key Features

### 🤝 Compatible Clients

- Implementation of clients compatible with OpenAI API format of `openai.ChatCompletion`, `openai.Completion`, `openai.Embedding`.
- Easily switch between different LLMs like `openai.ChatCompletion` and `huggingface.ChatCompletion` by changing one line of code. 
- Support for streaming of completions, checkout example [How to stream completions](./notebooks/stream-chat-completions.ipynb).

### ⚙️ Helper Modules ⚙️

- `evol_instruct` (work in progress) - Use evolutionary algorithms create instructions for LLMs.

- `prompt_utils` - Helper methods to easily convert between prompt formats like OpenAI Messages to prompts for open source models like Llama 2.

## 📔 Citation & Acknowledgements

If you use EasyLLM, please share it with me on social media or email. I would love to hear about it!
You can also cite the project using the following BibTeX:

```bash
@software{Philipp_Schmid_EasyLLM_2023,
author = {Philipp Schmid},
license = {Apache-2.0},
month = juj,
title = {EasyLLM: Streamlined Tools for LLMs},
url = {https://github.com/philschmid/easyllm},
year = {2023}
}
```
