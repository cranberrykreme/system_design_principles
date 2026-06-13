from fastapi import APIRouter, Depends
from api.deps import get_rate_limiter

router = APIRouter()

@router.get('/make-request')
async def make_request(user_id: str, limiter = Depends(get_rate_limiter)):
    allowed = await limiter.allow_request(user_id)

    return {
        "user_id": user_id,
        "allowed": allowed
    }