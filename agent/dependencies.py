import asyncio
import os
from functools import cache

import boto3

from .agent import agent

_api_key_cache: str | None = None


async def get_openai_api_key() -> str:
    global _api_key_cache

    if _api_key_cache:
        return _api_key_cache

    if _api_key_cache := os.getenv("OPENAI_API_KEY"):
        return _api_key_cache

    def _fetch_from_ssm():
        ssm = boto3.client("ssm")
        response = ssm.get_parameter(Name="/langchain-agent/openai-api-key", WithDecryption=True)
        return response["Parameter"]["Value"]

    _api_key_cache = await asyncio.to_thread(_fetch_from_ssm)
    os.environ["OPENAI_API_KEY"] = _api_key_cache
    return _api_key_cache


@cache
def get_agent():
    table_name = os.getenv("CHECKPOINTS_TABLE_NAME")
    if not table_name:
        raise ValueError("CHECKPOINTS_TABLE_NAME environment variable not set")
    return agent(table_name)
