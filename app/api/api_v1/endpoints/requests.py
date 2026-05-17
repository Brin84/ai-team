from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.base import get_session
from app.db.models import Request, RequestStatus
from app.services.request_service import RequestService
from pydantic import BaseModel

router = APIRouter(prefix="/requests", tags=["requests"])


class RequestCreate(BaseModel):
    telegram_id: int
    description: str
    username: str | None = None
    full_name: str | None = None


class RequestRead(BaseModel):
    id: int
    user_id: int
    description: str
    status: RequestStatus

    class Config:
        orm_mode = True


class RequestUpdateStatus(BaseModel):
    status: RequestStatus


@router.post("/", response_model=RequestRead)
async def create_request(request_in: RequestCreate, session: AsyncSession = Depends(get_session)):
    request = await RequestService.create_request(
        session,
        telegram_id=request_in.telegram_id,
        description=request_in.description,
        username=request_in.username,
        full_name=request_in.full_name,
    )
    return request


@router.get("/{request_id}", response_model=RequestRead)
async def get_request(request_id: int, session: AsyncSession = Depends(get_session)):
    request = await RequestService.get_request(session, request_id)
    if not request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    return request


@router.get("/", response_model=List[RequestRead])
async def list_requests(status: RequestStatus | None = None, session: AsyncSession = Depends(get_session)):
    requests = await RequestService.list_requests(session, status)
    return requests


@router.patch("/{request_id}/status", response_model=RequestRead)
async def update_request_status(request_id: int, status_in: RequestUpdateStatus, session: AsyncSession = Depends(get_session)):
    request = await RequestService.update_status(session, request_id, status_in.status)
    if not request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    return request