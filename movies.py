from statistics import median
import random
import movie_storage
from datetime import datetime

# ******** Defining the "Menu" function ***********
def movie_menu():
    print("\n********** My Movies Database **********")
    print("\n0. Exit")
    print("1. List movies")
    print("2. Add movie")
    print("3. Delete movie")
    print("4. Update movie")
    print("5. Stats")
    print("6. Random movie")
    print("7. Search movie")
    print("8. Movie sorted by rating")

    user_menu_choice = input("\nEnter choice (0-8): ")
    while user_menu_choice not in [str(i) for i in range(0, 9)]:
        print("Invalid choice")
        user_menu_choice = input("Enter choice (0-8): ")
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
    user_movie = input("\nEnter movie name: ")
    if user_movie in movies:
        print("\nAlready there")
        return

    # Rating validation
    while True:
        try:
            user_rating = float(input("Enter movie rating (1-10): "))
            if 1 <= user_rating <= 10:
                break
            else:
                print("Rating must be between 1 and 10.")
        except ValueError:
            print("Please enter a valid number.")

    # Year validation using 1888 as the cutoff date
    current_year = datetime.now().year
    while True:
        try:
            user_year = int(input("Enter movie year: "))
            if 1888 <= user_year <= current_year:
                break
            else:
                print(f"Year must be between 1888 and {current_year}.")
        except ValueError:
            print("Please enter a valid year (e.g. 1994).")

    movie_storage.add_movie(user_movie, user_year, user_rating)
    print(f"\nThe movie '{user_movie}' with rating {user_rating} and year {user_year} has been added")


# ****** Defining the "Delete movie" function ********
def delete_movie():
    movies = movie_storage.get_movies()
    user_movie = input("\nEnter movie name: ")
    if user_movie not in movies:
        print("\nMovie not found")
    else:
        movie_storage.delete_movie(user_movie)
        print(f"The movie called '{user_movie}' has been deleted")


# ****** Defining the "Update movie" function ********
def update_movie():
    movies = movie_storage.get_movies()
    user_movie = input("\nEnter movie name: ")
    if user_movie not in movies:
        print("Movie not found")
        return

    # Rating validation
    while True:
        try:
            user_rate = float(input("Enter the new movie rate (1-10): "))
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

    user_movie_input = input("\nEnter part of the movie name: ").lower().strip()
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
        elif user_menu_choice == "0":
            print("Bye 👋!")
            break
        else:
            print("Something went wrong with your choice")


if __name__ == "__main__":
    main()
