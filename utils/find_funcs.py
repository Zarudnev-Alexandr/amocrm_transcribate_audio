# Получение id сделки из данных AmoCRM
import re


def find_lead_id(form_data):
    form_data_str = str(form_data)
    pattern = r"\('leads\[note\]\[0\]\[note\]\[element_id\]',\s*'(\d+)'\)"
    match = re.search(pattern, form_data_str)
    print("🥴 Функция нашла", match.group(1) if match else None)
    return match.group(1) if match else None