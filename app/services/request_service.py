from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Request, User, RequestStatus
from typing import Optional, List


class RequestService:
    @staticmethod
    async def create_request(
        session: AsyncSession, telegram_id: int, description: str, username: Optional[str] = None, full_name: Optional[str] = None
    ) -> Request:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalars().first()
        if not user:
            user = User(telegram_id=telegram_id, username=username, full_name=full_name)
            session.add(user)
            await session.flush()  # to get user.id
        request = Request(user_id=user.id, description=description)
        session.add(request)
        await session.commit()
        await session.refresh(request)
        return request

    @staticmethod
    async def get_request(session: AsyncSession, request_id: int) -> Optional[Request]:
        result = await session.execute(select(Request).where(Request.id == request_id))
        return result.scalars().first()

    @staticmethod
    async def list_requests(session: AsyncSession, status: Optional[RequestStatus] = None) -> List[Request]:
        query = select(Request)
        if status:
            query = query.where(Request.status == status)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def update_status(session: AsyncSession, request_id: int, status: RequestStatus) -> Optional[Request]:
        request = await RequestService.get_request(session, request_id)
        if request:
            request.status = status
            await session.commit()
            await session.refresh(request)
        return request