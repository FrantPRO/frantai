from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Database session dependency"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def verify_admin_access(x_admin_token: str = Header(None)) -> bool:
    """
    Verify admin access (placeholder for future implementation)
    For now, just check if header is present
    TODO: Implement proper authentication (JWT, API key, etc.)
    """
    # Placeholder: accept any token for development
    # In production, verify against secure token/JWT
    if not x_admin_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin access required",
        )

    # TODO: Implement real verification
    # For now, accept "dev-admin-token" for development
    if x_admin_token != "dev-admin-token":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid admin token"
        )

    return True
