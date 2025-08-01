# Добавление примечание к сделке в AmoCRM
import requests

from utils.get_grom_db import get_settings_string


async def add_note_to_deal(deal_id, text):
    settings_string = await get_settings_string()

    url = f'{settings_string.amo_crm_link}/api/v4/leads/{deal_id}/notes'
    headers = {'Authorization': f'Bearer {settings_string.amo_crm_token}', 'Content-Type': 'application/json'}
    data = [{"note_type": "common", "params": {"text": text}}]
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print(f"❌Ошибка при добавлении примечания: {response.text}")
    else:
        print("✅Примечание успешно добавлено")