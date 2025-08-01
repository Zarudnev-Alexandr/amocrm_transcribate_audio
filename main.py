import json
import os

from fastapi import FastAPI, Request

from utils.added_funcs import add_note_to_deal
from utils.find_funcs import find_lead_id
from utils.generate_funcs import transcribe_to_dialog
from utils.get_funcs import download_audio_async

app = FastAPI()

@app.post("/webhooks/voice")
async def voice_webhook(request: Request):
    form_data = await request.form()

    if "leads[note][0][note][note_type]" in form_data:
        lead_id = find_lead_id(form_data)
        print('✅✅✅', lead_id, flush=True)
        note_type = form_data["leads[note][0][note][note_type]"]
        #10 - входящий, 11 - исходящий
        if note_type in ["10", "11"]:
            print('📞Данные от AMOCrm (звонки)', form_data, flush=True)
            text = form_data["leads[note][0][note][text]"]
            try:
                text_data = json.loads(text)
                audio_url = text_data.get("LINK")
                if audio_url:
                    # Скачивание аудиофайла асинхронно
                    output_path = "downloaded_call.mp3"
                    if await download_audio_async(audio_url, output_path):
                        # Транскрипция и саммари
                        dialog_text, summary = await transcribe_to_dialog(output_path)
                        dialog_text = "Расшифрованный текст диалога\n" + dialog_text
                        summary = "Краткая выжимка из диалога\n" + summary

                        print('💀💀💀', dialog_text, summary, flush=True)
                        await add_note_to_deal(lead_id, dialog_text)
                        await add_note_to_deal(lead_id, summary)
                        # Удаление временного файла
                        if os.path.exists(output_path):
                            os.remove(output_path)
                            print(f"Временный файл удален: {output_path}")
            except json.JSONDecodeError:
                print("Ошибка: Не удалось распарсить JSON в поле text")
            except Exception as e:
                print(f"Ошибка при обработке звонка: {e}")







