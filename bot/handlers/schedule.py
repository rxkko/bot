from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router
from bot.core.session import get_api_client
from bot.schemas.get_schedule import GetScheduleByGroup


router = Router()

@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer(f"Hello, {message.from_user.full_name}!")


@router.message()
async def handle_schedule(message: Message):
    await message.answer("🤔")

    group_name = message.text.strip().upper()

    request = GetScheduleByGroup(
        group=group_name
    )

    async with get_api_client() as api_client:
        schedule_dict = await api_client.get_schedule_by_group(request)

    if schedule_dict.get("error"):
        await message.answer(f"❌ Ошибка: {schedule_dict['error']}")
        return

    if not schedule_dict["schedule"]:
        await message.answer("📭 Расписание не найдено")
        return

    answer = f"📚 *{schedule_dict['group']}*\n"
    answer += f"📅 {schedule_dict['week']}\n\n"

    current_day = None
    for lesson in schedule_dict["schedule"]:
        if lesson["day"] != current_day:
            current_day = lesson["day"]
            answer += f"\n*{current_day}*\n"
        answer += f"⏰ {lesson['time']} — *{lesson['subject']}*\n"
        answer += f"   👨‍🏫 {lesson['teacher']} | 🏠 {lesson['room']}\n\n"

    await message.answer(answer, parse_mode="Markdown")