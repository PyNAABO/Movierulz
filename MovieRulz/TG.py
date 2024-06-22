import json
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


def send_photos(bot_token: str, chat_id: str, images: list, caption: str = None):
    """
    Sends a group of photos to a Telegram chat with an optional caption.

    :param bot_token: The token of the bot obtained from BotFather.
    :param chat_id: The unique identifier for the target chat or username of the target channel.
    :param images: A list of file paths of the images to be sent.
    :param caption: An optional caption for the images.
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMediaGroup"

    # Prepare the media group
    media_group = []
    files = {}
    for i, image in enumerate(images):
        files[f"photo{i}"] = open(image, "rb")
        media_item = {"type": "photo", "media": f"attach://photo{i}"}
        if i == 0 and caption:  # Add caption to the first image
            media_item["caption"] = caption
        media_group.append(media_item)

    payload = {
        "chat_id": chat_id,
        "media": json.dumps(media_group),  # JSON encode the media group
    }

    response = requests.post(url, data=payload, files=files)

    # Close the files after sending the request
    for f in files.values():
        f.close()

    return response.json()
