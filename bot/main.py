from playwright.sync_api import sync_playwright
import time
from getlyrics import get_random_lyric
import pyautogui
import random
from dotenv import load_dotenv
import os

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

INTERVAL = 1200 #intervalo entre postagens

def random_type(page, selector, text, min_delay=50, max_delay=150):
    page.click(selector)

    for char in text:
        page.keyboard.type(char)
        time.sleep(random.uniform(min_delay, max_delay) / 1000)

def human_move(x, y):
    steps = random.randint(50, 150)

    start_x, start_y = pyautogui.position()

    for i in range(steps):
        nx = start_x + (x - start_x) * (i / steps) + random.randint(-2, 2)
        ny = start_y + (y - start_y) * (i / steps) + random.randint(-2, 2)

        pyautogui.moveTo(nx, ny, random.uniform(0.01, 0.05), pyautogui.easeInQuad)
        time.sleep(random.uniform(0.005, 0.02))

    pyautogui.moveTo(x, y, random.uniform(0.05, 0.2), pyautogui.easeInBounce)

def trim_lines(s: str, limit: int = 255) -> str:
    if len(s) <= limit:
        return s

    s = s[:limit]
    last_newline = s.rfind("\n")
    return s[:last_newline + 1] if last_newline != -1 else ""

def format_time(seconds: int) -> str:
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)

    parts = []
    if h:
        parts.append(f"{h}h")
    if m:
        parts.append(f"{m}m")
    if s or not parts:  # show seconds if nothing else exists
        parts.append(f"{s}s")

    return " ".join(parts)

FORMATTED_INTERVAL = format_time(INTERVAL)

def enter_username(page):
    while True:
        page.click('input[name="text"]')
        page.fill('input[name="text"]', "")


        
        pyautogui.moveTo(random.randint(0, 1200), random.randint(0, 800),
                         duration=random.uniform(0.2, 1))

        # move back to input
        human_move(860, 480)
        pyautogui.click()
        random_type(page, 'input[name="text"]', USERNAME, 40, 120)
            
        page.click('span:has-text("Next")')
        

        try:
            page.wait_for_selector('input[name="password"]', timeout=3000)
            print("[INFO] Username accepted")
            return True

        except:
            print("[ERROR] Username not accepted, retrying...")

            # move cursor randomly
            
            #pyautogui.click()
def post():
    lyric = trim_lines(get_random_lyric())
    print(f"[INFO] POSTING LYRIC: \n{lyric}===================================")

    while True:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                args=["--disable-blink-features=AutomationControlled"]
            )
            page = browser.new_page()

            page.goto("https://x.com/login")

            try:
                page.wait_for_selector(
                    'input[name="text"], input[autocomplete="username"]',
                    timeout=8000
                )
                print("[INFO] Login page loaded")

                time.sleep(1)

                enter_username(page)

                page.type('input[name="password"]', PASSWORD, delay=87)
                page.click('span:has-text("Log in")')

                page.wait_for_url("https://x.com/home")

                page.click('div.public-DraftStyleDefault-block')
                page.keyboard.type(lyric)
                page.get_by_test_id("tweetButtonInline").click()

                print("[INFO ]SUCCESSFULLY POSTED")
                return  

            except Exception as e:
                print(f"[ERROR] Error occurred: {e}")
                print("[INFO] Retrying...\n")
                browser.close()
                continue

while True:
    post()
    
    for i in range(0, INTERVAL):
        print(f"[TIME] {format_time(i)}/{FORMATTED_INTERVAL}")
        pyautogui.moveTo(random.randint(50, 400), random.randint(50, 400))
        time.sleep(1)