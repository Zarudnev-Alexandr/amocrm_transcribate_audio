# Добавление примечание к сделке в AmoCRM
import httpx
import requests
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import ProcessedNotes
from utils.get_grom_db import get_settings_string


async def add_note_to_deal(deal_id, text):
    try:
        settings_string = await get_settings_string()
        url = f'{settings_string.amo_crm_link}/api/v4/leads/{deal_id}/notes'
        headers = {
            'Authorization': f'Bearer {settings_string.amo_crm_token}',
            'Content-Type': 'application/json'
        }
        data = [{"note_type": "common", "params": {"text": text}}]

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)

        if response.status_code != 200:
            print(f"❌ Ошибка при добавлении примечания: {response.status_code} - {response.text}", flush=True)
            return False
        else:
            print("✅ Примечание успешно добавлено", flush=True)
            return True

    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP-ошибка при добавлении примечания: {e}", flush=True)
        return False
    except httpx.RequestError as e:
        print(f"❌ Ошибка сети при добавлении примечания: {e}", flush=True)
        return False
    except Exception as e:
        print(f"❌ Неизвестная ошибка при добавлении примечания: {e}", flush=True)
        return False


async def is_note_processed(db: AsyncSession, note_id: str) -> bool:
    query = select(ProcessedNotes).where(ProcessedNotes.note_id == note_id)
    result = await db.execute(query)
    return result.scalar_one_or_none() is not None


async def save_processed_note(db: AsyncSession, note_id: str):
    note = ProcessedNotes(note_id=note_id)
    db.add(note)
    await db.commit()