from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import re
import unicodedata

def data_lowongan_karir(kata_kunci, taggar):
    if taggar is not None :
        job_name = taggar
    else :
        job_name = kata_kunci
    allData = []
    baseUrl = "https://www.karir.com"
    for x in range(5):
        x = x+1
        print(f"Ambil data karir ke - {x}")
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
        logo = []
        
        # Iterate through each job listing
        for job in kerjaan:
            h1_tags = job.find_all("h4",attrs={'class':'tdd-function-name'})
            job_title = [h1.text.strip() for h1 in h1_tags]
            company_name = job.find_all("div", attrs={'class': 'tdd-company-name'})
            company = [company.text.strip() for company in company_name]
            logos = job.find_all("img", attrs={'alt': 'logo'})
            logo = [logo.get("src") for logo in logos]
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
            logo.extend(logo)
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

            if i < len(logo) and logo[i] is not None:
                job_info['logo'] = logo[i]
            else:
                job_info['logo'] = "-"

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

    return allData