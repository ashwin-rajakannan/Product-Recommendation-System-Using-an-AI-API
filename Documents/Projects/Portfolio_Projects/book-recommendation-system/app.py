"""
Flask Web App for Book Recommendation System
"""
from flask import Flask, render_template_string, request
import pandas as pd
from book_recommender import load_books, filter_books

app = Flask(__name__)

# Load dataset once at startup
books_path = 'dataset/book32-listing.csv'
df = load_books(books_path)

# Curated genres (same as script)
GENRES = [
    "Calendars", "Science Fiction & Fantasy", "Romance", "Children's Books", "Mystery, Thriller & Suspense",
    "Comics & Graphic Novels", "Cookbooks, Food & Wine", "Biographies & Memoirs", "Christian Books & Bibles",
    "Medical Books", "Parenting & Relationships", "Politics & Social Sciences", "Reference", "Religion & Spirituality",
    "Self-Help", "Sports & Outdoors", "Teen & Young Adult", "Travel", "History", "Business & Money",
    "Education & Teaching", "Engineering & Transportation", "Arts & Photography", "Computers & Technology",
    "Crafts, Hobbies & Home", "Health, Fitness & Dieting", "Humor & Entertainment", "Law", "Literature & Fiction",
    "Science & Math"
]

def get_unique_authors():
    return sorted(set(df['Author'].dropna().unique()))

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang='en'>
<head>
    <title>Book Recommendation System based on Genre</title>
    <style>
    body {
        font-family: Arial, sans-serif;
        margin: 0;
        background: #18181b;
        color: #fff;
    }
    .container {
        max-width: 1200px;
        margin: 40px auto 0 auto;
        padding: 0 24px;
    }
    .form-group { margin-bottom: 1em; }
    .footer {
        background: #111;
        color: #aaa;
        text-align: center;
        padding: 24px 0 12px 0;
        font-size: 1em;
        margin-top: 48px;
    }
    .pagination {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 4px;
        margin: 32px 0 0 0;
        flex-wrap: wrap;
    }
    .page-btn, .page-ellipsis {
        background: #222;
        color: #fff;
        border-radius: 6px;
        padding: 6px 14px;
        border: none;
        margin: 0 2px;
        font-size: 1em;
        text-decoration: none;
        transition: background 0.2s;
    }
    .page-btn:hover {
        background: #4ade80;
        color: #222;
    }
    .page-btn.active {
        background: #4ade80;
        color: #fff;
        font-weight: bold;
    }
    .page-ellipsis {
        background: none;
        color: #aaa;
        padding: 6px 8px;
        cursor: default;
    }
    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fit,minmax(180px,1fr));
        gap: 1.5em;
        margin-bottom: 0;
    }
    .card {
        background: #222;
        border-radius: 8px;
        padding: 1em;
        text-align: center;
        color: #fff;
        box-shadow: 0 2px 8px #0002;
    }
    .card img {
        max-width: 120px;
        max-height: 160px;
        border-radius: 4px;
        margin-bottom: 0.5em;
    }
    .card .title {
        font-weight: bold;
        font-size: 1.05em;
        margin-bottom: 0.3em;
    }
    .card .author {
        color: #aaa;
        font-size: 0.95em;
        margin-bottom: 0.2em;
    }
    .card .genre {
        font-size: 0.9em;
        color: #4ade80;
    }
    </style>
</head>
<body>
    <div class="container">
        <h1 style="margin-bottom:1.2em;">Book Recommendation System based on Genre</h1>
        <form method="get" style="display:flex;flex-direction:row;align-items:center;gap:1.2em;margin-bottom:2em;flex-wrap:nowrap;">
            <label>Genre:
                <select name="genre" style="min-width:140px;">
                    <option value="">All</option>
                    {% for g in genres %}
                    <option value="{{g}}" {% if g==genre %}selected{% endif %}>{{g}}</option>
                    {% endfor %}
                </select>
            </label>
            <label>Author:
                <input type="text" name="author" value="{{author}}" style="min-width:120px;max-width:180px;" placeholder="Author name" />
            </label>
            <label>Search:
                <input type="text" name="search" value="{{search}}" style="min-width:180px;" placeholder="Title, author, ISBN" />
            </label>
            <label>Sort by:
                <select name="sort" style="min-width:100px;">
                    <option value="">None</option>
                    <option value="title" {% if sort_by=='title' %}selected{% endif %}>Title</option>
                    <option value="author" {% if sort_by=='author' %}selected{% endif %}>Author</option>
                </select>
            </label>
            <button type="submit" style="padding:0.5em 1.2em;background:#2ecc40;color:#fff;border:none;border-radius:4px;">Search</button>
        </form>
        {% if results is not none %}
            <h2 style="margin-bottom:1.2em;">Results ({{total_results}} found)</h2>
            <div class="grid">
                {% for row in results %}
                <div class="card">
                    <img src="{{row['ImageURL']}}" alt="Book Cover" />
                    <div class="title">{{row['Title']}}</div>
                    <div class="author">{{row['Author']}}</div>
                    <div class="genre">{{row['Genre']}}</div>
                </div>
                {% endfor %}
            </div>
            {% if total_pages > 1 %}
            <div class="pagination">
                {% if page > 1 %}
                    <a class="page-btn" href="?{{query_string}}&page={{page-1}}">Prev</a>
                {% endif %}
                {% set start_page = max(1, page-4) %}
                {% set end_page = min(total_pages, page+4) %}
                {% if start_page > 1 %}
                    <a class="page-btn" href="?{{query_string}}&page=1">1</a>
                    {% if start_page > 2 %}
                        <span class="page-ellipsis">...</span>
                    {% endif %}
                {% endif %}
                {% for p in range(start_page, end_page+1) %}
                    {% if p == page %}
                        <span class="page-btn active">{{p}}</span>
                    {% else %}
                        <a class="page-btn" href="?{{query_string}}&page={{p}}">{{p}}</a>
                    {% endif %}
                {% endfor %}
                {% if end_page < total_pages %}
                    {% if end_page < total_pages-1 %}
                        <span class="page-ellipsis">...</span>
                    {% endif %}
                    <a class="page-btn" href="?{{query_string}}&page={{total_pages}}">{{total_pages}}</a>
                {% endif %}
                {% if page < total_pages %}
                    <a class="page-btn" href="?{{query_string}}&page={{page+1}}">Next</a>
                {% endif %}
            </div>
            {% endif %}
        {% endif %}
    </div>
    <div class="footer">
        Ashwin Rajakannan © 2011 - 2025 &nbsp; - &nbsp; Browse Books
    </div>
</body>
</html>
"""
@app.route('/')
def home():
    genre = request.args.get('genre', '')
    author = request.args.get('author', '').strip()
    search = request.args.get('search', '').strip()
    sort_by = request.args.get('sort', '')

    filtered = df.copy()
    if genre:
        filtered = filtered[filtered['Genre'] == genre]
    if author:
        filtered = filtered[filtered['Author'].str.contains(author, case=False, na=False)]
    if search:
        filtered = filtered[
            filtered['Title'].str.contains(search, case=False, na=False) |
            filtered['Author'].str.contains(search, case=False, na=False)
        ]
    if sort_by == 'title':
        filtered = filtered.sort_values('Title')
    elif sort_by == 'author':
        filtered = filtered.sort_values('Author')

    books = filtered.head(20)
    results = []
    for _, row in books.iterrows():
        results.append({
            'ImageURL': row.get('ImageURL', ''),
            'Title': row.get('Title', ''),
            'Author': row.get('Author', ''),
            'Genre': row.get('Genre', '')
        })

    # Build query string for pagination (not implemented yet)
    query_string = f"genre={genre}&author={author}&search={search}&sort={sort_by}"

    return render_template_string(
        HTML_TEMPLATE,
        genres=GENRES,
        genre=genre,
        author=author,
        search=search,
        sort_by=sort_by,
        results=results,
        total_results=len(filtered),
        total_pages=1,
        page=1,
        query_string=query_string
    )
if __name__ == '__main__':
    app.run(debug=True)