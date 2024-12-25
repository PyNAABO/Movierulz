import os
import logging
from MovieRulz.get_LL import get_latest_link
from MovieRulz.scrape import scrape_movie_data
from MovieRulz.movie_details import get_movie_details_TMDB
from MovieRulz.get_SS import get_driver, save_image_from_url
from MovieRulz.TG import send_message, send_photos, send_photo_from_link
from MovieRulz.utils import read_data, read_movie_data, write_movie_data

# Configure logging
logging.basicConfig(
    filename="logs_main.txt",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

bot_token = os.environ["BOT_TOKEN"]
chat_id = "976223233"


def maintain_data_limit():
    data = read_movie_data()
    if len(data) > 25:
        data.pop()
        write_movie_data(data)


def main():
    try:
        logging.info("Starting main function")
        driver = get_driver()
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
                MovieName = data[n][0]

                # Refining name
                MovieName = f"{MovieName.rsplit(')')[0]})"

                # Getting Movie Details
                MovieLink = data[n][2]
                MovieImageLink = data[n][1]
                MovieDetails = get_movie_details_TMDB(
                    MovieName, MovieLink, driver
                ).strip()
                if MovieDetails != "Adult":
                    save_image_from_url(url=MovieImageLink)
                    try:
                        resp = send_photos(
                            bot_token=bot_token,
                            chat_id=chat_id,
                            images=[
                                "./Data/Poster.jpg",
                                "./Data/IMDB_Screenshot.png",
                            ],
                            caption=MovieDetails,
                        )
                        if resp["ok"]:
                            logging.info(f"Done ✅ - {MovieName}")
                        else:
                            logging.error(
                                f"Sending Local Images to Telegram Failed!! {resp}"
                            )
                            raise Exception(
                                "🔴 Sending Local Images to Telegram Failed!! 🔴"
                            )
                    except Exception as e:
                        logging.error(f"Error Occurred: {e}")
                        send_message(
                            bot_token, chat_id, text=f"🔴🔴 Error Occurred 🔴🔴:\n\n{e}"
                        )
                        send_photo_from_link(
                            bot_token=bot_token,
                            chat_id=chat_id,
                            photo_link=MovieImageLink,
                            caption=MovieDetails,
                        )
                    write_movie_data((data[n][0], data[n][1], data[n][2]))
    except Exception as e:
        logging.error(f"Exception in main: {e}")
        send_message(bot_token, chat_id, text=f"🔴🔴 Error Occurred 🔴🔴:\n\n{e}")
    finally:
        driver.quit()
        logging.info("Driver quit successfully")
    with open("logs_main.txt", "r") as f:
        logs = f.read()
        print(logs)


if __name__ == "__main__":
    main()
