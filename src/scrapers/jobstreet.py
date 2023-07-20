# Pustaka
from requests import get
import bs4 as bs


def data_lowongan_jobstreet(kata_kunci, taggar):
    try:
        if kata_kunci != '' and taggar == "":
            print('Yang keprint kondisi pertama')
            yang_dicari = kata_kunci+'-jobs/'
            jobstreet = 'https://www.jobstreet.co.id/id/job-search/'
            page = get(f"{jobstreet}{yang_dicari}", headers={
                "User-Agent": "Mozilla/5.0"}).content
        elif kata_kunci != '' and taggar is not None:
            print('Yang keprint kondisi kedua')
            if taggar == 'komputer_ti':
                yang_dicari = kata_kunci+'-jobs/'
                jobstreet = 'https://www.jobstreet.co.id/id/job-search/'
                spesialis = '?specialization=508'
                page = get(f"{jobstreet}{yang_dicari}{spesialis}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'manufaktur':
                yang_dicari = kata_kunci+'-jobs/'
                jobstreet = 'https://www.jobstreet.co.id/id/job-search/'
                spesialis = '?specialization=510'
                page = get(f"{jobstreet}{yang_dicari}{spesialis}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'keuangan':
                yang_dicari = kata_kunci+'-jobs/'
                jobstreet = 'https://www.jobstreet.co.id/id/job-search/'
                spesialis = '?specialization=501'
                page = get(f"{jobstreet}{yang_dicari}{spesialis}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'telekomunikasi':
                yang_dicari = kata_kunci+'-jobs/'
                jobstreet = 'https://www.jobstreet.co.id/id/job-search/'
                spesialis = '?specialization=504'
                page = get(f"{jobstreet}{yang_dicari}{spesialis}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'ritel':
                yang_dicari = kata_kunci+'-jobs/'
                jobstreet = 'https://www.jobstreet.co.id/id/job-search/'
                spesialis = '?specialization=503'
                page = get(f"{jobstreet}{yang_dicari}{spesialis}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
        elif kata_kunci == '' and taggar is not None:
            print('Yang keprint kondisi terakhir')
            if taggar == 'komputer_ti':
                jobstreet = 'https://www.jobstreet.co.id/id/job-search/computer-information-technology-jobs/'
                page = get(f"{jobstreet}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'manufaktur':
                jobstreet = 'https://www.jobstreet.co.id/id/job-search/manufacturing-jobs/'
                page = get(f"{jobstreet}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'keuangan':
                jobstreet = 'https://www.jobstreet.co.id/id/job-search/accounting-finance-jobs/'
                page = get(f"{jobstreet}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'telekomunikasi':
                jobstreet = 'https://www.jobstreet.co.id/id/job-search/arts-media-communications-jobs/'
                page = get(f"{jobstreet}", headers={
                    "User-Agent": "Mozilla/5.0"}).content
            elif taggar == 'ritel':
                jobstreet = 'https://www.jobstreet.co.id/id/job-search/sales-marketing-jobs/'
                page = get(f"{jobstreet}", headers={
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
        print("Jobsteet:", jobstreet)
        print('Kata kunci: '+kata_kunci)
        if taggar is not None:
            print('Taggar: '+taggar)
        # response = get(f"{jobstreet}{yang_dicari}")

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

        list_situs = []
        for semua_halaman in soup.findAll('select', {"id": "pagination"}):
            for link in semua_halaman.findAll('option'):
                # print(link.get_text())
                list_situs.append(link.get_text())

        # list_situs

        hasil = []
        for i in range(0, len(list_situs)):
            if i == (len(list_situs)-1):
                total = int(list_situs[i])

        # result

        # total = len(hasil) + 1
        total = 1

        # jobstreet_new = "https://www.jobs.id/lowongan-kerja?kata-kunci=keuangan"
        # semua_halaman = urllib.request.urlopen(jobstreet_new)
        # soup_semua = bs.BeautifulSoup(page, 'html.parser')
        data_array = []
        for crawl in range(total):
            # jobstreet = 'https://www.jobstreet.co.id/id/job-search/keuangan-jobs/{0}'.format(crawl+1)
            if kata_kunci == '':
                jobstreet_new = jobstreet+'{0}'.format(crawl+1)
            else:
                jobstreet_new = jobstreet+yang_dicari+'{0}'.format(crawl+1)
            # print(jobstreet)
            page_semua = get(
                jobstreet_new, headers={"User-Agent": "Mozilla/5.0"})
            page_semua = page_semua.content
            soup_semua = bs.BeautifulSoup(page_semua, 'html.parser')
            div_table_fix = soup_semua.find(
                'div', {'class': 'sx2jih0 zcydq8bm'})
            # div_table_fix

            for semua_data in div_table_fix.findAll('div', {'class': 'sx2jih0 zcydq89e zcydq88e zcydq872 zcydq87e'}):
                detail_array = []
                # lowongan_pekerjaan = semua_data.find('div', attrs={'class': 'sx2jih0 l3gun70 l3gun74 l3gun72'})
                link = 'Jobsteet'
                lokasi = semua_data.find(
                    'span', {'class': 'sx2jih0 iwjz4h1 zcydq84u zcydq80 zcydq8r'}).get_text()
                # print(lokasi)
                perusahaan = semua_data.find(
                    'span', {'class': 'sx2jih0 zcydq84u es8sxo0 es8sxo1 es8sxo21 es8sxoi'})
                if perusahaan is None:
                    lokasi_perusahaan = "tidak diberitahukan"
                # print(perusahaan)
                else:
                    perusahaan = perusahaan.get_text()
                    lokasi_perusahaan = perusahaan + ", " + lokasi
                detail_situs = semua_data.find('a', {'target': '_top'})['href']
                detail_array.append(link)
                detail_array.append('https://www.jobstreet.co.id'+detail_situs)
                for spesialisasi in semua_data.findAll('a', {'class': '_1hr6tkx5 _1hr6tkx8 _1hr6tkxb sx2jih0 sx2jihf zcydq8h'}):
                    # spesifik = spesialisasi.find(
                    #     'a', {'class': '_1hr6tkx5 _1hr6tkx8 _1hr6tkxb sx2jih0 sx2jihf zcydq8h'})
                    detail_array.append(spesialisasi.get_text())
                pengalaman = semua_data.find(
                    'div', {'class': 'CompactOpportunityCardsc__OpportunityInfo-sc-1y4v110-13 ikxvyY'})
                # detail_array.append(lowongan_pekerjaan.get_text().strip())
                for detail_data in semua_data.findAll('span'):
                    # print(detail_data.get_text().strip())
                    detail_array.append(detail_data.get_text().strip())
                # detail_array.append(pengalaman.get_text().strip())

                data_array.append(detail_array)

                # data_baru = list(
                #     map(lambda x: list(dict.fromkeys(x)), data_array))

                data_lowongan_baru = list(dict.fromkeys(detail_array))
                berkebalikan = data_lowongan_baru[::-1]

                detail_page = get(data_lowongan_baru[1], headers={
                    "User-Agent": "Mozilla/5.0"}).content
                soup_detail = bs.BeautifulSoup(detail_page, 'html.parser')
                array_javascript = []
                for javascriptAll in soup_detail.findAll('script'):
                    # print(javascriptAll.find('window.REDUX_STATE'))
                    ambil_data_javascript = javascriptAll.text.split()
                    # print(ambil_data_javascript)
                    array_javascript.append(ambil_data_javascript)
                print(array_javascript)
                data_tanggal_fix = array_javascript[1][1023]

                # print(data_baru)
                # print(mylist)
                # print('\n\n')
                # Menyimpan data website ke pustaka sementara
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
#     data_lowongan_jobstreet('keuangan')
