import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import  Service
import streamlit as st
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, WebDriverException

# Initialize Firefox WebDriver with GeckoDriver
def get_movie_reviews(movie_name):
    try:
        # Configure Firefox to run headlessly (without opening the actual browser window)
        # options = Options()
        # options.headless = True
    
        # Specify the path to your geckodriver
        driver_path=r'geckodriver.exe'
        service=Service(driver_path)
        driver = webdriver.Firefox(service=service)  # Update path to geckodriver

        # Visit IMDb page for the movie
        driver.get(f"https://www.imdb.com/find?q={movie_name}&ref_=nv_sr_sm")
        time.sleep(2)  # Wait for page to load

        # Click the first movie link
        movie_link = driver.find_element(By.XPATH,"/html/body/div[2]/main/div[2]/div[3]/section/div/div[1]/section[2]/div[2]/ul/li[1]/div[2]/div")
        movie_link.click()
        time.sleep(2)  # Wait for movie page to load

        # Scroll to reviews section
        reviews_button = driver.find_element(By.XPATH,"/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[1]/a/span/div/div[2]/div[1]/span[1]")
        reviews_button.click()
        time.sleep(2)

        #  Fetch reviews
        reviews = []
        review_elements = driver.find_elements(By.XPATH,"/html/body/div[2]/main/div/section/div/section/div/div[1]/section[1]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/span[1]")
        if review_elements:
            for review in review_elements[:5]:  # Limit to 5 reviews for brevity
                reviews.append(review.text)
        else:
            reviews=[]
        driver.quit()
        return reviews
    
    except NoSuchElementException as e:
        # Handle case when elements are not found
        reviews=[]
        error_message=f"Error: Movie or review section not found - {str(e)}"
        return reviews,error_message
   
    except WebDriverException as e:
        # Handle WebDriver errors (e.g., if the browser fails to open)
        reviews=[]
        error_message=f"Error: WebDriver issue - {str(e)}"
        return reviews,error_message
   
    except Exception as e:
        # Handle any other exceptions
        reviews=[]
        error_message=f"An unexpected error occurred: {str(e)}"
        return reviews, error_message
    

# Streamlit UI setup
st.title("Movie Review Fetcher")

# Dynamic input for movie
movie_name = st.text_input("Enter Movie name:","")

# Fetch reviews when user selects a movie
if movie_name:
    st.write(f"Fetching reviews for {movie_name}...")
    reviews,error_message = get_movie_reviews(movie_name)
   
    # Display reviews
    if reviews:
        st.subheader("Top Reviews:")
        for i, review in enumerate(reviews):
            st.write(f"{i+1}. {review}")
    else:
        st.write("No reviews found.")
        st.write(error_message)

# Exit button to terminate Streamlit app
exit_app = st.button('Exit Application')

if exit_app:
    st.write("Exiting Streamlit...")
    # sys.exit()  # This will stop the execution of the script and close the Streamlit server

    # Use JavaScript to close the current browser tab
    st.markdown(""" 
    <script type="text/javascript">
      window.close(); 
    </script> 
    """, unsafe_allow_html=True)
    # Optionally, force kill the Streamlit process (this is for Windows)
    os.system('taskkill /f /im streamlit.exe') 
    st.stop() # Stops the current Streamlit script execution
