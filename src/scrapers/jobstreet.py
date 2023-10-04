from requests import get
import bs4 as bs

def data_lowongan_jobstreet(kata_kunci, taggar):
    try:
        taggar_map = {
            'komputer_ti': '?specialization=508',
            'manufaktur': '?specialization=510',
            'keuangan': '?specialization=501',
            'telekomunikasi': '?specialization=504',
            'ritel': '?specialization=503'
        }

        jobstreet_base = 'https://www.jobstreet.co.id/id/job-search/'

        if kata_kunci != '' and taggar == "":
            print('Yang keprint kondisi pertama')
            yang_dicari = kata_kunci+'-jobs/'
            page = get(f"{jobstreet_base}{yang_dicari}", headers={
                "User-Agent": "Mozilla/5.0"}).content
        elif kata_kunci != '' and taggar is not None:
            print('Yang keprint kondisi kedua')
            taggar_path = taggar_map.get(taggar, '')
            yang_dicari = kata_kunci+'-jobs/'
            page = get(f"{jobstreet_base}{yang_dicari}{taggar_path}", headers={
                "User-Agent": "Mozilla/5.0"}).content
        elif kata_kunci == '' and taggar is not None:
            print('Yang keprint kondisi terakhir')
            taggar_path = taggar_map.get(taggar, '')
            jobstreet = f"https://www.jobstreet.co.id/id/job-search/{taggar_path}"
            page = get(jobstreet, headers={
                "User-Agent": "Mozilla/5.0"}).content

        print('Kata kunci: ' + kata_kunci)
        if taggar is not None:
            print('Taggar: ' + taggar)

        results = []
        soup = bs.BeautifulSoup(page, 'html.parser')

        list_situs = []
        for semua_halaman in soup.findAll('select', {"id": "pagination"}):
            for link in semua_halaman.findAll('option'):
                list_situs.append(link.get_text())

        hasil = []
        for i in range(0, len(list_situs)):
            if i == (len(list_situs)-1):
                total = int(list_situs[i])

        total = 1

        data_array = []
        for crawl in range(total):
            if kata_kunci == '':
                jobstreet_new = jobstreet_base+'{0}'.format(crawl+1)
            else:
                jobstreet_new = jobstreet_base+yang_dicari+'{0}'.format(crawl+1)
            page_semua = get(jobstreet_new, headers={"User-Agent": "Mozilla/5.0"})
            page_semua = page_semua.content
            soup_semua = bs.BeautifulSoup(page_semua, 'html.parser')
            div_table_fix = soup_semua.find('div', {'class': 'sx2jih0 zcydq8bm'})

            for semua_data in div_table_fix.findAll('div', {'class': 'sx2jih0 zcydq89e zcydq88e zcydq872 zcydq87e'}):
                detail_array = []
                link = 'Jobsteet'
                lokasi = semua_data.find('span', {'class': 'sx2jih0 iwjz4h1 zcydq84u zcydq80 zcydq8r'}).get_text()
                perusahaan = semua_data.find('span', {'class': 'sx2jih0 zcydq84u es8sxo0 es8sxo1 es8sxo21 es8sxoi'})
                if perusahaan is None:
                    lokasi_perusahaan = "tidak diberitahukan"
                else:
                    perusahaan = perusahaan.get_text()
                    lokasi_perusahaan = perusahaan + ", " + lokasi
                detail_situs = semua_data.find('a', {'target': '_top'})['href']
                detail_array.append(link)
                detail_array.append('https://www.jobstreet.co.id'+detail_situs)
                for spesialisasi in semua_data.findAll('a', {'class': '_1hr6tkx5 _1hr6tkx8 _1hr6tkxb sx2jih0 sx2jihf zcydq8h'}):
                    detail_array.append(spesialisasi.get_text())
                pengalaman = semua_data.find('div', {'class': 'CompactOpportunityCardsc__OpportunityInfo-sc-1y4v110-13 ikxvyY'})
                for detail_data in semua_data.findAll('span'):
                    detail_array.append(detail_data.get_text().strip())

                data_array.append(detail_array)

                data_lowongan_baru = list(dict.fromkeys(detail_array))
                berkebalikan = data_lowongan_baru[::-1]

                detail_page = get(data_lowongan_baru[1], headers={
                    "User-Agent": "Mozilla/5.0"}).content
                soup_detail = bs.BeautifulSoup(detail_page, 'html.parser')
                array_javascript = []
                for javascriptAll in soup_detail.findAll('script'):
                    ambil_data_javascript = javascriptAll.text.split()
                    array_javascript.append(ambil_data_javascript)
                data_tanggal_fix = array_javascript[1][1023]

                if "IDR" in data_lowongan_baru:
                    if "IDR" in berkebalikan[2]:
                        job_data = {
                            'detail_situs': data_lowongan_baru[1],
                            'perusahaan_lokasi': lokasi_perusahaan,
                            'sumber_situs': link,
                            'lowongan_pekerjaan': data_lowongan_baru[2],
                            'tanggal_terbit': data_tanggal_fix[17:27],
                            'gaji': data_lowongan_baru[8],
                            'job_desk': 'tidak diberitahukan',
                        }
                    else:
                        job_data = {
                            'detail_situs': data_lowongan_baru[1],
                            'perusahaan_lokasi': lokasi_perusahaan,
                            'sumber_situs': link,
                            'lowongan_pekerjaan': data_lowongan_baru[2],
                            'tanggal_terbit': data_tanggal_fix[17:27],
                            'gaji': data_lowongan_baru[8],
                            'job_desk': data_lowongan_baru[9],
                        }
                else:
                    job_data = {
                        'detail_situs': data_lowongan_baru[1],
                        'perusahaan_lokasi': lokasi_perusahaan,
                        'sumber_situs': link,
                        'lowongan_pekerjaan': data_lowongan_baru[2],
                        'tanggal_terbit': data_tanggal_fix[17:27],
                        'gaji': 'tidak diberitahukan',
                        'job_desk': 'tidak diberitahukan',
                    }
                results.append(job_data)

        return results
    except:
        return [{
            'detail_situs': "",
            'perusahaan_lokasi': "",
            'gaji': "",
            'lowongan_pekerjaan': "",
            'sumber_situs': "",
            'tanggal_terbit': "",
            'job_desk': ""
        }]

# Example usage:
# if __name__ == "__main__":
#     data_lowongan_jobstreet('keuangan', 'komputer_ti')
