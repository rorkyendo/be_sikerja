from requests import get
from urllib import request
import bs4 as bs
import lxml
import re
import json
from datetime import datetime


def data_lowongan_glints(kata_kunci, taggar):
    try:
        if kata_kunci != '' and taggar == "":
            print('Yang keprint kondisi pertama')
            yang_dicari = kata_kunci
            glints = "https://glints.com/id/opportunities/jobs/explore?keyword="
            page = get(f"{glints}{yang_dicari}", headers={
                "User-Agent": "Mozilla/5.0"}).content
        elif kata_kunci != '' and taggar is not None:
            print('Yang keprint kondisi kedua')
            if taggar == 'komputer_ti':
                yang_dicari = kata_kunci
                glints = 'https://glints.com/id/opportunities/jobs/explore?keyword=' + \
                    yang_dicari+'&slug=data-science-jobs&id=2&country=ID&jobCategories=2%2C1'
                page = get(f"{glints}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'manufaktur':
                yang_dicari = kata_kunci
                glints = 'https://glints.com/id/opportunities/jobs/explore?keyword=' + \
                    yang_dicari+'&jobCategories=6'
                page = get(f"{glints}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'keuangan':
                yang_dicari = kata_kunci
                glints = 'https://glints.com/id/opportunities/jobs/explore?keyword=' + \
                    yang_dicari+'&slug=finance-jobs&id=10&country=ID&jobCategories=10%2C7%2C5'
                page = get(f"{glints}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'telekomunikasi':
                yang_dicari = kata_kunci
                glints = 'https://glints.com/id/opportunities/jobs/explore?keyword=' + \
                    yang_dicari+'&jobCategories=12'
                page = get(f"{glints}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'ritel':
                yang_dicari = kata_kunci
                glints = 'https://glints.com/id/opportunities/jobs/explore?keyword=' + \
                    yang_dicari+'&jobCategories=13'
                page = get(f"{glints}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
        elif kata_kunci == '' and taggar is not None:
            print('Yang keprint kondisi terakhir')
            if taggar == 'komputer_ti':
                glints = 'https://glints.com/id/opportunities/jobs/explore?slug=data-science-jobs&id=2&country=ID&jobCategories=2%2C1'
                page = get(f"{glints}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'manufaktur':
                yang_dicari = kata_kunci
                glints = 'https://glints.com/id/opportunities/jobs/explore?jobCategories=6'
                page = get(f"{glints}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'keuangan':
                yang_dicari = kata_kunci
                glints = 'https://glints.com/id/opportunities/jobs/explore?slug=finance-jobs&id=10&country=ID&jobCategories=10%2C7%2C5'
                page = get(f"{glints}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'telekomunikasi':
                yang_dicari = kata_kunci
                glints = 'https://glints.com/id/opportunities/jobs/explore?jobCategories=12'
                page = get(f"{glints}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'ritel':
                yang_dicari = kata_kunci
                glints = 'https://glints.com/id/opportunities/jobs/explore?jobCategories=13'
                page = get(f"{glints}", headers={
                    "User-Agent": "Mozilla/5.0"}).content

                # response = get(f"{glints}{yang_dicari}", headers={
                # "User-Agent": "Mozilla/5.0"})
                # Cek Status Respon
                # if response.status_code != 200:
                #     # Error
                #     print("Tidak dapat mencari situs")

                # else:
                # Tidak ada error
                # Mencari Informasi Perusahaan
                # print(response.text)

        print('Kata kunci: '+kata_kunci)
        if taggar is not None:
            print('Taggar: '+taggar)

        results = []
        # Dapatkan data html
        soup = bs.BeautifulSoup(page, 'html.parser')

        div_table_fix = soup.find('div', {
            'class': 'CompactJobCardListsc__JobCardListContainer-sc-1jkgvrs-0'})

        data_array = []
        for semua_data in div_table_fix.findAll('div', {'class': 'JobCardsc__JobcardContainer-sc-1f9hdu8-0 hvpJwO CompactOpportunityCardsc__CompactJobCardWrapper-sc-1y4v110-0 dLzoMG compact_job_card'}):
            detail_array = []
            lowongan_pekerjaan = semua_data.find(
                'h2', {'class': 'CompactOpportunityCardsc__JobTitle-sc-1y4v110-7'})
            link = 'Glints'
            detail_situs = semua_data.find(
                'a', {'class': 'CompactOpportunityCardsc__CardAnchorWrapper-sc-1y4v110-18 iOjUdU job-search-results_job-card_link'})['href']
            perusahaan = semua_data.find(
                'a', {'class': 'CompactOpportunityCardsc__CompanyLink-sc-1y4v110-8'})
            pengalaman = semua_data.find(
                'div', {'class': 'CompactOpportunityCardsc__OpportunityInfo-sc-1y4v110-13 ikxvyY'})
            terakhir_update = semua_data.find(
                'div', {'class': 'CompactOpportunityCardsc__UpdatedTimeContainer-sc-1y4v110-20 ksKnzo'})
            # lokasi = semua_data.find('span')
            detail_array.append(lowongan_pekerjaan.get_text().strip())
            detail_array.append(link)
            detail_array.append('https://glints.com'+detail_situs)
            detail_array.append(perusahaan.get_text().strip())
            # for detail_data in semua_data.findAll('span'):
            #     # print(detail_data.get_text().strip())
            #     detail_array.append(detail_data.get_text().strip())

            # detail_array.append(pengalaman.get_text().strip())
            # detail_array.append(terakhir_update)
            for detail_data2 in semua_data.findAll('div', {'class': 'CompactOpportunityCardsc__OpportunityInfo-sc-1y4v110-13 ikxvyY'}):
                # print(detail_data.get_text().strip())
                detail_array.append(detail_data2.get_text().strip())

            id_link = detail_array[2].split('/')[-1]
            job_id_link = 'Job:'+id_link
            page_detail_situs = get(detail_array[2], headers={
                "User-Agent": "Mozilla/5.0"})
            page_detail_situs = page_detail_situs.content
            soup_detail_situs = bs.BeautifulSoup(page_detail_situs, 'html.parser')
            ambil_data_javascript = soup_detail_situs.find(
                'script', {'type': 'application/json'}).text
            data_json_detail = json.loads(ambil_data_javascript, strict=False)
            tanggal_publish = datetime.strptime(
                data_json_detail['props']['apolloCache'][job_id_link]['updatedAt'], '%Y-%m-%dT%H:%M:%S.%f%z').strftime("%Y-%m-%d")

            data_array.append(detail_array)

            # Menyimpan data website ke pustaka sementara
            job_data = {
                'detail_situs': detail_array[2],
                'perusahaan_lokasi': detail_array[3]+', '+detail_array[4],
                'gaji': detail_array[5],
                'lowongan_pekerjaan': detail_array[0],
                'sumber_situs': link,
                'tanggal_terbit': tanggal_publish,
                'job_desk': 'Memiliki pengalaman: '+detail_array[6]
            }

            results.append(job_data)

        # print(results)

        return results
    except:
        return[{
                'detail_situs': "",
                'perusahaan_lokasi': "",
                'gaji': "",
                'lowongan_pekerjaan': "",
                'sumber_situs': "",
                'tanggal_terbit': "",
                'job_desk': ""
            }]

# if __name__ == "__main__":
#     data_lowongan_glints('it')
