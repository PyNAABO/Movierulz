import requests
from lxml import html
from bs4 import BeautifulSoup
from MovieRulz.get_SS import get_IMDB_Screenshot


def get_details_from_site(url):
    # Headers to mimic a real browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }

    # Sending a GET request to the webpage
    response = requests.get(url, headers=headers)

    # Checking if the request was successful
    if response.status_code == 200:
        # Parsing the HTML content
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")

        # Extracting the text from the specified <p> tags
        p2_tag = soup.select_one("#post > div:nth-of-type(2) > p:nth-of-type(2)")
        if p2_tag:
            # Formatting the extracted content
            content = p2_tag.get_text(separator="\n", strip=True)
            lines = content.split("\n")

            # Formatting lines to be in a single line with correct commas
            formatted_lines = []
            for line in lines:
                if line.endswith(":"):
                    formatted_lines.append(line)
                else:
                    formatted_lines[-1] += " " + line.strip()

            p2_text = "\n".join(formatted_lines)
        else:
            p2_text = "Specified <p> tag not found"

        p3_text = soup.select_one(
            "#post > div:nth-of-type(2) > p:nth-of-type(3)"
        ).get_text(strip=True)

        # Printing the extracted text
        movie_info_from_site = f"{p2_text}\n\nOverview: {p3_text}"
        return movie_info_from_site.strip()
    else:
        return "Error fetching the HTML content"


def get_IMDB_link(query):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }
        params = {
            "q": f"{str(query)} IMDB",
        }
        response = requests.get(
            "https://www.google.com/search", params=params, headers=headers
        )

        tree = html.fromstring(response.content)

        Links = []
        elements = tree.xpath('//div[@class="yuRUbf"]/div/span/a')[:5]
        for element in elements:
            link = element.get("href").strip()
            if "imdb" in link:
                Links.append(link)

        link = Links[0] if Links else None
        return link
    except Exception as e:
        print("Error fetching latest link:", e)
        return None


# Function to get movie details by name
def get_movie_details_TMDB(query, url, driver):
    # Initialize movie details variable
    movie_details_TMDB = ""

    movie_details_TMDB += f"{query}\n\n"
    IMDBLink = get_IMDB_link(query)
    movie_details_TMDB += f"IMDB Link: {IMDBLink}\n\n"

    # Grabing SS from IMDB
    get_IMDB_Screenshot(driver=driver, link=IMDBLink)
    movie_details_TMDB += get_details_from_site(url)
    return movie_details_TMDB
