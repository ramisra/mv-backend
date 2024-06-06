from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from core.api.v1.endpoints import users, jobs, file

MAIN_ROUTER = APIRouter()


@MAIN_ROUTER.get("/rate_limit", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
def test_rate_limit():
    return {"Hello": "This is a  rate limited endpoint!"}

#
MAIN_ROUTER.include_router(users.router, prefix="", tags=["User"])
# MAIN_ROUTER.include_router(auth.router, prefix="", tags=["Auth"])
# MAIN_ROUTER.include_router(actions.router, prefix="", tags=["Action"])
MAIN_ROUTER.include_router(jobs.router, prefix="", tags=["Job"])
MAIN_ROUTER.include_router(file.router, prefix="", tags=["File"])
# MAIN_ROUTER.include_router(realtime.router, prefix="", tags=["Realtime"])
