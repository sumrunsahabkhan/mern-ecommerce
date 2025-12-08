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

driver = webdriver.Chrome( options=options)
wait = WebDriverWait(driver, 15)

# Create screenshots folder
os.makedirs("screenshots", exist_ok=True)

# ---------------- OPEN SITE ---------------- #
driver.get("http://localhost:5173/auth/login")
time.sleep(1)
driver.save_screenshot("screenshots/01_open_site.png")

# ---------------- LOGIN ---------------- #


email_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"]')))
email_field.send_keys("test123@gmail.com")
password_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]')))
password_field.send_keys("12345678")

signin_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[1]/div/div[2]/div/form/button')))
driver.execute_script("arguments[0].click();", signin_button)
print("Login completed!")
time.sleep(3)  # wait for home page to load
driver.save_screenshot("screenshots/03_after_login.png")

# ---------------- CLICK MENU ITEMS ---------------- #
menu_items = ["Home","Products","Men","Women","Kids","Footwear","Accessories","Search"]

for idx, item in enumerate(menu_items, start=1):
    xpath = f"/html/body/div/div[1]/div/header/div/div[1]/nav/label[{idx}]"
    
    menu_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    driver.execute_script("arguments[0].scrollIntoView(true);", menu_element)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", menu_element)
    
    print(f"Clicked menu item: {item}")
    
    driver.save_screenshot(f"screenshots/0{idx}_clicked_{item}.png")
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

driver.save_screenshot("screenshots/08_home_again.png")
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
driver.save_screenshot("screenshots/09_product_image.png")
time.sleep(2)


add_to_cart = wait.until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div[4]/button"))
)
driver.execute_script("arguments[0].scrollIntoView(true);", add_to_cart)
driver.execute_script("arguments[0].click();", add_to_cart)
print("clicked add to cart")
driver.save_screenshot("screenshots/10_selected_size.png")
time.sleep(1)

# ---------------- CLICK CROSS BUTTON ---------------- #
cross_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/button"))
)

driver.execute_script("arguments[0].scrollIntoView(true);", cross_button)
time.sleep(0.3)
driver.execute_script("arguments[0].click();", cross_button)

print("Clicked cross button")
driver.save_screenshot("screenshots/11_added_to_cart.png")
time.sleep(1)

# ---------------- CLICK CART ICON ---------------- #
cart_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div/header/div/div[2]/div/button"))
)

driver.execute_script("arguments[0].click();", cart_button)
print("Opened cart")
driver.save_screenshot("screenshots/12_open_cart.png")
time.sleep(1)


# ---------------- PROCEED TO CHECKOUT ---------------- #
checkout_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/button[1]")))
driver.execute_script("arguments[0].scrollIntoView(true);", checkout_button)
driver.execute_script("arguments[0].click();", checkout_button)
print("Proceeded to checkout")
driver.save_screenshot("screenshots/13_checkout_page.png")
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

driver.save_screenshot("screenshots/14_filled_checkout.png")
time.sleep(1)


# ---------------- Add Address ---------------- #
add_address = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/div/main/div/div[2]/div[1]/div[3]/form/button")))
driver.execute_script("arguments[0].scrollIntoView(true);", add_address)
driver.execute_script("arguments[0].click();", add_address)
print("Address Added Successfully!")
driver.save_screenshot("screenshots/15_order_placed.png")
time.sleep(2)

driver.quit()


