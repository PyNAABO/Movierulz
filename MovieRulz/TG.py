import requests


def send_message(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {"chat_id": chat_id, "text": text}
    response = requests.get(url, params=params)
    return response.json()


def send_photo_from_link(bot_token, chat_id, photo_link, caption=None):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    params = {"chat_id": chat_id, "photo": photo_link}
    if caption:
        params["caption"] = caption
    response = requests.get(url, params=params)
    return response.json()
