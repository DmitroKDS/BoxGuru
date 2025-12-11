from aiogram import Router
from .category import router as category_router

router = Router()

router.include_router(category_router)