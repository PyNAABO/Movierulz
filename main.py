import os
from MovieRulz.get_LL import get_latest_link
from MovieRulz.scrape import scrape_movie_data
from MovieRulz.TG import send_message, send_photo_from_links
from MovieRulz.movie_details import get_movie_details_TMDB
from MovieRulz.utils import read_data, read_movie_data, write_movie_data

bot_token = os.environ["BOT_TOKEN"]
chat_id = "976223233"


def main():
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
                MovieName = data[n][0]

                # Refining name
                MovieName = f"{MovieName.rsplit(')')[0]})"

                # Getting Movie Details
                MovieLink = data[n][2]
                MovieDetails = get_movie_details_TMDB(MovieName, MovieLink).strip()
                send_photo_from_links(
                    bot_token=bot_token,
                    chat_id=chat_id,
                    photo_links=[data[n][1]],
                    caption=MovieDetails,
                )
                write_movie_data((data[n][0], data[n][1], data[n][2]))
    except Exception as e:
        send_message(bot_token, chat_id, text=f"🔴🔴 Error Occurred 🔴🔴:\n\n{e}")


if __name__ == "__main__":
    main()
