from fastapi import APIRouter
from .users import router as users_router
from .auth import router as auth_router
from .codes import router as code_router
from .referrals import router as referral_router

router = APIRouter(prefix="/api-v1")
router.include_router(users_router, prefix="/users")
router.include_router(auth_router, prefix="/auth")
router.include_router(code_router, prefix="/codes")
router.include_router(referral_router, prefix="/referrals")
