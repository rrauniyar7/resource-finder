import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

app = Flask(__name__)

# Function to perform Google Custom Search
def google_search(query):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CSE_ID
    }
    
    try:
        response = requests.get(search_url, params=params)
        results = response.json()
        return results.get("items", [])  # Return search results
    except Exception as e:
        print(f"Error fetching search results: {e}")
        return []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description", "")
        query = f"{title} {description}" if description else title

        search_results = google_search(query)

        return jsonify({"results": [{"title": item["title"], "link": item["link"]} for item in search_results]})

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
