import json
from statistics import median
import random
import movie_storage_sql as movie_storage
import requests

# Constants for API
API_KEY = "3aea435f"
API_URL = "http://omdbapi.com/"

# Helper function for API calls
def fetch_movie_data(title):
    """
    Fetches data for a movie from OMDb.
    Returns the movie data as a dictionary if found, otherwise None.

    """

    try:

        params = {
            "t": title,
            "apikey": API_KEY
        }
        response = requests.get(API_URL, params=params)
        response.raise_for_status() # Raise an error in case of 404, 500

        data = response.json()

        #Check if API found the movie
        if data.get('Response') == 'True':
            return data
        else:
            print("No movie data found in our movie provider")
            return None

    except requests.exceptions.RequestException as e:
        # Handle network errors
        print(f"Connection error: {e}")
        return None
    except json.JSONDecodeError:
        print(f"Could not decode API response")
        return None

# ******** Defining the "Menu" function ***********
def movie_menu():
    print("\n********** My Movies Database **********")
    print("**********     🍿🎥📺🎞️🎬    **********")
    print("\n0. Exit ➜]")
    print("1. List movies")
    print("2. Add movie")
    print("3. Delete movie")
    print("4. Update movie")
    print("5. Stats")
    print("6. Random movie")
    print("7. Search movie")
    print("8. Movie sorted by rating")
    print("9. Generate website")

    user_menu_choice = input("\n▶ Enter choice (0 - 9): ")
    while user_menu_choice not in [str(i) for i in range(0, 10)]:
        print("Invalid choice")
        user_menu_choice = input("▶ Enter choice (0 - 9): ")
    return user_menu_choice
