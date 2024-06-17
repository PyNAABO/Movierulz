import requests


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
def get_movie_details_TMDB(movie_name):
    # TMDb API endpoints and authentication headers
    search_url = "https://api.themoviedb.org/3/search/movie"
    movie_url = "https://api.themoviedb.org/3/movie/{}"

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

    # Check if search request was successful
    if response.status_code == 200:
        search_results = response.json()
        if search_results["total_results"] > 0:
            movie_id = search_results["results"][0]["id"]
            print(f"Found movie ID: {movie_id}")

            # Step 2: Retrieve detailed information about the movie using its ID
            movie_response = requests.get(
                movie_url.format(movie_id),
                params={"language": "en-US"},
                headers=headers,
            )

            # Check if movie details request was successful
            if movie_response.status_code == 200:
                movie_details = movie_response.json()

                # Format and print movie details
                print(f"Title: {get_safe_value(movie_details, 'title')}")
                print(
                    f"Original Title: {get_safe_value(movie_details, 'original_title')}"
                )
                print(f"Release Date: {get_safe_value(movie_details, 'release_date')}")
                print(
                    f"Runtime: {convert_to_hours(get_safe_value(movie_details, 'runtime'))}"
                )
                print(
                    f"Genres: {', '.join([genre['name'] for genre in movie_details['genres']])}"
                )
                print(f"Overview: {get_safe_value(movie_details, 'overview')}")
                print(f"Tagline: {get_safe_value(movie_details, 'tagline')}")
                print(
                    f"IMDB ID: https://www.imdb.com/title/{get_safe_value(movie_details, 'imdb_id')}"
                )
                print(f"Homepage: {get_safe_value(movie_details, 'homepage')}")
                print(f"Popularity: {get_safe_value(movie_details, 'popularity')}")
                print(f"Average Vote: {get_safe_value(movie_details, 'vote_average')}")
                print(f"Vote Count: {get_safe_value(movie_details, 'vote_count')}")

                # Additional details with error handling
                print(f"Budget: ${get_safe_value(movie_details, 'budget')}")
                print(f"Revenue: ${get_safe_value(movie_details, 'revenue')}")

                # Production companies
                production_companies = ", ".join(
                    [
                        company["name"]
                        for company in movie_details["production_companies"]
                    ]
                )
                print(f"Production Companies: {production_companies}")

                # Production countries
                production_countries = ", ".join(
                    [
                        country["name"]
                        for country in movie_details["production_countries"]
                    ]
                )
                print(f"Production Countries: {production_countries}")

                # Spoken languages
                spoken_languages = ", ".join(
                    [lang["english_name"] for lang in movie_details["spoken_languages"]]
                )
                print(f"Spoken Languages: {spoken_languages}")

            else:
                print(f"Failed to retrieve movie details: {movie_response.status_code}")
        else:
            print("No results found for the search query.")
    else:
        print(f"Search request failed: {response.status_code}")


if __name__ == "__main__":
    # Example usage:
    get_movie_details_TMDB("The Family Star")
