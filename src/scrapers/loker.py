# Pustaka
from requests import get
import bs4 as bs
import lxml
import re
import json
from datetime import datetime


def data_lowongan_loker(kata_kunci, taggar):
    try:
        if kata_kunci != '' and taggar == "":
            print('Yang keprint kondisi pertama')
            yang_dicari = kata_kunci
            loker = 'https://www.loker.id/cari-lowongan-kerja?q='
            page = get(f"{loker}{yang_dicari}", headers={
                "User-Agent": "Mozilla/5.0"}).content
        elif kata_kunci != '' and taggar is not None:
            print('Yang keprint kondisi kedua')
            if taggar == 'komputer_ti':
                yang_dicari = kata_kunci
                loker = 'https://www.loker.id/cari-lowongan-kerja?q=' + \
                    yang_dicari+'&category=information-technology'
                page = get(f"{loker}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'manufaktur':
                yang_dicari = kata_kunci
                loker = 'https://www.loker.id/cari-lowongan-kerja?q=' + \
                    yang_dicari+'&category=pabrik-dan-manufaktur'
                page = get(f"{loker}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'keuangan':
                yang_dicari = kata_kunci
                loker = 'https://www.loker.id/cari-lowongan-kerja?q=' + \
                    yang_dicari+'&category=akuntansi-keuangan'
                page = get(f"{loker}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'telekomunikasi':
                yang_dicari = kata_kunci
                loker = 'https://www.loker.id/cari-lowongan-kerja?q=' + \
                    yang_dicari+'&category=telecommunications'
                page = get(f"{loker}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'ritel':
                yang_dicari = kata_kunci
                loker = 'https://www.loker.id/cari-lowongan-kerja?q=' + \
                    yang_dicari+'&category=penjualan-pemasaran'
                page = get(f"{loker}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
        elif kata_kunci == '' and taggar is not None:
            print('Yang keprint kondisi terakhir')
            if taggar == 'komputer_ti':
                loker = 'https://www.loker.id/lowongan-kerja/information-technology'
                page = get(f"{loker}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'manufaktur':
                loker = 'https://www.loker.id/lowongan-kerja/pabrik-dan-manufaktur'
                page = get(f"{loker}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'keuangan':
                loker = 'https://www.loker.id/lowongan-kerja/akuntansi-keuangan'
                page = get(f"{loker}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'telekomunikasi':
                loker = 'https://www.loker.id/lowongan-kerja/telecommunications'
                page = get(f"{loker}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'ritel':
                loker = 'https://www.loker.id/lowongan-kerja/penjualan-pemasaran'
                page = get(f"{loker}", headers={
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
        # response = get(f"{loker}{yang_dicari}")

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

        total_loker = soup.find('a', {'aria-label': 'Akhir'})

        if total_loker is None:
            total_loker = 1
        else:
            total_loker = re.findall(r'\b\d+\b', total_loker['href'])
            total_loker = int(total_loker[0])

        total_loker = 1

        data_array = []
        for crawl in range(total_loker):
            # loker_new = 'https://www.loker.id/cari-lowongan-kerja/page/{0}?q=keuangan'.format(
            #     crawl+1)
            # print(loker)
            if kata_kunci == '':
                loker_new = loker+'{0}?q='.format(crawl+1)
            else:
                loker_new = loker+'{0}?q='.format(crawl+1)+yang_dicari
            page_semua = get(
                loker, headers={"User-Agent": "Mozilla/5.0"})
            page_semua = page_semua.content
            soup_semua = bs.BeautifulSoup(page_semua, 'html.parser')
            div_table_fix = soup_semua.find('div', {'class': 'm-b-40'})
            # div_table_fix

            for semua_data in div_table_fix.findAll('div', {'class': 'job-box'}):
                detail_array = []
                # lowongan_pekerjaan = semua_data.find('div', attrs={'class': 'sx2jih0 l3gun70 l3gun74 l3gun72'})
                link = 'Loker'
                detail_situs = semua_data.find(
                    'a', {'class': 'btn btn-default btn-block'})['href']
                # pengalaman = semua_data.find('div', {'class': 'CompactOpportunityCardsc__OpportunityInfo-sc-1y4v110-13 ikxvyY'})
                # detail_array.append(lowongan_pekerjaan.get_text().strip())
                for detail_data in semua_data.findAll('td'):
                    # print(detail_data.get_text().strip())
                    detail_array.append(detail_data.get_text().strip())
                # detail_array.append(pengalaman.get_text().strip())
                detail_array.append(link)
                detail_array.append(detail_situs)

                # detail loker
                detail_page = get(detail_array[7], headers={
                    "User-Agent": "Mozilla/5.0"}).content
                soup_detail = bs.BeautifulSoup(detail_page, 'html.parser')
                ambil_data_javascript = soup_detail.find(
                    'script', {'type': 'application/ld+json'}).text
                data_json_detail = json.loads(
                    ambil_data_javascript, strict=False)

                # Ambil data tanggal
                tanggal_publikasi = datetime.strptime(
                    data_json_detail['datePosted'], "%Y-%m-%d").strftime("%Y-%m-%d")

                # Ambil data posisi
                lowongan_pekerjaan = data_json_detail['occupationalCategory']

                # Ambil data gaji
                array_gaji = []
                for tawaran_gaji in soup_detail.findAll('div', {'class': 'panel-heading padding-horizontal-double'}):
                    for element in tawaran_gaji.findChildren('div'):
                        array_gaji.append(element.text)

                detail_array.append(tanggal_publikasi)
                detail_array.append(array_gaji[3])
                detail_array.append(data_json_detail['responsibilities'])

                data_array.append(detail_array)

                # Menyimpan data website ke pustaka sementara
                job_data = {
                    'detail_situs': detail_array[7],
                    'perusahaan_lokasi': detail_array[1]+', '+detail_array[5],
                    'gaji': detail_array[9],
                    'lowongan_pekerjaan': lowongan_pekerjaan,
                    'sumber_situs': link,
                    'tanggal_terbit': detail_array[8],
                    'job_desk': detail_array[10]
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
#     data_lowongan_loker('keuangan')