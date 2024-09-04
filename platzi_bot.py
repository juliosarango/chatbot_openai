import os
import time
import requests
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv

load_dotenv()

openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def get_updates(offset=None):
    telegram_url = os.environ.get("TELEGRAM_BOT_URL")
    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    url = f"{telegram_url}{telegram_token}/getUpdates"
    params = {
        "timeout": 100,
        "offset": offset,
    }

    try:
        response = requests.get(url=url, params=params)

        return response.json()["result"]
    except Exception as e:
        print(f"Error al obtener actualizaciones del bot de telegram: {e}")


def send_messages(chat_id, text):
    telegram_url = os.environ.get("TELEGRAM_BOT_URL")
    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    url = f"{telegram_url}{telegram_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": text,
    }
    try:

        response = requests.post(url=url, params=params)

        return response
    except Exception as e:
        print(f"Error al enviar actualizaciones del bot de telegram: {e}")


def get_openai_response(prompt):
    system = """Eres un asitente de atención a clientes y estudiantes de la 
    plataforma de educación en línea en tecnología, inglés y liderazgo llamado Platzi"""

    try:
        response = openai_client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL_FINE_TUNING"),
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
            n=1,
            temperature=0.5,
        )

        return response.choices[0].message.content.strip()
    except OpenAIError as e:
        print(f"La API de OpenAI devolvió un error: {e}")


def main():
    print("starting bot...")
    offset = 0
    while True:
        updates = get_updates(offset=offset)
        if updates:
            for update in updates:
                if "message" in update:
                    offset = update["update_id"] + 1
                    chat_id = update["message"]["chat"]["id"]
                    user_message = update["message"]["text"]
                    user_name = (
                        update["message"]["from"]["first_name"]
                        + " "
                        + update["message"]["from"]["last_name"]
                        + " - "
                        + update["message"]["from"]["username"]
                    )
                    print(f"Message received: {user_message} from: {user_name}")
                    gpt = get_openai_response(user_message)
                    send_messages(chat_id, gpt)
        else:
            time.sleep(1)


if __name__ == "__main__":
    main()
