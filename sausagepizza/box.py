from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import base64
import logging
import os

# Configure logging for debug purposes
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

def scrape_canvas_images(url, save_folder="jap/box_images"):
    # Set up Selenium with a headless Chrome browser
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    service = Service(executable_path="chromedriver.exe")  # Update with your chromedriver path
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Open the target URL
        logger.debug(f"Navigating to URL: {url}")
        driver.get(url)
        
        # Wait for page to load (adjust time as needed or use WebDriverWait for more precision)
        driver.implicitly_wait(10)
        logger.debug("Page loaded successfully.")
        
        # Locate all <canvas> elements
        canvas_elements = driver.find_elements(By.TAG_NAME, "canvas")
        logger.debug(f"Found {len(canvas_elements)} <canvas> elements.")
        
        # Ensure the save folder exists
        os.makedirs(save_folder, exist_ok=True)
        logger.debug(f"Directory '{save_folder}' is ready to save images.")
        
        for index, canvas in enumerate(canvas_elements):
            try:
                # Use JavaScript to extract canvas content as a Base64-encoded PNG
                canvas_base64 = driver.execute_script(
                    "return arguments[0].toDataURL('image/png').substring(22);", canvas
                )
                logger.debug(f"Extracted Base64 data from canvas {index + 1}.")
                
                # Decode and save the image
                img_data = base64.b64decode(canvas_base64)
                img_path = os.path.join(save_folder, f"canvas_image_{index + 1}.png")
                with open(img_path, "wb") as img_file:
                    img_file.write(img_data)
                    logger.debug(f"Saved canvas image as: {img_path}")
            except Exception as e:
                logger.error(f"Error processing canvas {index + 1}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during scraping: {e}")
    finally:
        # Clean up and close the browser
        driver.quit()
        logger.debug("Browser session closed.")

if __name__ == "__main__":
    # Example usage
    target_url = "https://app.box.com/s/c3zxn9fz9hj75kh158h1yscwfe2r7ojx"  # Replace with your target URL
    scrape_canvas_images(target_url)
