from aiogram import Router, F
from aiogram.types import Message


router = Router()


@router.message(F.text == "Statistics 📊")
async def statistics_plug(message: Message) -> None:
    await message.answer("Statistics block is in development. Gonna be ready approximately in the end of 2023")
