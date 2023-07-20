from urllib import request
import bs4 as bs
from datetime import datetime


def data_lowongan_jobsid(kata_kunci, taggar):
    try:
        if kata_kunci != '' and taggar=="":
            yang_dicari = kata_kunci
            jobs_id = "https://www.jobs.id/lowongan-kerja?kata-kunci="
            page = request.urlopen(f"{jobs_id}{yang_dicari}")
        elif kata_kunci != '' and taggar is not None:
            print('Yang keprint kondisi kedua')
            if taggar == 'komputer_ti':
                yang_dicari = kata_kunci
                jobs_id = 'https://www.jobs.id/lowongan-kerja-' + \
                    yang_dicari+'-bidang-it?kata-kunci='+yang_dicari+'&bidang=it'
                page = request.urlopen(f"{jobs_id}")
            elif taggar == 'manufaktur':
                yang_dicari = kata_kunci
                jobs_id = 'https://www.jobs.id/lowongan-kerja-' + \
                    yang_dicari+'-bidang-manufaktur?kata-kunci='+yang_dicari+'&bidang=manufaktur'
                page = request.urlopen(f"{jobs_id}")
            elif taggar == 'keuangan':
                yang_dicari = kata_kunci
                jobs_id = 'https://www.jobs.id/lowongan-kerja-' + \
                    yang_dicari+'-bidang-keuangan?kata-kunci='+yang_dicari+'&bidang=keuangan'
                page = request.urlopen(f"{jobs_id}")
            elif taggar == 'telekomunikasi':
                yang_dicari = kata_kunci
                jobs_id = 'https://www.jobs.id/lowongan-kerja-' + \
                    yang_dicari+'-bidang-telekomunikasi?kata-kunci=' + \
                    yang_dicari+'&bidang=telekomunikasi'
                page = request.urlopen(f"{jobs_id}")
            elif taggar == 'ritel':
                yang_dicari = kata_kunci
                jobs_id = 'https://www.jobs.id/lowongan-kerja-' + \
                    yang_dicari+'-bidang-ritel?kata-kunci=' + \
                    yang_dicari+'&bidang=ritel'
                page = request.urlopen(f"{jobs_id}")
        elif kata_kunci == '' and taggar is not None:
            print('Yang keprint kondisi terakhir')
            if taggar == 'komputer_ti':
                jobs_id = 'https://www.jobs.id/lowongan-kerja-bidang-it'
                page = request.urlopen(f"{jobs_id}")
            elif taggar == 'manufaktur':
                jobs_id = 'https://www.jobs.id/lowongan-kerja-bidang-manufaktur'
                page = request.urlopen(f"{jobs_id}")
            elif taggar == 'keuangan':
                jobs_id = 'https://www.jobs.id/lowongan-kerja-bidang-keuangan'
                page = request.urlopen(f"{jobs_id}")
            elif taggar == 'telekomunikasi':
                jobs_id = 'https://www.jobs.id/lowongan-kerja-bidang-telekomunikasi'
                page = request.urlopen(f"{jobs_id}")
            elif taggar == 'ritel':
                jobs_id = 'https://www.jobs.id/lowongan-kerja-bidang-ritel'
                page = request.urlopen(f"{jobs_id}")

        print("Jobs id:", jobs_id)
        print(page)
        print('Kata kunci: '+kata_kunci)
        if taggar is not None:
            print('Taggar: '+taggar)

        # response = get(f"{jobs_id}{yang_dicari}")

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
        for semua_halaman in soup.findAll('ul', {"class": "pagination"}):
            for link in semua_halaman.findAll('a'):
                # print(link['href'])
                list_situs.append(link['href'])

        # list_situs

        hasil = []
        for i in list_situs:
            if i not in hasil:
                hasil.append(i)

        # result

        # total = len(hasil) + 1
        total = 1

        # jobsid = "https://www.jobs.id/lowongan-kerja?kata-kunci=keuangan"
        # semua_halaman = urllib.request.urlopen(jobsid)
        # soup_semua = bs.BeautifulSoup(page, 'html.parser')
        data_array = []
        for crawl in range(total):
            # print('https://www.jobs.id/lowongan-kerja?kata-kunci=keuangan&halaman={0}'.format(crawl+1))
            jobsid = 'https://www.jobs.id/lowongan-kerja?kata-kunci='+kata_kunci+'&halaman={0}'.format(
                crawl+1)
            # print(jobsid)

            semua_halaman = request.urlopen(jobsid)
            soup_semua = bs.BeautifulSoup(semua_halaman, 'html.parser')
            div_table_fix = soup.find('div', {'id': 'job-ads-container'})
            # div_table_fix

            for semua_data in div_table_fix.findAll('div', {'class': 'col-xs-8 col-md-10'}):
                detail_array = []
                lowongan_pekerjaan = semua_data.find('a', {'target': '_blank'})
                link = 'Job.id'
                detail_situs = semua_data.find(
                    'a', {'target': '_blank'})['href']
                akses_detail_halaman = request.urlopen(detail_situs)
                soup_akses_detail = bs.BeautifulSoup(
                    akses_detail_halaman, 'html.parser')
                tanggal_publish = soup_akses_detail.find(
                    'p', {'class': 'text-gray'}).get_text().strip()
                tanggal_publish_fix = tanggal_publish.replace(
                    'Diiklankan sejak', '').strip()
                tanggal_konversi = datetime.strptime(
                    tanggal_publish_fix, "%d %B %Y").strftime("%Y-%m-%d")
                pengalaman = semua_data.find(
                    'div', {'class': 'CompactOpportunityCardsc__OpportunityInfo-sc-1y4v110-13 ikxvyY'})
                detail_array.append(lowongan_pekerjaan.get_text().strip())
                detail_array.append(link)
                detail_array.append(detail_situs)
                for detail_data in semua_data.findAll('p'):
                    # print(detail_data.get_text().strip())
                    detail_array.append(detail_data.get_text().strip())
                if pengalaman is not None:
                    detail_array.append(pengalaman.get_text().strip())

                data_array.append(detail_array)

                # Menyimpan data website ke pustaka sementara
                job_data = {
                    'detail_situs': detail_situs,
                    'perusahaan_lokasi': detail_array[3],
                    'gaji': detail_array[4],
                    'lowongan_pekerjaan': detail_array[0],
                    'sumber_situs': link,
                    'tanggal_terbit': tanggal_konversi,
                    'job_desk': detail_array[5]
                }

                results.append(job_data)

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