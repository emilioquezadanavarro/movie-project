import json
import os
from typing import Dict, Any

# Name of the JSON file used for persistent storage as per the example
_DATA_FILE = "data.json"
_TMP_FILE = _DATA_FILE + ".tmp"


def _ensure_file_exists() -> None:
    """
    Make sure the JSON file exists. If not, create an empty JSON object {}.
    This makes the storage robust if the file wasn't created manually.
    """
    if not os.path.exists(_DATA_FILE):
        with open(_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2)


def get_movies() -> Dict[str, Dict[str, Any]]:
    """
    Load the whole movies database from the JSON file and return it.
    If the file is missing or not a dict, it returns an empty dict.
    """
    _ensure_file_exists()
    with open(_DATA_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            # If file is invalid JSON, treat as empty
            return {}
    return data if isinstance(data, dict) else {}


def save_movies(movies: Dict[str, Dict[str, Any]]) -> None:
    """
    Save the entire movies dictionary to the JSON file.

    We write to a temporary file first and then atomically replace the original
    file to reduce the risk of corruption (partial write).

    """
    with open(_TMP_FILE, "w", encoding="utf-8") as f:
        json.dump(movies, f, indent=2, ensure_ascii=False)
    # Atomic replace on most platforms
    os.replace(_TMP_FILE, _DATA_FILE)


def add_movie(title: str, year: int, rating: float) -> None:
    """
    Add (or overwrite) a movie in storage.

    Steps:
      - load file
      - set movies[title] = {"rating": rating, "year": year}
      - save file

    Note: this will overwrite an existing movie with the same title.
    """
    movies = get_movies()
    movies[title] = {"rating": rating, "year": year}
    save_movies(movies)


def delete_movie(title: str) -> bool:
    """
    Delete a movie by title.
    Returns True if the movie existed and was deleted, False otherwise.

    """
    movies = get_movies()
    if title in movies:
        movies.pop(title)
        save_movies(movies)
        return True
    return False


def update_movie(title: str, rating: float) -> bool:
    """
    Update the rating for an existing movie (keeps other properties like year).
    Returns True if updated, False if the movie does not exist.

    """
    movies = get_movies()
    if title in movies:
        movies[title]["rating"] = rating
        save_movies(movies)
        return True
    return False
