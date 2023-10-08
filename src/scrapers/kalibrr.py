from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import re
import unicodedata

def data_lowongan_kalibrr(kata_kunci, taggar):
    if taggar is not None :
        job_name = taggar
    else :
        job_name = kata_kunci
    allData = []
    baseUrl = "https://www.kalibrr.com/"
    y = 5
    if job_name.lower() == "manufaktur":
        y = 1

    for x in range(y):
        x = x + 1
        print(f"Ambil data kalibrr ke - {x}")
        html_text = requests.get(f"{baseUrl}id-ID/job-board/te/{job_name}/{x}").text
        web_html = BeautifulSoup(html_text, "lxml")
            
        # Find all job listings
        kerjaan = web_html.find_all("main")

        # Initialize empty lists to store job details
        job_titles = []
        detail_situs = []
        company_names = []
        locations = []
        job_desk = []
        logo = []
        
        # Iterate through each job listing
        for job in kerjaan:
            h1_tags = job.find_all("a",attrs={'class':'k-text-primary-color'})
            job_title = [h1.text.strip() for h1 in h1_tags]
            detail_situs = [h1.get('href') for h1 in h1_tags]
            company_name = job.find_all("span", attrs={'class': 'k-inline-flex k-items-center k-mb-1'})
            company = [company.text.strip() for company in company_name]
            logos = job.find_all("img", attrs={'loading': 'eager'})
            logo = [logo.get("src") for logo in logos]
            location_name = job.find_all("div", attrs={'class': 'k-flex k-flex-col md:k-flex-row'})
            location = [location.text.strip() for location in location_name]
            created_time = job.find_all("span", attrs={'class': 'k-block k-mb-1'})
            created = [created.text.strip() for created in created_time]
            job_desk_name = job.find_all("div", attrs={'class': 'k-text-xs k-text-subdued k-col-start-2 k-row-start-5'})
            job_desk = [job_desk.text.strip() for job_desk in job_desk_name]
            
            # Append job details to respective lists
            job_titles.extend(job_title)
            logo.extend(logo)
            company_names.extend(company)
            locations.extend(location)
            created.extend(created)
            job_desk.extend(job_desk)

        for i in range(len(job_titles)):
            job_info = {}

            job_info['sumber_situs'] = baseUrl

            if i < len(logo) and logo[i] is not None:
                job_info['logo'] = logo[i]
            else:
                job_info['logo'] = "-"

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
                match = re.search(r"Posted (\d+) (days|months) ago", created_text)
                match2 = re.search(r"Posted a (day|month) ago", created_text)
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

    return allData