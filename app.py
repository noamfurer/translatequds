from flask import Flask, render_template_string
import feedparser
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

@app.route('/')
def home():
    # קישור לפיד ה-RSS
    rss_url = "https://ch2rss.fflow.net/QudsN"
    
    # קריאת הפיד
    feed = feedparser.parse(rss_url)
    
    # יצירת רשימת פריטים עם כותרות מתורגמות
    translated_entries = []
    for entry in feed.entries:
        # תרגום הכותרת מערבית לעברית
        translated_title = translator.translate(entry.title, src='ar', dest='he').text
        translated_entries.append({'title': translated_title, 'link': entry.link})
    
    # תבנית HTML להצגת הפיד
    template = """
    <!doctype html>
    <html lang="he">
      <head>
        <meta charset="utf-8">
        <title>פיד מתורגם לעברית</title>
      </head>
      <body>
        <h1>כותרות הפיד (מתורגם לעברית)</h1>
        <ul>
          {% for entry in entries %}
            <li><a href="{{ entry.link }}" target="_blank">{{ entry.title }}</a></li>
          {% endfor %}
        </ul>
      </body>
    </html>
    """
    
    # החזרת הדף עם הפריטים המתורגמים
    return render_template_string(template, entries=translated_entries)

if __name__ == '__main__':
    app.run(debug=True)
