import os
import subprocess
from MovieRulz.get_SS import get_driver
from MovieRulz.get_LL import get_latest_link
from MovieRulz.scrape import scrape_movie_data
from MovieRulz.movie_details import get_movie_details_TMDB
from MovieRulz.TG import (
    send_message,
    send_photo_from_link,
    send_photo_from_links,
)
from MovieRulz.utils import read_data, read_movie_data, write_movie_data


def git_commit_and_push():
    try:
        # Configure Git user if not already configured
        subprocess.run(
            ["git", "config", "--global", "user.name", "github-actions[bot]"]
        )
        subprocess.run(
            [
                "git",
                "config",
                "--global",
                "user.email",
                "41898282+github-actions[bot]@users.noreply.github.com",
            ]
        )

        # Add changes to the index
        subprocess.run(["git", "add", "-A"])

        # Check if there are any changes to commit
        status = subprocess.run(["git", "diff-index", "--quiet", "HEAD"])
        if status.returncode != 0:
            # Commit changes with a meaningful message
            subprocess.run(["git", "commit", "-m", "Commit message describing changes"])

            # Pull latest changes from remote (optional, if needed)
            subprocess.run(["git", "pull", "origin", "main"])

            # Push changes to the remote repository
            subprocess.run(["git", "push", "origin", "main"])
        else:
            print("No changes to commit.")

    except subprocess.CalledProcessError as e:
        print(f"Error executing Git command: {e}")


bot_token = os.environ["BOT_TOKEN"]
chat_id = "976223233"


def main():
    driver = get_driver()
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
                MovieDetails = get_movie_details_TMDB(
                    MovieName, MovieLink, driver
                ).strip()
                git_commit_and_push()
                try:
                    # send_photos(
                    #     bot_token=bot_token,
                    #     chat_id=chat_id,
                    #     photo_link=data[n][1],
                    #     local_photo_path="./Data/IMDB_Screenshot.png",
                    #     captions=[MovieDetails],
                    # )
                    send_photo_from_links(
                        bot_token=bot_token,
                        chat_id=chat_id,
                        photo_links=[
                            data[n][1],
                            "https://raw.githubusercontent.com/PyNAABO/Movierulz/main/Data/IMDB_Screenshot.png",
                        ],
                        captions=[MovieDetails],
                    )
                except Exception as e:
                    print("ERROR:", e)
                    send_photo_from_link(
                        bot_token=bot_token,
                        chat_id=chat_id,
                        photo_link=data[n][1],
                        caption=MovieDetails,
                    )
                write_movie_data((data[n][0], data[n][1], data[n][2]))
    except Exception as e:
        send_message(bot_token, chat_id, text=f"🔴🔴 Error Occurred 🔴🔴:\n\n{e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
