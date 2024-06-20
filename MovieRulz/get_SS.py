import io
import time
import subprocess
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


def get_IMDB_Screenshot(driver, link):
    driver.get(link)

    with open("./LOGS.txt", "a+") as f:
        string = f"Screenshot Taken : {driver.title} : {str(datetime.now())}"
        f.write(string + "\n")

    file_name = "./Data/IMDB_Screenshot.png"
    capture_long_screenshot(driver=driver, url=link, output_file=file_name)
    print("Screenshot Saved:", file_name)
    git_commit_and_push()
    return file_name
