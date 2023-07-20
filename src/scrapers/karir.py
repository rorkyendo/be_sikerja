from requests import get
import bs4 as bs
from datetime import datetime
import json


def data_lowongan_karir(kata_kunci, taggar):
    try:
        if kata_kunci != '' and taggar == "":
            print('Yang keprint kondisi pertama')
            yang_dicari = kata_kunci
            karir = 'https://www.karir.com/search?context=welcome_main_search&q='
            page = get(f"{karir}{yang_dicari}", headers={
                "User-Agent": "Mozilla/5.0"}).content
        elif kata_kunci != '' and taggar is not None:
            print('Yang keprint kondisi kedua')
            if taggar == 'komputer_ti':
                yang_dicari = kata_kunci
                karir = 'https://www.karir.com/search?q='+yang_dicari + \
                    '&sort_order=newest&industry_ids=-6&context=welcome_main_favorite_industry_item'
                page = get(f"{karir}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'manufaktur':
                yang_dicari = kata_kunci
                karir = 'https://www.karir.com/search?q='+yang_dicari + \
                    '&sort_order=newest&industry_ids=-44&context=welcome_main_favorite_industry_item'
                page = get(f"{karir}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'keuangan':
                yang_dicari = kata_kunci
                karir = 'https://www.karir.com/search?q='+yang_dicari + \
                    '&sort_order=newest&industry_ids=-11&context=welcome_main_favorite_industry_item'
                page = get(f"{karir}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'telekomunikasi':
                yang_dicari = kata_kunci
                karir = 'https://www.karir.com/search?q='+yang_dicari + \
                    '&sort_order=newest&industry_ids=-33&context=welcome_main_favorite_industry_item'
                page = get(f"{karir}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'ritel':
                yang_dicari = kata_kunci
                karir = 'https://www.karir.com/search?q='+yang_dicari + \
                    '&sort_order=newest&industry_ids=-29&context=welcome_main_favorite_industry_item'
                page = get(f"{karir}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
        elif kata_kunci == '' and taggar is not None:
            print('Yang keprint kondisi terakhir')
            if taggar == 'komputer_ti':
                karir = 'https://www.karir.com/search?q=&sort_order=newest&industry_ids=-6&context=welcome_main_favorite_industry_item'
                page = get(f"{karir}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'manufaktur':
                karir = 'https://www.karir.com/search?q=&sort_order=newest&industry_ids=-44&context=welcome_main_favorite_industry_item'
                page = get(f"{karir}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'keuangan':
                karir = 'https://www.karir.com/search?q=&sort_order=newest&industry_ids=-11&context=welcome_main_favorite_industry_item'
                page = get(f"{karir}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'telekomunikasi':
                karir = 'https://www.karir.com/search?q=&sort_order=newest&industry_ids=-33&context=welcome_main_favorite_industry_item'
                page = get(f"{karir}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'ritel':
                karir = 'https://www.karir.com/search?industry_ids=29'
                page = get(f"{karir}", headers={
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
        print("Karir:", karir)
        print('Kata kunci: '+kata_kunci)
        if taggar is not None:
            print('Taggar: '+taggar)

        # response = get(f"{karir}{yang_dicari}")

        # Cek Status Respon
        # if response.status_code != 200:
        #     # Error
        #     print("Tidak dapat mencari situs")

        # else:
        # Tidak ada error
        # Mencari Informasi Perusahaan
        # print(response.text)

        results = []
        # Dapatkan data html
        soup = bs.BeautifulSoup(page, 'html.parser')

        div_table_fix = soup.find('ul', {'class': 'opportunities'})
        # div_table_fix

        for lowongan_pekerjaan in div_table_fix.findAll('h4', {'class': 'tdd-function-name --semi-bold --inherit'}):
            print(lowongan_pekerjaan.string)

        data_array = []
        for semua_data in div_table_fix.findAll('li', {'class': 'columns opportunity'}):
            detail_array = []
            lowongan_pekerjaan = semua_data.find(
                'h4', {'class': 'tdd-function-name --semi-bold --inherit'})
            link = 'Karir'
            detail_situs = semua_data.find('a', {'class': '--blue'})['href']
            perusahaan = semua_data.find(
                'div', 'tdd-company-name h8 --semi-bold')
            waktu_publikasi = semua_data.find('time', '--h8')
            job_desk = semua_data.find('span', 'tdd-company')
            lokasi = semua_data.find('span', 'tdd-location')
            gaji = semua_data.find('span', 'tdd-salary')
            pengalaman = semua_data.find('span', 'tdd-experience')

            detail_array.append(lowongan_pekerjaan.get_text().strip())
            detail_array.append(link)
            detail_array.append('https://www.karir.com'+detail_situs)
            detail_array.append(perusahaan.get_text().strip())
            detail_array.append(waktu_publikasi.get_text().strip())
            detail_array.append(job_desk.get_text().strip())
            detail_array.append(lokasi.get_text().strip())
            detail_array.append(gaji.get_text().strip())
            detail_array.append(pengalaman.get_text().strip())

            data_array.append(detail_array)

            detail_halaman_situs = detail_array[2]
            page_detail_halaman_situs = get(detail_halaman_situs, headers={
                "User-Agent": "Mozilla/5.0"})
            page_detail_halaman_situs = page_detail_halaman_situs.content
            soup_detail_halaman_situs = bs.BeautifulSoup(
                page_detail_halaman_situs, 'html.parser')
            ambil_data_javascript = soup_detail_halaman_situs.find(
                'script', {'type': 'application/ld+json'}).text
            data_json_detail = json.loads(ambil_data_javascript, strict=False)
            waktu_terbit = datetime.strptime(
                data_json_detail['datePosted'], "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%Y-%m-%d")

            # Menyimpan data website ke pustaka sementara
            job_data = {
                'detail_situs': detail_array[2],
                'perusahaan_lokasi': detail_array[3]+', '+detail_array[6],
                'gaji': detail_array[7],
                'lowongan_pekerjaan': detail_array[0],
                'sumber_situs': link,
                'tanggal_terbit': waktu_terbit,
                'job_desk': 'Pengalaman '+detail_array[8]
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
    #     data_lowongan_karir('marketing')
