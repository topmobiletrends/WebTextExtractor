from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/extract-text', methods=['POST'])
def extract_text():
    url = request.json.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML and extract text
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator='\n')  # Clean text with line breaks

        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)