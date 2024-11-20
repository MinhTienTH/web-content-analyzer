# Web Content Analyzer

Web Content Analyzer is a Python-based web application that helps analyze the content of web pages for sensitive keywords and assigns a safety score and rating based on the content. The application includes a Flask-based web interface for user interaction.

---

## Features

- **Google Search Integration**: Perform a custom Google search and retrieve URLs for analysis.
- **Content Analysis**: Analyze web page content for sensitive keywords related to categories like violence, adult content, drugs, discrimination, gambling, and fraud.
- **Safety Rating**: Assign safety scores and ratings to web pages based on the frequency of sensitive keywords.
- **Multithreading**: Use multithreaded processing to analyze multiple web pages efficiently.
- **Flask Web Interface**: A simple and interactive web interface to input queries and view analysis results.

---

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/MinhTienTH/web-content-analyzer.git
    cd web-content-analyzer
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Install NLTK data:
    ```bash
    python -m nltk.downloader punkt
    ```

---

## Usage

1. **Run the Application**:
    ```bash
    python app.py
    ```

2. **Access the Web Interface**:
   Open your browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000).

3. **Analyze Search Queries**:
   - Enter a search query in the input box on the homepage.
   - View the safety scores and detailed analysis of the top search results.

---

## Key Components

### **WebContentAnalyzer**
- `google_search(query, num_results=10)`: Fetch URLs from a Google search.
- `fetch_webpage(url)`: Download the HTML content of a webpage.
- `analyze_text_content(text)`: Analyze text for sensitive keywords.
- `get_safety_rating(bad_word_count, total_word_count)`: Calculate the safety score and rating.
- `analyze_single_webpage(url)`: Perform a detailed analysis of a single webpage.
- `analyze_search_results(query)`: Analyze multiple webpages from Google search results.

### **Flask Application**
- **Routes**:
  - `/`: Render the homepage.
  - `/analyze`: Accept POST requests with a search query and return analysis results in JSON format.

---

## Screenshots

### Home Page
*(Add a screenshot of your homepage)*

### Analysis Results
*(Add a screenshot of the results page)*

---

## Dependencies

- **Python 3.8+**
- **Flask**: Web framework.
- **Requests**: HTTP requests library.
- **BeautifulSoup**: HTML parsing.
- **NLTK**: Natural language processing toolkit.
- **ThreadPoolExecutor**: Multithreading for concurrent processing.

---

## License

This project is licensed under the [MIT License](LICENSE).

- **Google Search Parsing**: Custom parsing for Google search results.
- **NLTK**: For tokenizing and analyzing text.
- **BeautifulSoup**: For HTML content parsing.
# web-content-analyzer
