import json
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from langgraph.graph.state import CompiledStateGraph
from uuid import uuid4

from .dependencies import get_agent
from .schemas import ChatRequest, ChatResponse

router = APIRouter()


async def generate_stream(messages: list[dict], agent: CompiledStateGraph, conversation_id: str):
    yield f"data: {json.dumps({'conversation_id': conversation_id})}\n\n"
    async for token, metadata in agent.astream({"messages": messages}, {"configurable": {"thread_id": conversation_id}}, stream_mode="messages"):
        if not token.content_blocks: # pyrefly: ignore[missing-attribute]
            continue
        yield f"data: {json.dumps({'content': token.content_blocks})}\n\n"


@router.get("/healthz")
async def healthz():
    return {"status": "ok"}


@router.post("/chat")
async def chat(
    request: ChatRequest, agent: Annotated[CompiledStateGraph, Depends(get_agent)]
) -> ChatResponse:
    conversation_id = request.conversation_id or str(uuid4())
    messages = [{"role": "user", "content": request.message}]
    result = await agent.ainvoke({"messages": messages}, {"configurable": {"thread_id": conversation_id}})
    last_message = result["messages"][-1]
    return ChatResponse(
        conversation_id=conversation_id,
        role=last_message.type,
        content=last_message.content,
    )


@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest, agent: Annotated[CompiledStateGraph, Depends(get_agent)]
):
    conversation_id = request.conversation_id or str(uuid4())
    messages = [{"role": "user", "content": request.message}]
    return StreamingResponse(
        generate_stream(messages, agent, conversation_id), media_type="text/event-stream"
    )
