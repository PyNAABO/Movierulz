import json


def read_data():
    with open("./Data/data.json", "r") as f:
        link_data = json.load(f)
    return link_data


def read_movie_data():
    with open("./Data/movie_data.json", "r") as file:
        movie_data = json.load(file)
    return movie_data


def write_movie_data(data):
    try:
        movie_data = read_movie_data()
    except FileNotFoundError:
        movie_data = []

    movie_data.insert(0, data)
    movie_data = movie_data[:50]

    with open("./Data/movie_data.json", "w") as file:
        json.dump(movie_data, file, indent=4)
