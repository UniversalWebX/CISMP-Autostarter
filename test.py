import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuration ---
TARGET_URL = "https://app.nodecraft.com/shared/14419a06-d514-49af-a28d-c01bc169aceb"
SHARE_PASSWORD = "gIAkoKXvU0HC8YnKnbGvqN9NL5cRsCeJ"
WAIT_TIME_SECONDS = 300  # 5 minutes

# Setup Headless Background Options
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")
# Required for GitHub Actions / Linux environments
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Automatically installs and manages the Chrome driver
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), 
    options=chrome_options
)

def activate_server_background():
    try:
        print("🚀 Starting background process...")
        driver.get(TARGET_URL)
        wait = WebDriverWait(driver, 15)
        actions = ActionChains(driver)

        # 1. Click main button
        print("Finding main button...")
        start_span = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//span[contains(text(), 'Start Server')]")
        ))
        actions.move_to_element(start_span).click().perform()
        print("✓ Main button clicked.")

        # 2. Enter Password
        password_input = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[type='password']")
        ))
        password_input.send_keys(SHARE_PASSWORD)
        print("✓ Password entered.")

        # 3. Handle Modal
        time.sleep(2) 
        modal_btn = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[@role='dialog']//span[contains(text(), 'Start Server')]")
        ))
        actions.move_to_element(modal_btn).click().perform()
        print("✓ Modal button clicked. Server should be starting!")
        
        # Take a success screenshot just to be sure
        driver.save_screenshot("success_check.png")
        print("✓ Success screenshot saved as 'success_check.png'.")

    except Exception as e:
        print(f"❌ Error: {e}")
        driver.save_screenshot("error_debug.png")
        print("❌ Error screenshot saved as 'error_debug.png'.")
        
    finally:
        print(f"⌛ Waiting {WAIT_TIME_SECONDS/60} minutes before closing browser...")
        time.sleep(WAIT_TIME_SECONDS)
        driver.quit()
        print("✅ Process finished and browser closed.")

if __name__ == "__main__":
    activate_server_background()
