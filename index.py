from flask import Flask, render_template, request, jsonify
import os
from src.classes.QueryBuilder import QueryBuilder
from src.scrapers.coordinator import get_new_jobs
from src.classes.HarmonySearch import harmony_search
import pandas as pd
from datetime import datetime

from bs4 import BeautifulSoup
import requests

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
    
    if taggar is None:
        taggar = ''
    if keyword is None:
        keyword = ''
    return harmony_search(taggar, keyword)

@app.route("/search")
def search():
    """
    Mengembalikan list pekerjaan dalam bentuk halaman website
    Selain itu route ini akan melakukan scraping terlebih dahulu
    """
    
    keyword = request.args.get("keyword")
    taggar = request.args.get("taggar")
    
    if taggar is None:
        taggar = ''
    if keyword is None:
        keyword = ''
    
    # start scraping
    new_jobs = get_new_jobs(keyword, taggar)
    
    # Check if "detail_situs" is empty in any of the new jobs
    if any(job['detail_situs'] == '' for job in new_jobs):
        return "Data tidak ada"
    
    jobs_to_insert = []
    for job in new_jobs:
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

@app.route("/testScrape")
def scrape():
    job_name = "programmer"
    allData = []
    for x in range(5): 
        html_text = requests.get(f"https://www.jobstreet.co.id/id/{job_name}-jobs?pg={x}").text
        web_html = BeautifulSoup(html_text, "lxml")
        
        # Find all job listings
        kerjaan = web_html.find_all("div", attrs={'class': 'z1s6m00', 'data-automation': 'jobListing'})
        
        # Initialize empty lists to store job details
        job_titles = []
        company_names = []
        locations = []
        
        # Iterate through each job listing
        for job in kerjaan:
            h1_tags = job.find_all("h1")
            job_title = [h1.text.strip() for h1 in h1_tags]
            company_name = job.find_all("a", attrs={'data-automation': 'jobCardCompanyLink'})
            company = [company.text.strip() for company in company_name]
            location_name = job.find_all("a", attrs={'data-automation': 'jobCardLocationLink'})
            location = [location.text.strip() for location in location_name]
            
            # Append job details to respective lists
            job_titles.extend(job_title)
            company_names.extend(company)
            locations.extend(location)

        for i in range(len(job_titles)):
            job_info = {}
            
            if i < len(job_titles) and job_titles[i] is not None:
                job_info['lowongan_pekerjaan'] = job_titles[i]
            else:
                job_info['lowongan_pekerjaan'] = "-"

            if i < len(company_names) and company_names[i] is not None:
                job_info['perusahaan_lokasi'] = company_names[i]
            else:
                job_info['perusahaan_lokasi'] = "-"

            if i < len(locations) and locations[i] is not None:
                job_info['lokasi'] = locations[i]
            else:
                job_info['lokasi'] = "-"
            
            allData.append(job_info)
    return jsonify(allData)

@app.route("/testScrape2")
def scrape2():
    job_name = "programmer"
    allData = []
    for x in range(5):
        html_text = requests.get(f"https://karir.com/search?q={job_name}&page={x}").text
        web_html = BeautifulSoup(html_text, "lxml")
        
        # Find all job listings
        kerjaan = web_html.find_all("section")

        # Initialize empty lists to store job details
        job_titles = []
        company_names = []
        locations = []
        
        # Iterate through each job listing
        for job in kerjaan:
            h1_tags = job.find_all("h4",attrs={'class':'tdd-function-name'})
            job_title = [h1.text.strip() for h1 in h1_tags]
            company_name = job.find_all("div", attrs={'class': 'tdd-company-name'})
            company = [company.text.strip() for company in company_name]
            location_name = job.find_all("span", attrs={'class': 'tdd-location'})
            location = [location.text.strip() for location in location_name]
            
            # Append job details to respective lists
            job_titles.extend(job_title)
            company_names.extend(company)
            locations.extend(location)

        for i in range(len(job_titles)):
            job_info = {}
            
            if i < len(job_titles) and job_titles[i] is not None:
                job_info['lowongan_pekerjaan'] = job_titles[i]
            else:
                job_info['lowongan_pekerjaan'] = "-"

            if i < len(company_names) and company_names[i] is not None:
                job_info['perusahaan_lokasi'] = company_names[i]
            else:
                job_info['perusahaan_lokasi'] = "-"

            if i < len(locations) and locations[i] is not None:
                job_info['lokasi'] = locations[i]
            else:
                job_info['lokasi'] = "-"

            allData.append(job_info)

    return jsonify(allData)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
