print("Hello World!!")

import io
import time
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


driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(11)


def capture_long_screenshot(url, output_file):
    try:
        driver.get(url)
        viewport_height = driver.execute_script("return window.innerHeight")
        total_height = (
            2000  # driver.execute_script("return document.body.scrollHeight")
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


def main(links):
    for link in links:
        driver.get(link)

        with open("./LOGS.txt", "a+") as f:
            string = f"Screenshot Taken : {driver.title} : {str(datetime.now())}"
            f.write(string + "\n")
        file_name = f"./Screenshots/{str(driver.title).strip(chars_not_allowed)}.png"
        capture_long_screenshot(url=link, output_file=file_name)


if __name__ == "__main__":
    links = [
        "https://pynaabo.blogspot.com/",
        "https://thepiratebay.org/search.php?q=top100:all",
    ]
    main(links=links)
