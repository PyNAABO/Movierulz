import requests
from lxml import html


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
def get_movie_details_TMDB(query):
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
                movie_details_TMDB += f"{query}\n"

                # Format movie details into a string
                from_TMDB = f"https://www.imdb.com/title/{get_safe_value(movie_details, 'imdb_id')}/"
                IMDBLink = get_IMDB_link(query)
                if IMDBLink == from_TMDB:
                    Checked = "✅"
                else:
                    Checked = "❌"
                    movie_details_TMDB += f"IMDB Link: {IMDBLink}\n\n"
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
            movie_details_TMDB += "No results found for the search query.\n"
    else:
        movie_details_TMDB += f"Search request failed: {response.status_code}\n"

    print(movie_details_TMDB)
    return movie_details_TMDB


if __name__ == "__main__":
    # Example usage:
    get_movie_details_TMDB("The Family Star (2024)")
