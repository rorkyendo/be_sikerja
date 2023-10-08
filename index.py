from flask import Flask, render_template, request, jsonify
import os
from src.classes.QueryBuilder import QueryBuilder
from src.scrapers.coordinator import get_new_jobs
from src.classes.HarmonySearch import harmony_search
import pandas as pd
from datetime import datetime, timedelta
import re
import unicodedata
from bs4 import BeautifulSoup
import requests
from unidecode import unidecode

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
    
    jobs_to_insert = []
    for job in new_jobs:
        if job['lowongan_pekerjaan'] is not None :
            jobs_to_insert.append({
                'nama_loker': job['lowongan_pekerjaan'],
                'perusahaan': job['perusahaan_lokasi'],
                'deskripsi': job['job_desk'],
                'logo_perusahaan': job['logo'],
                'kategori': taggar,
                'gaji': job['gaji'],
                'tanggal': job['tanggal_terbit'] if job['tanggal_terbit'] != '' else datetime.now().strftime("%Y-%m-%d"),
                'source': job['detail_situs'],
                'status': 'BARU',
                'created_by': 0
            })

        builder = QueryBuilder()
        builder.insert_if_not_exist('sk_loker', pd.DataFrame(jobs_to_insert))

    # start harmony search
    solution = harmony_search(taggar, keyword)

    return render_template(
        "cari.html", 
        keyword=keyword,
        taggar=taggar,
        jobs=solution
    )

@app.route("/getData")
def getData():
    keyword = request.args.get("keyword")
    taggar = request.args.get("taggar")
    if taggar is None:
        taggar = ''
    if keyword is None:
        keyword = ''
    # start scraping
    new_jobs = get_new_jobs(keyword, taggar)
    
    jobs_to_insert = []
    for job in new_jobs:
        if job['lowongan_pekerjaan'] is not None :
            jobs_to_insert.append({
                'nama_loker' : unidecode(job['lowongan_pekerjaan']),
                'perusahaan' : unidecode(job['perusahaan_lokasi']),
                'deskripsi' : unidecode(job['job_desk']),
                'logo_perusahaan': job['logo'],
                'kategori': taggar,
                'gaji': job['gaji'],
                'tanggal': job['tanggal_terbit'] if job['tanggal_terbit'] != '' else datetime.now().strftime("%Y-%m-%d"),
                'source': job['detail_situs'],
                'status': 'BARU',
                'created_by': 0
            })

        builder = QueryBuilder()
        builder.insert_if_not_exist('sk_loker', pd.DataFrame(jobs_to_insert))

    return "success"

@app.route("/testScrape")
def scrape():
    job_name = "programmer"
    allData = []
    baseUrl = "https://www.jobstreet.co.id"
    for x in range(5): 
        x = x+1
        html_text = requests.get(f"{baseUrl}/id/{job_name}-jobs?pg={x}").text
        web_html = BeautifulSoup(html_text, "lxml")
        
        # Find all job listings
        kerjaan = web_html.find_all("div", attrs={'class': 'z1s6m00', 'data-automation': 'jobListing'})
        
        # Initialize empty lists to store job details
        job_titles = []
        company_names = []
        locations = []
        detail_situs = []
        created = []
        # Iterate through each job listing
        for job in kerjaan:
            h1_tags = job.find_all("h1")
            job_title = [h1.text.strip() for h1 in h1_tags]
            detail_situs_name = job.find_all("a", attrs={'class': 'jdlu992 jdlu994 jdlu997 y44q7i2 z1s6m00 z1s6m0f _1hbhsw6h'})
            detail_situs = [detail_situs.get("href") for detail_situs in detail_situs_name]
            company_name = job.find_all("a", attrs={'data-automation': 'jobCardCompanyLink'})
            company = [company.text.strip() for company in company_name]
            location_name = job.find_all("a", attrs={'data-automation': 'jobCardLocationLink'})
            location = [location.text.strip() for location in location_name]
            created_time = job.find_all("time")
            created = [created.get('datetime') for created in created_time]

            # Append job details to respective lists
            job_titles.extend(job_title)
            company_names.extend(company)
            locations.extend(location)
            created.extend(created)
            # job_desk.extend(job_desk)

        for i in range(len(job_titles)):
            job_info = {}
            
            job_info['gaji'] = '-'
            job_info['job_desk'] = '-'
            job_info['sumber_situs'] = baseUrl

            if i < len(detail_situs) and detail_situs[i] is not None:
                job_info['detail_situs'] = baseUrl+detail_situs[i]
            else:
                job_info['detail_situs'] = "-"

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

            if i < len(created) and created[i] is not None:
                # Parsing tanggal dalam format ISO 8601
                tanggal_terbit_datetime = datetime.strptime(created[i], "%Y-%m-%dT%H:%M:%S.%fZ")
                # Memformat tanggal ke format "Y-m-d"
                tanggal_terbit_format_baru = tanggal_terbit_datetime.strftime("%Y-%m-%d")
                job_info['tanggal_terbit'] = tanggal_terbit_format_baru 
            else:
                job_info['tanggal_terbit'] = "-"

            if job_info['detail_situs'] != "-" :            
                allData.append(job_info)

    return jsonify(allData)

@app.route("/testScrape2")
def scrape2():
    job_name = "programmer"
    allData = []
    baseUrl = "https://www.karir.com"
    for x in range(5):
        x = x+1
        html_text = requests.get(f"{baseUrl}/search?q={job_name}&page={x}").text
        web_html = BeautifulSoup(html_text, "lxml")
        
        # Find all job listings
        kerjaan = web_html.find_all("section")

        # Initialize empty lists to store job details
        job_titles = []
        company_names = []
        locations = []
        detail_situs = []
        gaji = []
        created = []
        
        # Iterate through each job listing
        for job in kerjaan:
            h1_tags = job.find_all("h4",attrs={'class':'tdd-function-name'})
            job_title = [h1.text.strip() for h1 in h1_tags]
            company_name = job.find_all("div", attrs={'class': 'tdd-company-name'})
            company = [company.text.strip() for company in company_name]
            detail_situs_name = job.find_all("a", attrs={'class': '--blue'})
            detail_situs = [detail_situs.get("href") for detail_situs in detail_situs_name]
            rangeGaji = job.find_all("span", attrs={'class': 'tdd-salary'})
            gaji = [gaji.text.strip() for gaji in rangeGaji]
            location_name = job.find_all("span", attrs={'class': 'tdd-location'})
            location = [location.text.strip() for location in location_name]
            created_time = job.find_all("time")
            created = [created.get('datetime') for created in created_time]

            # Append job details to respective lists
            job_titles.extend(job_title)
            company_names.extend(company)
            locations.extend(location)
            created.extend(created)
            detail_situs.extend(detail_situs)
            gaji.extend(gaji)

        for i in range(len(job_titles)):
            job_info = {}

            if i < len(gaji) and gaji[i] is not None:
                job_info['gaji'] = gaji[i]
            else:
                job_info['gaji'] = "-"

            job_info['job_desk'] = '-'
            job_info['sumber_situs'] = baseUrl

            if i < len(detail_situs) and detail_situs[i] is not None:
                job_info['detail_situs'] = baseUrl+detail_situs[i]
            else:
                job_info['detail_situs'] = "-"
            
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

            if i < len(created) and created[i] is not None:
                # Parsing tanggal dalam format ISO 8601 dengan timezone offset
                tanggal_terbit_datetime = datetime.strptime(created[i], "%Y-%m-%dT%H:%M:%S.%f%z")

                # Memformat tanggal ke format "Y-m-d"
                tanggal_terbit_format_baru = tanggal_terbit_datetime.strftime("%Y-%m-%d")
                job_info['tanggal_terbit'] = tanggal_terbit_format_baru 
            else:
                job_info['tanggal_terbit'] = "-"

            if job_info['detail_situs'] != "-" :            
                allData.append(job_info)

    return jsonify(allData)

@app.route("/testScrape3")
def scrape3():
    job_name = "programmer"
    allData = []
    baseUrl = "https://www.kalibrr.com"
    for x in range(5):
        x = x+1
        html_text = requests.get(f"{baseUrl}/job-board/te/{job_name}/{x}").text
        web_html = BeautifulSoup(html_text, "html.parser")
        print(f"{baseUrl}/job-board/te/{job_name}/{x}")
        # Find all job listings
        kerjaan = web_html.find_all("main")
        # Initialize empty lists to store job details
        job_titles = []
        detail_situs = []
        company_names = []
        locations = []
        job_desk = []
        
        # Iterate through each job listing
        for job in kerjaan:
            h1_tags = job.find_all("a",attrs={'class':'k-text-primary-color'})
            job_title = [h1.text.strip() for h1 in h1_tags]
            detail_situs = [h1.get('href') for h1 in h1_tags]
            company_name = job.find_all("span", attrs={'class': 'k-inline-flex k-items-center k-mb-1'})
            company = [company.text.strip() for company in company_name]
            location_name = job.find_all("div", attrs={'class': 'k-flex k-flex-col md:k-flex-row'})
            location = [location.text.strip() for location in location_name]
            created_time = job.find_all("span", attrs={'class': 'k-block k-mb-1'})
            created = [created.text.strip() for created in created_time]
            job_desk_name = job.find_all("div", attrs={'class': 'k-text-xs k-text-subdued k-col-start-2 k-row-start-5'})
            job_desk = [job_desk.text.strip() for job_desk in job_desk_name]
            
            # Append job details to respective lists
            job_titles.extend(job_title)
            company_names.extend(company)
            locations.extend(location)
            created.extend(created)
            job_desk.extend(job_desk)

        for i in range(len(job_titles)):
            job_info = {}

            job_info['sumber_situs'] = baseUrl
            if i < len(job_titles) and job_titles[i] is not None:
                job_info['lowongan_pekerjaan'] = job_titles[i]
            else:
                job_info['lowongan_pekerjaan'] = "-"

            if i < len(detail_situs) and detail_situs[i] is not None:
                job_info['detail_situs'] = baseUrl+detail_situs[i]
            else:
                job_info['detail_situs'] = "-"

            if i < len(company_names) and company_names[i] is not None:
                job_info['perusahaan_lokasi'] = company_names[i]
            else:
                job_info['perusahaan_lokasi'] = "-"

            if i < len(job_desk) and job_desk[i] is not None:
                job_info['job_desk'] = job_desk[i]
            else:
                job_info['job_desk'] = "-"
                        
            if i < len(locations) and locations[i] is not None:
                cleaned_text = unicodedata.normalize("NFKD", locations[i])
                lokasi_array = cleaned_text.split(" \u00b7 ")
                if len(lokasi_array) > 1:
                    job_info['lokasi'] = lokasi_array[0]
                    job_info['gaji'] = lokasi_array[1]
                else:
                    job_info['lokasi'] = cleaned_text
                    job_info['gaji'] = "-"  # Atau atur nilai default lainnya
            else:
                job_info['lokasi'] = "-"
                job_info['gaji'] = "-"  # Atau atur nilai default lainnya

            if i < len(created) and created[i] is not None:
                created_text = created[i]
                match = re.search(r"Posted (\d+) (day|days|month|months) ago", created_text)
                match2 = re.search(r"Posted a (day|days|month|months) ago", created_text)
                if match:
                    amount = int(match.group(1))
                    unit = match.group(2)
                    if unit == "days":
                        delta = timedelta(days=amount)
                    elif unit == "months":
                        # Menganggap satu bulan = 30 hari
                        delta = timedelta(days=amount * 30)
                    else:
                        pass

                    current_date = datetime.now()
                    created_date = current_date - delta
                    # Format tanggal sesuai kebutuhan
                    formatted_created_date = created_date.strftime("%Y-%m-%d")

                    job_info['tanggal_terbit'] = formatted_created_date  # Mengganti created dengan tanggal yang sudah diubah
                elif match2:
                    if unit == "month":
                        # Menganggap satu bulan = 30 hari
                        delta = timedelta(days=30)
                    else:
                        # Handle kasus lain jika perlu
                        pass
                    current_date = datetime.now()
                    created_date = current_date - delta
                    # Format tanggal sesuai kebutuhan
                    formatted_created_date = created_date.strftime("%Y-%m-%d")

                    job_info['tanggal_terbit'] = formatted_created_date  # Mengganti created dengan tanggal yang sudah diubah
                else :
                    current_date = datetime.now()
                    created_date = current_date
                    # Format tanggal sesuai kebutuhan
                    formatted_created_date = created_date.strftime("%Y-%m-%d")
                    job_info['tanggal_terbit'] = formatted_created_date
            else:
                current_date = datetime.now()
                created_date = current_date
                # Format tanggal sesuai kebutuhan
                formatted_created_date = created_date.strftime("%Y-%m-%d")
                job_info['tanggal_terbit'] = formatted_created_date

            if job_info['detail_situs'] != "-" :            
                allData.append(job_info)

    return jsonify(allData)

@app.route("/testScrape4")
def scrape4():
    job_name = "programmer"
    allJobs = []

    for x in range(5):
        # Mengirim permintaan GET ke URL dengan parameter job_name dan x
        response = requests.get(f"https://www.kalibrr.com/_next/data/is4RCy7AUF3h7gGXEaO8c/en/job-board/te/{job_name}/{x}.json")
        
        # Memeriksa apakah respons berhasil (status code 200)
        if response.status_code == 200:
            # Mengambil data JSON dari respons
            data = response.json()

            # Mengambil data pekerjaan dari properti jobs dalam jobBoardCorrection
            jobs = data.get("pageProps", {}).get("jobBoardCorrection", {}).get("jobs", [])
            for i in range(len(jobs)):
                job_info = {}
                job_info['lowongan_pekerjaan'] = jobs.company.companyName
                job_info['perusahaan_lokasi'] = jobs.company[i]

            # Menambahkan data pekerjaan ke daftar allJobs
            allJobs.extend(jobs)
        else:
            # Handle kesalahan jika permintaan tidak berhasil
            allJobs.append({"error": f"Failed to retrieve data for page {x}"})

    # Mengembalikan data pekerjaan dalam bentuk JSON menggunakan jsonify
    return jsonify(allJobs)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
