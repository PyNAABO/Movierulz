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
        print(link)
        return link
    except Exception as e:
        print("Error fetching latest link:", e)
        return None


# Function to handle missing data gracefully
def get_safe_value(data, key):
    return data[key] if key in data and data[key] is not None else "N/A"


# Function to convert minutes to hours and minutes format
def convert_to_hours(minutes):
    if minutes is not None and minutes != "N/A":
        hours = minutes // 60
        remainder_minutes = minutes % 60
        return f"{hours} hours {remainder_minutes} minutes"
    else:
        return "N/A"


# Function to get movie details by name
def get_movie_details_TMDB(query, url, driver):
    # TMDb API endpoints and authentication headers
    search_url = "https://api.themoviedb.org/3/search/movie"
    movie_url = "https://api.themoviedb.org/3/movie/{}"

    movie_name = query.split("(")[0].strip()
    search_params = {
        "query": movie_name,
        "include_adult": "true",
        "language": "en-US",
        "page": 1,
    }
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjNzE0ZTQzZmQ5YzBmZTllYmNmZWIwNWQxNTc0YmVhNyIsInN1YiI6IjY1NjE5MzZhN2RmZGE2NTkyZjUzMjU1ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.yDKG1HImCfyRvtZH5xz-kxw5vJ1_GeoGmkDrpvjnedI",
    }

    # Step 1: Search for the movie by name
    response = requests.get(search_url, params=search_params, headers=headers)

    # Initialize movie details variable
    movie_details_TMDB = ""
    movie_details_TMDB += f"{query}\n\n"
    IMDBLink = get_IMDB_link(query)

    # Check if search request was successful
    if response.status_code == 200:
        search_results = response.json()
        if search_results["total_results"] > 0:
            movie_id = search_results["results"][0]["id"]

            # Step 2: Retrieve detailed information about the movie using its ID
            movie_response = requests.get(
                movie_url.format(movie_id),
                params={"language": "en-US"},
                headers=headers,
            )

            # Check if movie details request was successful
            if movie_response.status_code == 200:
                movie_details = movie_response.json()

                # Format movie details into a string
                from_TMDB = f"https://www.imdb.com/title/{get_safe_value(movie_details, 'imdb_id')}/"
                if IMDBLink == from_TMDB:
                    Checked = "✅"
                    get_IMDB_Screenshot(
                        driver=driver, link=IMDBLink
                    )  # Grabing SS from IMDB
                else:
                    movie_details_TMDB += f"IMDB Link: {IMDBLink}\n\n"
                    get_IMDB_Screenshot(
                        driver=driver, link=IMDBLink
                    )  # Grabing SS from IMDB
                    movie_details_TMDB += get_details_from_site(url)
                    return movie_details_TMDB

                movie_details_TMDB += (
                    f"Title [{Checked}]: {get_safe_value(movie_details, 'title')}\n"
                )
                movie_details_TMDB += f"Original Title: {get_safe_value(movie_details, 'original_title')}\n"
                movie_details_TMDB += (
                    f"Release Date: {get_safe_value(movie_details, 'release_date')}\n"
                )
                movie_details_TMDB += f"Runtime: {convert_to_hours(get_safe_value(movie_details, 'runtime'))}\n"
                movie_details_TMDB += f"Genres: {', '.join([genre['name'] for genre in movie_details['genres']])}\n"
                movie_details_TMDB += (
                    f"Overview: {get_safe_value(movie_details, 'overview')}\n"
                )
                movie_details_TMDB += (
                    f"Tagline: {get_safe_value(movie_details, 'tagline')}\n"
                )
                movie_details_TMDB += f"IMDB ID: https://www.imdb.com/title/{get_safe_value(movie_details, 'imdb_id')}\n"
                movie_details_TMDB += (
                    f"Homepage: {get_safe_value(movie_details, 'homepage')}\n"
                )
                movie_details_TMDB += (
                    f"Popularity: {get_safe_value(movie_details, 'popularity')}\n"
                )
                movie_details_TMDB += (
                    f"Average Vote: {get_safe_value(movie_details, 'vote_average')}\n"
                )
                movie_details_TMDB += (
                    f"Vote Count: {get_safe_value(movie_details, 'vote_count')}\n"
                )
                movie_details_TMDB += (
                    f"Budget: ${get_safe_value(movie_details, 'budget')}\n"
                )
                movie_details_TMDB += (
                    f"Revenue: ${get_safe_value(movie_details, 'revenue')}\n"
                )
                movie_details_TMDB += f"Production Companies: {', '.join([company['name'] for company in movie_details['production_companies']])}\n"
                movie_details_TMDB += f"Production Countries: {', '.join([country['name'] for country in movie_details['production_countries']])}\n"
                movie_details_TMDB += f"Spoken Languages: {', '.join([lang['english_name'] for lang in movie_details['spoken_languages']])}\n"
            else:
                movie_details_TMDB += (
                    f"Failed to retrieve movie details: {movie_response.status_code}\n"
                )
        else:
            movie_details_TMDB += f"IMDB Link: {IMDBLink}\n\n"
            get_IMDB_Screenshot(driver=driver, link=IMDBLink)  # Grabing SS from IMDB
            movie_details_TMDB += get_details_from_site(url)
            # movie_details_TMDB += "No results found for the search query.\n"
    else:
        movie_details_TMDB += f"IMDB Link: {IMDBLink}\n\n"
        get_IMDB_Screenshot(driver=driver, link=IMDBLink)  # Grabing SS from IMDB
        movie_details_TMDB += get_details_from_site(url)
        # movie_details_TMDB += f"Search request failed: {response.status_code}\n"

    print(movie_details_TMDB)
    return movie_details_TMDB


if __name__ == "__main__":
    # Example usage:
    get_movie_details_TMDB("The Family Star (2024)")
