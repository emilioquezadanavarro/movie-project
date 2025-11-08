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

    user_menu_choice = input("\n▶ Enter choice (1 - 9): ")
    while user_menu_choice not in [str(i) for i in range(0, 10)]:
        print("Invalid choice")
        user_menu_choice = input("▶ Enter choice (1 - 9): ")
    return user_menu_choice


# ****** Defining the "List and rates" function ********
def list_movies_rates():
    movies = movie_storage.get_movies()
    count = len(movies)
    print(f"\n{count} movies in total\n")
    for movie in sorted(movies.keys()):
        props = movies[movie]
        print(f"{movie}: {props['rating']:.1f} ({props['year']})")


# ****** Defining the "Add movie" function ********
def add_movie():

    movies = movie_storage.get_movies()

    user_movie = input("\n▶ Enter movie name: ")

    # Check if movie is already in our 'local' database
    if user_movie.lower() in (title.lower() for title in movies.keys()):
        print("\nThat movie already exists in the database.!")
        return

    # Getting data from API using the helper function
    print(f"Searching for {user_movie}...")
    movie_data = fetch_movie_data(user_movie)

    # If the API fails, return None.
    if movie_data is None:
        print("No movie data found")
        return

    # Getting the data from the API Response and
    # convert them to the expected type.
    try:
        year = int(movie_data.get('Year', 0))

        rating = float(movie_data.get('imdbRating', 0.0))

        poster = movie_data.get('Poster', "")

        if poster == 'N/A':
            poster = None # Store as NULL in database

    except ValueError:
        print("The data from the movie is not in the expected format.")
        return

    movie_storage.add_movie(movie_data["Title"], year, rating, poster)
    print(f"\nThe Movie '{movie_data['Title']}' (Year: {year}, Rating: {rating} has been added.")


# ****** Defining the "Delete movie" function ********
def delete_movie():
    movies = movie_storage.get_movies()
    user_movie = input("\n▶ Enter movie name: ")
    if user_movie not in movies:
        print("\nMovie not found")
    else:
        movie_storage.delete_movie(user_movie)
        print(f"The movie called '{user_movie}' has been deleted")


# ****** Defining the "Update movie" function ********
def update_movie():
    movies = movie_storage.get_movies()
    user_movie = input("\n▶ Enter movie name: ")
    if user_movie not in movies:
        print("Movie not found")
        return

    # Rating validation
    while True:
        try:
            user_rate = float(input("▶ Enter the new movie rate (1-10): "))
            if 1 <= user_rate <= 10:
                break
            else:
                print("Rating must be between 1 and 10.")
        except ValueError:
            print("Please enter a valid number.")

    movie_storage.update_movie(user_movie, user_rate)
    print(f"The movie called '{user_movie}' has been updated")


# ****** Defining the "average rating" function ********
def average_rating():
    movies = movie_storage.get_movies()
    if not movies:
        return 0.0
    ratings = [props["rating"] for props in movies.values()]
    return sum(ratings) / len(ratings)


#****** Defining the "MEDIAN" function ********
def median_rating():
    movies = movie_storage.get_movies()
    ratings = [props["rating"] for props in movies.values()]
    if not ratings:
        return 0.0
    return median(ratings)


#****** Defining the "Best movies" function ********
def best_movies():
    movies = movie_storage.get_movies()
    if not movies:
        return [], 0
    best_rating = max(props["rating"] for props in movies.values())
    best_movies_list = [title for title, props in movies.items() if props["rating"] == best_rating]
    return best_movies_list, best_rating


# ****** Defining the "Worst movie" function ********
def worst_movies():
    movies = movie_storage.get_movies()
    if not movies:
        return [], 0
    worst_rating = min(props["rating"] for props in movies.values())
    worst_movies_list = [title for title, props in movies.items() if props["rating"] == worst_rating]
    return worst_movies_list, worst_rating


def stats():
    avg = average_rating()
    med = median_rating()
    best_movies_list, best_rating = best_movies()
    worst_movies_list, worst_rating = worst_movies()

    print(f"\nAverage rating: {avg:.1f}")
    print(f"Median rating: {med:.1f}")
    print(f"Best movie(s): {', '.join(best_movies_list)} ({best_rating})")
    print(f"Worst movie(s): {', '.join(worst_movies_list)} ({worst_rating})")


#****** Defining the "Random movie" function ********
def random_movie():
    movies = movie_storage.get_movies()
    if not movies:
        print("No movies in database.")
        return
    movie, props = random.choice(list(movies.items()))
    print(f"\nRandom selection: {movie}: {props['rating']:.1f} ({props['year']})")


#****** Defining the "Search movie" function ********
def search_movie():
    movies = movie_storage.get_movies()
    if not movies:
        print("No movies in database.")
        return

    user_movie_input = input("\n▶ Enter part of the movie name: ").lower().strip()
    if not user_movie_input:
        print("Please enter something to search.")
        return

    movie_found = []
    for movie, props in movies.items():
        if user_movie_input in movie.lower():
            movie_found.append((movie, props["rating"], props.get("year")))

    if movie_found:
        print("\nMovies found:")
        for movie, rating, year in movie_found:
            print(f'{movie}: {rating} ({year})')
    else:
        print("No movies matched your search.")


#****** Defining the "Movies sorted by rating" function ********
def movies_sorted():
    movies = movie_storage.get_movies()
    if not movies:
        print("No movies in database.")
        return
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]["rating"], reverse=True)
    for movie, props in sorted_movies:
        print(f"{movie}: {props['rating']:.1f} ({props['year']})")


#****** Defining the "generate website" function ********
def generate_website():
    """

        Generates a static index.html file from the movie database
        using index_template.html file and creating a final file
        called index.html.

    """

    print(f"\nGenerating website...")

    # Getting all the movies from the database

    movies = movie_storage.get_movies()

    if not movies:
        print("No movies in database.")
        return

    # Reading the HTML template
    try:
        with open("index_template.html", "r", encoding="utf-8") as f:
            template_content = f.read()
    except FileNotFoundError:
        print("File not found")
        print("Please enter a valid file name or generate a new file in the same directory.")
        return

    # Generate the HTML for the movie grid

    movie_grid_html = ""
    for title, details in movies.items():
        poster_url = details.get("poster")
        if not poster_url or poster_url == "N/A":
            poster_url = "https://via.placeholder.com/300x444?text=No+Poster"

        # HTML Structure
        movie_grid_html += '        <li>\n'  # <li> has no class
        movie_grid_html += '            <div class="movie">\n'  # Wrapper div
        movie_grid_html += f'                <img class="movie-poster" src="{poster_url}"/>\n'
        movie_grid_html += f'                <div class="movie-title">{title}</div>\n'
        movie_grid_html += f'                <div class="movie-year">{details.get("year", "N/A")}</div>\n'
        movie_grid_html += '            </div>\n'  # Close wrapper div
        movie_grid_html += '        </li>\n'
        # --- End of new structure ---

    # Replace the placeholders in the template

    final_html = template_content.replace("__TEMPLATE_TITLE__", "Movie Party App")
    final_html = final_html.replace("__TEMPLATE_MOVIE_GRID__", movie_grid_html)

    # Writing the final HTML
    try:
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(final_html)
        print("Website was generated successfully ✅")

    except IOError as e:
        print(f"An error occurred writing index.html: {e}")


# ******** Main ********
def main():
    while True:
        user_menu_choice = movie_menu()
        if user_menu_choice == "1":
            list_movies_rates()
        elif user_menu_choice == "2":
            add_movie()
        elif user_menu_choice == "3":
            delete_movie()
        elif user_menu_choice == "4":
            update_movie()
        elif user_menu_choice == "5":
            stats()
        elif user_menu_choice == "6":
            random_movie()
        elif user_menu_choice == "7":
            search_movie()
        elif user_menu_choice == "8":
            movies_sorted()
        elif user_menu_choice == "9":
            generate_website()
        elif user_menu_choice == "0":
            print("Bye 👋!")
            break
        else:
            print("Something went wrong with your choice")


if __name__ == "__main__":
    main()
