import requests
from bs4 import BeautifulSoup


def scrape_movie_data(url):
    """
    Scrape movie data from the given URL.

    Args:
    - url (str): The URL of the webpage to scrape.

    Returns:
    - list: A list of tuples containing movie titles and image URLs.
    """
    # Fetch the HTML content of the webpage
    response = requests.get(url)
    html_content = response.content

    # Parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all div elements with class="boxed film"
    film_divs = soup.find_all("div", class_="boxed film")

    # List to store the extracted data
    movie_data = []

    # Extract required information from each div element
    for div in film_divs:
        # Extract movie title and image URL
        title = (
            div.find("p").text.strip().replace("Movie Watch Online Free", "").strip()
        )
        img_url = div.find("img")["src"]

        # Append the extracted data to the list
        movie_data.append((title, img_url))
    return movie_data


# Example usage:
if __name__ == "__main__":
    url = "https://ww2.5movierulz.beer/quality/hdrip/"
    movie_data = scrape_movie_data(url)
    print(movie_data)
