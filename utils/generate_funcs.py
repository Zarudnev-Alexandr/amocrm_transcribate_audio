from openai import OpenAI
import requests

from utils.get_grom_db import get_settings_string

async def generate_gpt_response(history):
    settings_string = await get_settings_string()

    openai_client = OpenAI(api_key=settings_string.gpt_token)
    gpt_prompt = f"{settings_string.gpt_prompt} {history}"
    messages = [
        {"role": "system", "content": gpt_prompt}
    ]
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌Ошибка при генерации ответа GPT: {e}")
        return "⌛Извините, я не могу ответить прямо сейчас. GPT не доступен в этом регионе."


async def transcribe_to_dialog(file_path):
    settings_string = await get_settings_string()

    url = "https://api.lemonfox.ai/v1/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {settings_string.whisper_ai_token}"
    }
    files = {"file": open(file_path, "rb")}
    data = {
        "language": "russian",
        "response_format": "verbose_json",
        "speaker_labels": True,
    }

    try:
        response = requests.post(url, headers=headers, files=files, data=data)
        response.raise_for_status()
        result = response.json()

        # Извлечение сегментов
        segments = result.get("segments", [])

        print("=== Диалог ===")
        all_text = ''
        for segment in segments:
            speaker = "Собеседник 1" if segment["speaker"] == "SPEAKER_00" else "Собеседник 2"
            text = segment["text"]
            all_text += f"{speaker}: {text}\n"
            # print(f"{speaker}: {text}")

        # print(generate_gpt_response(all_text))
        return all_text, await generate_gpt_response(all_text)

    except requests.exceptions.HTTPError as e:
        print("HTTP Ошибка:", e)
        print("Ответ сервера:", response.text)
    except requests.exceptions.RequestException as e:
        print("Ошибка:", e)
    except FileNotFoundError:
        print("Ошибка: Файл не найден. Проверьте путь к файлу.")