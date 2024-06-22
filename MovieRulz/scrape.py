import requests
from bs4 import BeautifulSoup


def scrape_movie_data(url):
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
        # Extract movie title
        title = (
            div.find("p").text.strip().replace("Movie Watch Online Free", "").strip()
        )

        # Extract image URL
        img_url = div.find("img")["src"]

        # Extract link URL
        link_url = div.find("a")["href"]

        # Append the extracted data to the list
        movie_data.append((title, img_url, link_url))

    return movie_data


# Example usage:
if __name__ == "__main__":
    url = "https://ww2.5movierulz.beer/quality/hdrip/"
    movie_data = scrape_movie_data(url)
    print(movie_data)
