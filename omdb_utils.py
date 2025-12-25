# omdb_utils.py
import requests
from requests.exceptions import RequestException


def get_movie_details(title, api_key, timeout=5):
    """Fetch movie plot and poster from OMDB.

    Returns a tuple (plot, poster) or ("N/A", "N/A") on failure.
    """

    if not api_key:
        return "N/A", "N/A"

    params = {
        "t": title,
        "plot": "full",
        "apikey": api_key,
    }

    try:
        resp = requests.get("http://www.omdbapi.com/", params=params, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
    except (RequestException, ValueError):
        # Network error or invalid JSON
        return "N/A", "N/A"

    if data.get("Response") == "True":
        plot = data.get("Plot", "N/A") or "N/A"
        poster = data.get("Poster", "N/A") or "N/A"
        return plot, poster

    return "N/A", "N/A"
