from aiogram import Router
from .answer import router as answer_router
from .payment import router as payment_router
from .chat_payment import router as chat_payment_router

router = Router()

router.include_router(answer_router)
router.include_router(payment_router)
router.include_router(chat_payment_router)