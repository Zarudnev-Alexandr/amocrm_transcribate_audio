import json
import os
import gc

from fastapi import FastAPI, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.settings import get_db
from utils.added_funcs import add_note_to_deal, is_note_processed, save_processed_note
from utils.find_funcs import find_lead_id
from utils.generate_funcs import transcribe_to_dialog
from utils.get_funcs import download_audio_async

app = FastAPI()

@app.post("/webhooks/voice")
async def voice_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    form_data = await request.form()

    if "leads[note][0][note][note_type]" in form_data:
        lead_id = find_lead_id(form_data)
        print('✅✅✅', lead_id, flush=True)
        note_type = form_data["leads[note][0][note][note_type]"]
        note_id = form_data["leads[note][0][note][id]"]

        # Проверяем, не был ли звонок уже обработан
        if await is_note_processed(db, note_id):
            print(f"⏩ Пропуск: звонок с note_id={note_id} уже обработан", flush=True)
            return {"status": "skipped", "message": "Note already processed"}

        if note_type in ["10", "11"]:
            print('📞 Данные от AMOCrm (звонки)', form_data, flush=True)
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
                        # Добавляем примечания
                        if len(dialog_text) < 19900:#amocrm не хавает больше 20000 символов в примечании
                            if await add_note_to_deal(lead_id, dialog_text) and await add_note_to_deal(lead_id, summary):
                                # Сохраняем note_id как обработанный
                                await save_processed_note(db, note_id)
                            else:
                                print(f"❌ Не удалось добавить примечания для note_id={note_id}", flush=True)
                        else:
                            if await add_note_to_deal(lead_id, summary):
                                # Сохраняем note_id как обработанный
                                await save_processed_note(db, note_id)
                            else:
                                print(f"❌ Не удалось добавить примечания для note_id={note_id}", flush=True)

                        # Удаление временного файла
                        if os.path.exists(output_path):
                            os.remove(output_path)
                            gc.collect()
                            print(f"Временный файл удален: {output_path} и память очищена", flush=True)
            except json.JSONDecodeError:
                print("❌ Ошибка: Не удалось распарсить JSON в поле text", flush=True)
            except Exception as e:
                print(f"❌ Ошибка при обработке звонка: {e}", flush=True)

    return {"status": "ok"}







