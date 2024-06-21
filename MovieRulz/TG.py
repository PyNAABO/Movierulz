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


def send_photos(bot_token, chat_id, photo_paths, caption=None):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"

    files = {}
    for idx, photo_path in enumerate(photo_paths, start=1):
        files[f"photo{idx}"] = open(photo_path, "rb")

    data = {"chat_id": chat_id}
    if caption:
        data["caption"] = caption

    response = requests.post(url, files=files, data=data)
    return response.json()
