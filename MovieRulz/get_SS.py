import io
import os
import time
import subprocess
import requests
from datetime import datetime

from PIL import Image
from selenium import webdriver
import chromedriver_autoinstaller
from pyvirtualdisplay import Display


display = Display(visible=0, size=(800, 800))
display.start()
chars_not_allowed = '~!@#$%^&*()_-+""/\:"|<>?,./'


chromedriver_autoinstaller.install()

chrome_options = webdriver.ChromeOptions()
options = [
    # Define window size here
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    # "--headless",
    # "--disable-gpu",
    # "--disable-extensions",
    # "--no-sandbox",
    # "--disable-dev-shm-usage",
    # '--remote-debugging-port=9222'
]

for option in options:
    chrome_options.add_argument(option)


def get_driver():
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(11)
    return driver


def capture_long_screenshot(driver, url, output_file):
    try:
        driver.get(url)
        viewport_height = driver.execute_script("return window.innerHeight")
        total_height = (
            1717  # driver.execute_script("return document.body.scrollHeight")
        )
        screenshot = Image.new(
            "RGB", (driver.execute_script("return window.innerWidth"), total_height)
        )
        offset = 0

        while offset < total_height:
            driver.execute_script(f"window.scrollTo(0, {offset});")
            time.sleep(1)
            screenshot_part = Image.open(io.BytesIO(driver.get_screenshot_as_png()))
            screenshot.paste(screenshot_part, (0, offset))
            offset += viewport_height

        screenshot.save(output_file)
    except Exception as e:
        print("ERROR:", e)


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


def send_request(link2send):
    # API endpoint URL with parameters
    url = "https://api.screenshotone.com/take"

    # Parameters for the GET request
    params = {
        "access_key": "W00tYMV_ALeG8Q",
        "url": link2send,
        "full_page": "false",
        "viewport_width": "1920",
        "viewport_height": "1080",
        "device_scale_factor": "1",
        "format": "jpg",
        "image_quality": "80",
        "block_ads": "true",
        "block_cookie_banners": "true",
        "block_banners_by_heuristics": "false",
        "block_trackers": "true",
        "delay": "0",
        "timeout": "60",
    }

    # HTTP method
    method = "GET"

    # Sending the HTTP request
    response = requests.request(method, url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        raise Exception(f"Request failed with status: {response.status_code}")

    # Save the image to a file
    file_path = os.path.join("Data", "IMDB_Screenshot.png")
    with open(file_path, "wb") as f:
        f.write(response.content)

    print(f"Image saved successfully at {file_path}")


def get_IMDB_Screenshot(driver, link):
    try:
        send_request(link2send=link)
    except:
        driver.get(link)

        with open("./LOGS.txt", "a+") as f:
            string = f"Screenshot Taken : {driver.title} : {str(datetime.now())}"
            f.write(string + "\n")

        file_name = "./Data/IMDB_Screenshot.png"
        capture_long_screenshot(driver=driver, url=link, output_file=file_name)
        print("Screenshot Saved:", file_name)
    git_commit_and_push()
    return file_name
