from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# ---------------- SETUP ---------------- #
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # run headless
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")  # for Docker stability
options.add_argument("--remote-allow-origins=*")  # allow all origins in CI

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)  # global wait

# ---------------- CONFIGURATION ---------------- #
BASE_URL = os.environ.get("BASE_URL") or "http://3.80.204.243:3005"
LOGIN_URL = f"{BASE_URL}/auth/login"

print(f"Base URL set to: {BASE_URL}")
print(f"Attempting to open login page: {LOGIN_URL}")

try:
    # ---------------- OPEN SITE ---------------- #
    driver.get(LOGIN_URL)
    print("Waiting 5 seconds for React hydration...")
    time.sleep(5)
    print(f"Current Page Title: {driver.title}")

    # ---------------- LOGIN ---------------- #
    print("Starting login process...")
    email_field = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))
    )
    email_field.send_keys("test123@gmail.com")

    password_field = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
    )
    password_field.send_keys("12345678")

    signin_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Sign In') or contains(text(),'Login')]"))
    )
    driver.execute_script("arguments[0].click();", signin_button)
    print("Login click performed.")
    time.sleep(3)
    print("Login sequence completed.")

    # ---------------- CLICK MENU ITEMS ---------------- #
    menu_items = ["Home","Products","Men","Women","Kids","Footwear","Accessories","Search"]

    nav_container = wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "nav"))
    )

    for item in menu_items:
        try:
            menu_element = WebDriverWait(nav_container, 20).until(
                EC.element_to_be_clickable((By.XPATH, f".//label[contains(text(), '{item}')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", menu_element)
            driver.execute_script("arguments[0].click();", menu_element)
            print(f"Clicked menu item: {item}")
            time.sleep(1)
        except Exception as e:
            print(f"❌ Could not click menu item '{item}': {e}")

    # ---------------- CLICK HOME AGAIN ---------------- #
    home_menu = wait.until(
        EC.element_to_be_clickable((By.XPATH, ".//label[contains(text(),'Home')]"))
    )
    driver.execute_script("arguments[0].click();", home_menu)
    print("Clicked HOME again")
    time.sleep(2)

    # ---------------- CLICK PRODUCT IMAGE ---------------- #
    product_image = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.max-w-sm img"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", product_image)
    driver.execute_script("arguments[0].click();", product_image)
    print("Clicked product image")
    time.sleep(2)

    # ---------------- ADD TO CART ---------------- #
    add_to_cart = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Add to Cart')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", add_to_cart)
    driver.execute_script("arguments[0].click();", add_to_cart)
    print("Added product to cart")
    time.sleep(1)

    # ---------------- CLOSE MODAL ---------------- #
    close_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/button"))
    )
    driver.execute_script("arguments[0].click();", close_button)
    print("Closed modal")
    time.sleep(1)

    # ---------------- OPEN CART ---------------- #
    cart_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div/header/div/div[2]/div/button"))
    )
    driver.execute_script("arguments[0].click();", cart_button)
    print("Opened cart")
    time.sleep(1)

    # ---------------- PROCEED TO CHECKOUT ---------------- #
    checkout_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Checkout')]"))
    )
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
        input_field = wait.until(
            EC.visibility_of_element_located((By.NAME, field_name))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", input_field)
        input_field.clear()
        input_field.send_keys(value)
    print("Checkout form filled")



except Exception as e:
    print(f"\n❌ TEST FAILED: {e}")
    print("--------------------------------------------------")
    print("DEBUG: DUMPING PAGE SOURCE")
    print("--------------------------------------------------")
    try:
        print(driver.page_source[:2000])
        print("... (truncated)")
    except:
        print("Could not print page source.")
    print("--------------------------------------------------")
    raise e

finally:
    driver.quit()
    print("Browser closed")
