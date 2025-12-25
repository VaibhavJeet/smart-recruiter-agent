"""LLM provider configuration and factory."""

from functools import lru_cache
from langchain_core.language_models import BaseChatModel
from app.core.config import settings


@lru_cache()
def get_llm() -> BaseChatModel:
    """Get configured LLM instance.

    Supports:
    - OpenAI (GPT-4, GPT-3.5)
    - Anthropic (Claude)
    - Ollama (Local models)
    - LlamaCpp (Local GGUF models)
    """
    provider = settings.llm_provider.lower()

    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            temperature=0.7,
        )

    elif provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            api_key=settings.anthropic_api_key,
            model=settings.anthropic_model,
            temperature=0.7,
        )

    elif provider == "ollama":
        from langchain_community.chat_models import ChatOllama
        return ChatOllama(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
            temperature=0.7,
        )

    elif provider == "llamacpp":
        from langchain_community.chat_models import ChatLlamaCpp
        return ChatLlamaCpp(
            model_path=settings.llamacpp_model_path,
            n_ctx=settings.llamacpp_n_ctx,
            temperature=0.7,
        )

    raise ValueError(f"Unknown LLM provider: {provider}")


def get_embedding_model():
    """Get embedding model for vector operations."""
    provider = settings.llm_provider.lower()

    if provider in ["openai", "llamacpp"]:
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(api_key=settings.openai_api_key)

    elif provider == "ollama":
        from langchain_community.embeddings import OllamaEmbeddings
        return OllamaEmbeddings(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
        )

    from langchain_openai import OpenAIEmbeddings
    return OpenAIEmbeddings(api_key=settings.openai_api_key)