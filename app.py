from flask import Flask, request, jsonify, render_template
from newspaper import Article
import re

app = Flask(__name__)

# Serve the frontend (index.html) at the root route
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle text extraction
@app.route('/extract-text', methods=['POST'])
def extract_text():
    url = request.json.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        # Create an Article object
        article = Article(url)

        # Download and parse the article
        article.download()
        article.parse()

        # Extract the main article text
        text = article.text

        # Clean up the text (remove extra spaces and unwanted lines)
        text = re.sub(r'\n\s*\n', '\n', text)  # Remove extra newlines
        text = text.strip()  # Remove leading/trailing spaces

        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)