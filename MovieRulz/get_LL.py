import json
import requests
from bs4 import BeautifulSoup


def get_ip():
    try:
        response = requests.get("http://jsonip.com")
        data = response.json()
        ip = data.get("ip")
        return ip
    except Exception as e:
        print("Error fetching IP:", e)
        return None


def get_latest_link():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }

        params = {
            "q": "movierulz",
        }

        response = requests.get(
            "https://www.google.com/search", params=params, headers=headers
        )
        soup = BeautifulSoup(response.content, "lxml")

        movierulz_links = []
        links = soup.find_all("div", class_="byrV5b")[:5]
        for link in links:
            link_text = link.find("cite").text.strip()
            if "movierulz" in link_text:
                movierulz_links.append(link_text)

        latest_movierulz_link = movierulz_links[0] if movierulz_links else None
        latest_movierulz_link += "/quality/hdrip/"
        with open("data.json", "r") as f:
            link_data = json.load(f)
        link_data["link"] = latest_movierulz_link
        with open("./Data/data.json", "w") as f:
            json.dump(link_data, f, indent=4)
        return latest_movierulz_link
    except Exception as e:
        print("Error fetching latest link:", e)
        return None


if __name__ == "__main__":
    ip = get_ip()
    if ip:
        print("Your IP is", ip)
    latest_link = get_latest_link()
    if latest_link:
        print("Latest Movierulz link:", latest_link)
