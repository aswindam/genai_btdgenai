"""Central LLM access layer.

All model calls in this project go through here so that the provider can be
swapped in a single place.  The backend is an Azure AI Foundry deployment that
is accessed through the official Anthropic SDK (``AnthropicFoundry``).

Configuration is read from environment variables or Streamlit secrets:

    AZURE_FOUNDRY_API_KEY   - API key of the Foundry project (required)
    AZURE_FOUNDRY_ENDPOINT  - Anthropic route of the project endpoint, e.g.
                              https://<name>.services.ai.azure.com/anthropic
                              (a trailing "/v1" is accepted and stripped, since
                              the SDK appends the version segment itself)
    AZURE_FOUNDRY_MODEL     - deployment name, e.g. claude-opus-5

The key can be supplied through an environment variable or Streamlit secrets.
"""

import base64
import io
import os

from anthropic import AnthropicFoundry

DEFAULT_ENDPOINT = "https://finder-ai-dev.services.ai.azure.com/anthropic"
DEFAULT_MODEL = "claude-opus-5"
DEFAULT_MAX_TOKENS = 4096

# Deployment specific options that the SDK has no typed parameter for; they are
# passed straight through in the request body.
EXTRA_BODY = {
    "thinking": {"type": "adaptive"},
    "output_config": {"effort": "medium"},
}

_client = None


def _setting(name, default=None):
    value = os.getenv(name)
    if value:
        return value
    try:
        import streamlit as st
        value = st.secrets.get(name)
        if value:
            return str(value)
    except Exception:
        # Streamlit secrets are unavailable when running outside Streamlit.
        pass
    return default


def _api_key():
    key = _setting("AZURE_FOUNDRY_API_KEY")
    if key:
        return key

    raise RuntimeError(
        "No Azure Foundry API key found. Set AZURE_FOUNDRY_API_KEY in the "
        "environment or Streamlit secrets."
    )


def get_endpoint():
    endpoint = _setting("AZURE_FOUNDRY_ENDPOINT", DEFAULT_ENDPOINT).rstrip("/")
    # The Anthropic SDK appends "/v1/..." to the base URL, so an endpoint that
    # already carries the version segment would resolve to "/v1/v1/messages".
    if endpoint.endswith("/v1"):
        endpoint = endpoint[: -len("/v1")]
    return endpoint


def get_model():
    return _setting("AZURE_FOUNDRY_MODEL", DEFAULT_MODEL)


def get_client():
    """Return a lazily created, cached Foundry client."""
    global _client
    if _client is None:
        _client = AnthropicFoundry(api_key=_api_key(), base_url=get_endpoint())
    return _client


def _image_block(image):
    """Convert a PIL image / raw bytes into an Anthropic image content block."""
    if isinstance(image, (bytes, bytearray)):
        data = bytes(image)
    else:  # PIL.Image
        buffer = io.BytesIO()
        image.convert("RGB").save(buffer, format="PNG")
        data = buffer.getvalue()

    return {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": "image/png",
            "data": base64.b64encode(data).decode(),
        },
    }


def _user_message(text, image=None):
    content = []
    if image is not None:
        content.append(_image_block(image))

    # The API rejects empty text blocks, so only send one when there is text.
    text = (text or "").strip()
    if text:
        content.append({"type": "text", "text": text})
    elif not content:
        raise ValueError("Cannot send an empty message: provide text, an image, or both.")

    return {"role": "user", "content": content}


def generate(prompt, system=None, image=None, max_tokens=DEFAULT_MAX_TOKENS):
    """Single-turn completion. Returns the response text.

    Either ``prompt`` or ``image`` (or both) must be supplied.
    """
    response = get_client().messages.create(
        model=get_model(),
        max_tokens=max_tokens,
        system=system or "",
        messages=[_user_message(prompt, image)],
        extra_body=EXTRA_BODY,
    )
    return "".join(block.text for block in response.content if block.type == "text")


def chat(messages, system=None, max_tokens=DEFAULT_MAX_TOKENS):
    """Multi-turn completion.

    ``messages`` is a list of ``{"role": "user"|"assistant", "content": str}``.
    Returns the assistant reply as text.
    """
    response = get_client().messages.create(
        model=get_model(),
        max_tokens=max_tokens,
        system=system or "",
        messages=messages,
        extra_body=EXTRA_BODY,
    )
    return "".join(block.text for block in response.content if block.type == "text")


def stream_chat(messages, system=None, max_tokens=DEFAULT_MAX_TOKENS):
    """Multi-turn completion that yields text chunks as they arrive."""
    with get_client().messages.stream(
        model=get_model(),
        max_tokens=max_tokens,
        system=system or "",
        messages=messages,
        extra_body=EXTRA_BODY,
    ) as stream:
        for text in stream.text_stream:
            yield text
