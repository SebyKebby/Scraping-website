import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException

def close_modal_if_exists(driver, wait):
    """Try to close the modal if it exists"""
    try:
        modal_close = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "button.leadinModal-close")
        ))
        modal_close.click()
        print("Modal closed successfully")
        time.sleep(1)
        return True
    except (TimeoutException, NoSuchElementException):
        return False

def save_to_csv(hotels_data, save_dir):
    """Save hotel data to CSV file with explicit path"""
    # Create directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)
    
    # Create filename with timestamp
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f'virtuoso_hotels_{timestamp}.csv'
    filepath = os.path.join(save_dir, filename)
    
    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Hotel Name', 'Location'])
        for idx, (hotel, location) in enumerate(hotels_data, 1):
            writer.writerow([idx, hotel, location])
    
    print(f"\nData saved to: {filepath}")
    return filepath

# Get the current script directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Create a data directory path
data_dir = os.path.join(current_dir, 'data')

# Initialize WebDriver
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
os.environ['PATH'] += r"E:/ML Learning/NCKH/.venv/chromedriver-win64"
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open the URL
    url = "https://www.virtuoso.com/travel/luxury-hotels/search#page=5&hotelTypes=Hotel%20or%20Resort&sort=HotelNameAsc"
    driver.get(url)
    
    # Wait for initial page load
    wait = WebDriverWait(driver, 10)
    
    click_count = 0
    max_attempts = 3
    
    while True:
        try:
            close_modal_if_exists(driver, WebDriverWait(driver, 3))
            
            show_more_buttons = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "button.btn.btn-sm.btn-tertiary.mx-auto")
            ))
            
            if not show_more_buttons:
                print("No more 'Show More' buttons found.")
                break
                
            bottom_button = show_more_buttons[-1]
            
            driver.execute_script("arguments[0].scrollIntoView(true);", bottom_button)
            time.sleep(1)
            
            driver.execute_script("window.scrollBy(0, 100);")
            
            attempt = 0
            while attempt < max_attempts:
                try:
                    bottom_button.click()
                    click_count += 1
                    print(f"Successfully clicked bottom 'Show More' button {click_count} times")
                    time.sleep(2)
                    break
                except ElementClickInterceptedException:
                    if close_modal_if_exists(driver, WebDriverWait(driver, 3)):
                        continue
                    attempt += 1
                    time.sleep(1)
                    if attempt == max_attempts:
                        print("Could not click button after multiple attempts")
                        raise
            
        except TimeoutException:
            print(f"Finished after {click_count} clicks - no more content to load")
            break
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            break
    
    print("\nExtracting hotel information...")
    hotels = driver.find_elements(By.CSS_SELECTOR, "a.-no-decoration-idle")
    locations = driver.find_elements(By.CSS_SELECTOR, "div.-location")
    
    hotel_data = [(hotel.text, location.text) for hotel, location in zip(hotels, locations)]
    
    # Save to the data directory
    saved_file_path = save_to_csv(hotel_data, data_dir)
    
    # Print summary
    print(f"\nTotal hotels found: {len(hotel_data)}")
    print(f"CSV file location: {saved_file_path}")
    
    # Try to open the folder containing the CSV
    try:
        os.startfile(os.path.dirname(saved_file_path))
    except AttributeError:  # For non-Windows systems
        import subprocess
        subprocess.Popen(['xdg-open', os.path.dirname(saved_file_path)])

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    driver.quit()