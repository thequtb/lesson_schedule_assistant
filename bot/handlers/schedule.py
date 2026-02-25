import asyncio
import os
from typing import Optional
from urllib.parse import quote

import aiohttp
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

API_URL = os.environ.get('API_URL', 'http://127.0.0.1:8000')


async def fetch_today_schedule(tg_login: str) -> Optional[dict]:
    """Fetch today's schedule from API. Returns None on error."""
    url = f"{API_URL.rstrip('/')}/api/schedule/?tg_login={quote(tg_login)}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 404:
                    return {'error': 'not_found'}
                if resp.status != 200:
                    return {'error': 'api_error'}
                return await resp.json()
    except (aiohttp.ClientError, asyncio.TimeoutError):
        return {'error': 'unavailable'}


def format_schedule(data: dict) -> str:
    if 'error' in data:
        if data['error'] == 'not_found':
            return '❌ Вы не зарегистрированы в системе. Обратитесь к администратору.'
        if data['error'] == 'unavailable':
            return '❌ Сервис временно недоступен. Попробуйте позже.'
        return '❌ Произошла ошибка.'

    date_str = data.get('date', '')
    group = data.get('group', '')
    lessons = data.get('lessons', [])

    lines = [f'📅 Расписание на {date_str} (группа {group})\n']
    if not lessons:
        lines.append('Нет уроков на сегодня.')
    else:
        for l in lessons:
            lines.append(f"{l['order']}. {l['subject']} — каб. {l['room']}")
    return '\n'.join(lines)


@router.message(Command('today'))
async def cmd_today(message: Message):
    """Handle /today command — show today's schedule."""
    tg_login = (message.from_user.username or '').strip() if message.from_user else ''
    if not tg_login:
        await message.answer('❌ Укажите username в настройках Telegram (Settings → Username).')
        return
    data = await fetch_today_schedule(tg_login)
    text = format_schedule(data)
    await message.answer(text)
