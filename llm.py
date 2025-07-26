from google import genai
from dotenv import load_dotenv
from google.genai.errors import ServerError
import asyncio
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MAX_HISTORY = 3

client = genai.Client(api_key=GEMINI_API_KEY)

async def generate_scene_with_retry(prompt, retries=3, delay=2):
    for attempt in range(1, retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt,
            )
            return response
        except ServerError as e:
            if "503" in str(e) and attempt < retries:
                await asyncio.sleep(delay)
                continue
            raise


async def generate_scene(history):
    prompt = f"""
        Вы — генератор интерактивной истории в стиле квеста.  
        Пользователь выбирает, что делать дальше.  
        На основе предыдущей истории предложите продолжение и варианты выбора.  
        Начните сегмент истории естественным образом, как будто это часть повествования.  
        Не повторяйте то, что уже произошло, если это не необходимо для сюжета.  
        Сделайте историю яркой и увлекательной.

        {"Summarized story so far:\n" + "\n".join(history) if history else "Start of the story."}

        Затем:
        Сгенерируйте одну сцену (4–10 предложений) и предложите 3 варианта действий для пользователя.  
        Каждый вариант должен быть на отдельной строке, начинаться с тире '-'.  
        Каждый вариант должен быть не длиннее 48 символов. Делай всё с жёстким горячим гейским уклоном

        Формат ответа:
        <СЦЕНА>  
        - вариант 1  
        - вариант 2  
        - вариант 3
        """

    response = await generate_scene_with_retry(prompt)

    full_text = response.text.strip()
    lines = full_text.splitlines()

    scene = lines[0]
    options = [line[2:].strip() for line in lines[1:] if line.startswith("-")]

    return scene, options

async def summarize_history(history):
    if not history:
        return ""

    prompt = (
        "Ты — помощник, который умеет сжимать сюжетные истории.\n"
        "Дана история квеста — перечень последовательных сцен и выборов игрока.\n"
        "Сформулируй краткую сводку сюжета (2-4 предложения), сохранив основные события и логическую последовательность.\n\n"
        "История:\n"
        + "\n".join(history) +
        "\n\nСводка:"
    )

    response = await generate_scene_with_retry(prompt)

    return response.text.strip()
