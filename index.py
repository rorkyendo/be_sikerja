from flask import Flask, render_template, request
import os
from src.classes.QueryBuilder import QueryBuilder
from src.scrapers.coordinator import get_new_jobs

template_dir = os.path.abspath('views')
app = Flask("Lowongan Pekerjaan", template_folder=template_dir)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    taggar = request.args.get("taggar")
    
    new_jobs = get_new_jobs(keyword, taggar)
        
    builder = QueryBuilder()
    sk_loker = builder.raw_query("SELECT * FROM sk_loker")

    return render_template("cari.html", keyword=keyword, taggar=taggar, jobs=sk_loker)

if __name__ == '__main__':
    app.run(debug=True)
