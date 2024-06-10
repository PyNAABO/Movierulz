import os
from get_LL import get_latest_link
from scrape import scrape_movie_data
from TG import send_message, send_photo_from_link
from utils import read_data, read_movie_data, write_movie_data

bot_token = os.environ["BOT_TOKEN"]
chat_id = "976223233"


if __name__ == "__main__":
    try:
        MR_link = get_latest_link()
        if MR_link is None:
            MR_link = read_data()["link"]
        sent_data = read_movie_data()
        data = scrape_movie_data(url=MR_link)
        titles = [item[0] for item in data]
        sent_titles = [movie[0] for movie in sent_data]
        n = -1
        for title in titles:
            n += 1
            if title not in sent_titles:
                send_photo_from_link(
                    bot_token, chat_id, photo_link=data[n][1], caption=data[n][0]
                )
                write_movie_data((data[n][0], data[n][1]))
    except Exception as e:
        send_message(bot_token, chat_id, text=f"🔴🔴 Error Occured 🔴🔴:\n\n{e}")
