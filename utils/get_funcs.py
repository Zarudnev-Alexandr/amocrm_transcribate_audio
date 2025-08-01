import aiohttp

async def download_audio_async(url, output_path):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                with open(output_path, "wb") as f:
                    async for chunk in response.content.iter_chunked(8192):
                        if chunk:
                            f.write(chunk)
        print(f"Аудиофайл успешно скачан: {output_path}")
        return True
    except Exception as e:
        print(f"Ошибка при скачивании аудиофайла: {e}")
        return False