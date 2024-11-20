from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import warnings

warnings.filterwarnings('ignore')

class WebContentAnalyzer:
    def __init__(self):
        nltk.download('punkt', quiet=True)
        
        self.sensitive_keywords = {
            'violence': ['violence', 'murder', 'fight', 'weapons', 'blood', 'death', 'fatal'],
            'adult_content': ['pornography', 'adult', 'sex', 'nude', 'naked'],
            'drugs': ['drugs', 'cocaine', 'heroin', 'marijuana', 'opium'],
            'discrimination': ['discrimination', 'racism', 'sexism'],
            'gambling': ['gambling', 'casino', 'betting'],
            'fraud': ['fraud', 'hacking', 'scamming', 'theft']
        }

    def google_search(self, query, num_results=10):
        """Custom Google search using requests"""
        url = f"https://www.google.com/search?q={query}&num={num_results}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
        }
        
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            links = []
            for result in soup.find_all('div', class_='yuRUbf'):
                link = result.find('a')
                if link and link.has_attr('href'):
                    links.append(link['href'])
            
            return links[:num_results]
        except Exception as e:
            print(f"Google search error: {e}")
            return []

    def fetch_webpage(self, url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
            }
            response = requests.get(url, headers=headers, verify=False, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error loading page {url}: {e}")
            return None

    def analyze_text_content(self, text):
        if not text:
            return {}, 0, 0
        
        tokens = word_tokenize(text.lower())
        total_word_count = len(tokens)
        
        category_scores = {}
        bad_word_count = 0
        
        for category, keywords in self.sensitive_keywords.items():
            matches = sum(1 for token in tokens if any(keyword in token for keyword in keywords))
            category_scores[category] = matches
            bad_word_count += matches
        
        return category_scores, bad_word_count, total_word_count

    def get_safety_rating(self, bad_word_count, total_word_count):
        score = 10  # Base score
        
        # Calculate penalty
        if total_word_count > 0:
            bad_word_penalty = (bad_word_count / total_word_count) * 10 * 5  # Scale penalty
        else:
            bad_word_penalty = 0
        
        score -= bad_word_penalty
        
        # Limit score to minimum of 0
        score = max(0, score)
        
        # Assign rating based on score
        if score >= 9:
            rating = "Very Good"
        elif score >= 8:
            rating = "Good"
        elif score >= 7:
            rating = "Bad"
        else:
            rating = "Very Bad"
        
        return score, rating

    def analyze_single_webpage(self, url):
        try:
            content = self.fetch_webpage(url)
            if not content:
                return {
                    'url': url,
                    'status': 'error',
                    'message': 'Could not load the page'
                }
            
            soup = BeautifulSoup(content, 'html.parser')
            text_content = soup.get_text()
            
            category_scores, bad_word_count, total_word_count = self.analyze_text_content(text_content)
            score, rating = self.get_safety_rating(bad_word_count, total_word_count)
            
            return {
                'status': 'success',
                'url': url,
                'domain': urlparse(url).netloc,
                'safety_score': round(score, 2),
                'rating': rating,
                'bad_word_count': bad_word_count,
                'total_word_count': total_word_count,
                'category_analysis': category_scores
            }
        except Exception as e:
            return {
                'url': url,
                'status': 'error',
                'message': str(e)
            }

    def analyze_search_results(self, query):
        urls = self.google_search(query)
        if not urls:
            return []
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(self.analyze_single_webpage, urls))
        
        valid_results = [r for r in results if r.get('status') == 'success']
        return sorted(valid_results, key=lambda x: x['safety_score'], reverse=True)

app = Flask(__name__)
analyzer = WebContentAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    query = request.form.get('query')
    if not query:
        return jsonify({'error': 'Please enter a search keyword'}), 400
    
    results = analyzer.analyze_search_results(query)
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)
