from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# ---------------- SETUP ---------------- #
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # run headless
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage") # Added for better stability in Docker

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

# ---------------- CONFIGURATION ---------------- #
# Define Base URL from environment variable
BASE_URL = os.environ.get("BASE_URL")
if not BASE_URL:
    BASE_URL = "http://localhost:5173" 
    print("Warning: BASE_URL environment variable not set. Falling back to localhost.")

LOGIN_URL = f"{BASE_URL}/auth/login"
print(f"Base URL set to: {BASE_URL}")

# ---------------- OPEN SITE ---------------- #
try:
    print(f"Attempting to open login page: {LOGIN_URL}")
    driver.get(LOGIN_URL)

    # CRITICAL FIX: CI environments render React slower. 
    # Waiting 5 seconds ensures the DOM is fully hydrated before we check for elements.
    print("Waiting 5 seconds for page load...")
    time.sleep(5) 

    # DEBUG: Print title to verify we are on the right page
    print(f"Current Page Title: {driver.title}")

    # ---------------- LOGIN ---------------- #
    print("Starting login process...")
    
    # Increased wait time to 30s for the very first element to ensure app loaded
    email_field = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))
    )
    email_field.send_keys("test123@gmail.com")
    
    password_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]')))
    password_field.send_keys("12345678")

    signin_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[1]/div/div[2]/div/form/button')))
    driver.execute_script("arguments[0].click();", signin_button)
    print("Login click performed.")
    
    time.sleep(3)  # wait for home page to load
    print("Login sequence completed.")

    # ---------------- CLICK MENU ITEMS ---------------- #
    menu_items = ["Home","Products","Men","Women","Kids","Footwear","Accessories","Search"]

    for idx, item in enumerate(menu_items, start=1):
        xpath = f"/html/body/div/div[1]/div/header/div/div[1]/nav/label[{idx}]"
        
        menu_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        driver.execute_script("arguments[0].scrollIntoView(true);", menu_element)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", menu_element)
        
        print(f"Clicked menu item: {item}")
        time.sleep(1)

    # ---------------- CLICK HOME AGAIN ---------------- #
    home_menu = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/div/div[1]/div/header/div/div[1]/nav/label[1]")
        )
    )

    driver.execute_script("arguments[0].scrollIntoView(true);", home_menu)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", home_menu)

    print("Clicked HOME again")
    time.sleep(2)

    # ---------------- CLICK PRODUCT IMAGE ---------------- #
    image_element = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div.max-w-sm:nth-child(1) > div:nth-child(1) > div:nth-child(1) > img:nth-child(1)")
        )
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", image_element)
    driver.execute_script("arguments[0].click();", image_element)
    print("Clicked product image")
    time.sleep(2)

    add_to_cart = wait.until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div[4]/button"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", add_to_cart)
    driver.execute_script("arguments[0].click();", add_to_cart)
    print("clicked add to cart")
    time.sleep(1)

    # ---------------- CLICK CROSS BUTTON ---------------- #
    cross_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/button"))
    )

    driver.execute_script("arguments[0].scrollIntoView(true);", cross_button)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", cross_button)

    print("Clicked cross button")
    time.sleep(1)

    # ---------------- CLICK CART ICON ---------------- #
    cart_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div/header/div/div[2]/div/button"))
    )

    driver.execute_script("arguments[0].click();", cart_button)
    print("Opened cart")
    time.sleep(1)

    # ---------------- PROCEED TO CHECKOUT ---------------- #
    checkout_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/button[1]")))
    driver.execute_script("arguments[0].scrollIntoView(true);", checkout_button)
    driver.execute_script("arguments[0].click();", checkout_button)
    print("Proceeded to checkout")
    time.sleep(2)

    # ---------------- FILL CHECKOUT FORM ---------------- #
    checkout_data = {
        "address": "123 Main Street",
        "city": "New York",
        "pincode": "10001",
        "phone": "1234567890",
        "notes": "Please deliver between 9 AM to 5 PM"
    }

    for field_name, value in checkout_data.items():
        input_element = wait.until(
            EC.visibility_of_element_located((By.NAME, field_name))
        )

        driver.execute_script("arguments[0].scrollIntoView(true);", input_element)
        time.sleep(0.2)

        input_element.clear()
        input_element.send_keys(value)
    
    print("Checkout form filled")
    time.sleep(1)

    # ---------------- Add Address ---------------- #
    add_address = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/div/main/div/div[2]/div[1]/div[3]/form/button")))
    driver.execute_script("arguments[0].scrollIntoView(true);", add_address)
    driver.execute_script("arguments[0].click();", add_address)
    print("Address Added Successfully!")
    time.sleep(2)

except Exception as e:
    print(f"\n❌ TEST FAILED: {e}")
    print("--------------------------------------------------")
    print("DEBUG: DUMPING PAGE SOURCE")
    print("--------------------------------------------------")
    # This will print the HTML that Selenium sees, helping us identify if it's a 404, blank page, or loading screen.
    try:
        print(driver.page_source[:2000]) # Print first 2000 chars to avoid flooding logs too much
        print("... (truncated)")
    except:
        print("Could not print page source.")
    print("--------------------------------------------------")
    # Re-raise the exception so Jenkins marks the build as FAILED
    raise e

finally:
    driver.quit()
