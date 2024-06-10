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


if __name__ == "__main__":
    bot_token = "1887448307:AAEdv0qimtjYu37oClMSuRQlBtRmZuryaTg"
    chat_id = "976223233"
    # Example usage
    message = "Hello, this is a test message from your bot!"
    photo_link = (
        "https://ww2.5movierulz.beer/uploads/Varshangalkku-Shesham-Malayalam.jpg"
    )
    caption = "Check out this image!"

    response_message = send_message(bot_token, chat_id, message)
    print("Message Response:", response_message)

    response_photo = send_photo_from_link(bot_token, chat_id, photo_link, caption)
    print("Photo Response:", response_photo)
