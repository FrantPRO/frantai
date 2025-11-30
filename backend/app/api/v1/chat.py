"""
Chat API endpoints with streaming support.
"""

import json
import logging
import time
from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.rate_limit import get_rate_limiter, hash_ip
from app.models.chat import ChatMessage, ChatSession
from app.schemas.chat import ChatMessageRequest, SessionResponse
from app.services.rag import get_rag_service

logger = logging.getLogger(__name__)
router = APIRouter()
limiter = get_rate_limiter()


@router.post("/message")
@limiter.limit("25/minute")
@limiter.limit("100/hour")
async def chat_message(
    request: Request,
    chat_request: ChatMessageRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Send a chat message and get streaming response.

    Returns Server-Sent Events (SSE) stream.
    """
    start_time = time.time()

    # Validate message
    if not chat_request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty",
        )

    # Get or create session
    session_id = chat_request.session_id
    if not session_id:
        session_id = uuid4()
        session = ChatSession(
            id=session_id, ip_hash=hash_ip(request.client.host)
        )
        db.add(session)
        await db.commit()
        logger.info(f"Created new session: {session_id}")
    else:
        # Verify session exists
        result = await db.execute(
            select(ChatSession).where(ChatSession.id == session_id)
        )
        session = result.scalar_one_or_none()
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found",
            )

    # Log user message
    user_message = ChatMessage(
        session_id=session_id, role="user", content=chat_request.message
    )
    db.add(user_message)
    await db.commit()

    # Get RAG service
    rag_service = await get_rag_service(db)

    # Streaming response generator
    async def generate() -> AsyncGenerator[str, None]:
        try:
            # Send session_id first
            yield f"data: {json.dumps({'session_id': str(session_id)})}\n\n"

            # Detect language and retrieve chunks before streaming
            from app.services.text_utils import detect_language
            language = detect_language(chat_request.message)
            chunks = await rag_service.vector_search(
                query=chat_request.message, top_k=3
            )
            chunk_ids = [chunk.id for chunk in chunks] if chunks else []

            # Stream response from RAG
            full_response = ""
            async for token in rag_service.chat(
                question=chat_request.message, top_k=3, stream=True
            ):
                full_response += token
                yield f"data: {json.dumps({'token': token})}\n\n"

            # Send done signal
            response_time = int((time.time() - start_time) * 1000)
            done_data = {
                "done": True,
                "response_time_ms": response_time,
            }
            yield f"data: {json.dumps(done_data)}\n\n"

            # Log assistant message with metadata
            assistant_message = ChatMessage(
                session_id=session_id,
                role="assistant",
                content=full_response,
                response_time_ms=response_time,
                language_detected=language,
                retrieved_chunks=chunk_ids,
            )
            db.add(assistant_message)

            # Update session
            session.message_count += 2  # user + assistant
            session.last_message_at = datetime.now(UTC).replace(tzinfo=None)

            await db.commit()

            logger.info(
                f"Chat completed: session={session_id}, time={response_time}ms"
            )

        except Exception as e:
            logger.exception("Error in chat stream")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        },
    )


@router.post("/session/new")
async def create_session(
    request: Request, db: AsyncSession = Depends(get_db)
) -> SessionResponse:
    """Create a new chat session"""
    session_id = uuid4()
    session = ChatSession(id=session_id, ip_hash=hash_ip(request.client.host))
    db.add(session)
    await db.commit()

    return SessionResponse(
        session_id=session_id,
        message_count=0,
        first_message_at=session.first_message_at.isoformat(),
        last_message_at=session.last_message_at.isoformat(),
    )


@router.get("/session/{session_id}")
async def get_session(
    session_id: UUID, db: AsyncSession = Depends(get_db)
) -> SessionResponse:
    """Get session information"""
    result = await db.execute(
        select(ChatSession).where(ChatSession.id == session_id)
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        )

    return SessionResponse(
        session_id=session.id,
        message_count=session.message_count,
        first_message_at=session.first_message_at.isoformat(),
        last_message_at=session.last_message_at.isoformat(),
    )
