from flask import Flask, render_template, request
import os
from src.classes.QueryBuilder import QueryBuilder
from src.scrapers.coordinator import get_new_jobs
from src.classes.HarmonySearch import harmony_search
import pandas as pd
from datetime import datetime

template_dir = os.path.abspath('views')
app = Flask("Lowongan Pekerjaan", template_folder=template_dir)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/find")
def find():
    """
        Mengembalikan list pekerjaan dalam bentuk JSON
    """
    
    keyword = request.args.get("keyword")
    taggar = request.args.get("taggar")
    
    if taggar is None: taggar = ''
    if keyword is None: keyword = ''
    return harmony_search(taggar, keyword)

@app.route("/search")
def search():
    """
        Mengembalikan list pekerjaan dalam bentuk halaman website
        Selain itu route ini akan melakukan scraping terlebih dahulu
    """
    
    keyword = request.args.get("keyword")
    taggar = request.args.get("taggar")
    if taggar is not None and taggar != '':
        # Mengganti karakter '%2F' dengan '_'
        taggar = taggar.replace("/", "_")
        taggar = taggar.lower()

    if taggar is None: taggar = ''
    if keyword is None: keyword = ''
    
    # start scraping
    new_jobs = get_new_jobs(keyword, taggar)
    jobs_to_insert = []
    for job in new_jobs:
        if job['lowongan_pekerjaan'] is not None and job['lowongan_pekerjaan'] != '':
            jobs_to_insert.append({
                'nama_loker': job['lowongan_pekerjaan'],
                'perusahaan': job['perusahaan_lokasi'],
                'deskripsi': job['job_desk'],
                'logo_perusahaan': None,
                'kategori': taggar,
                'gaji': job['gaji'],
                'tanggal': job['tanggal_terbit'] if job['tanggal_terbit'] != '' else datetime.now().strftime("%Y-%m-%d"),
                'source': job['sumber_situs'],
                'status': 'BARU',
                'created_by': 0
            })

    builder = QueryBuilder()
    builder.insert('sk_loker', pd.DataFrame(jobs_to_insert))
    # start harmony search
    solution = harmony_search(taggar, keyword)

    return render_template(
        "cari.html", 
        keyword=keyword,
        taggar=taggar,
        jobs=solution
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
