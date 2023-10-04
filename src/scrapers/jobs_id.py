from requests import get
import bs4 as bs
import json
from datetime import datetime

def data_lowongan_jobsid(kata_kunci, taggar):
    try:
        taggar_map = {
            'komputer_ti': 'bidang-it',
            'manufaktur': 'bidang-manufaktur',
            'keuangan': 'bidang-keuangan',
            'telekomunikasi': 'bidang-telekomunikasi',
            'ritel': 'bidang-ritel'
        }

        jobs_id_base = 'https://www.jobs.id/lowongan-kerja?kata-kunci='

        if kata_kunci != '' and taggar == "":
            print('Yang keprint kondisi pertama')
            yang_dicari = kata_kunci
            jobs_id = f"{jobs_id_base}{yang_dicari}"
            page = request.urlopen(jobs_id)
        elif kata_kunci != '' and taggar is not None:
            print('Yang keprint kondisi kedua')
            yang_dicari = kata_kunci
            taggar_path = taggar_map.get(taggar, '')
            jobs_id = f"https://www.jobs.id/lowongan-kerja-{yang_dicari}-{taggar_path}?kata-kunci={yang_dicari}&bidang={taggar_path}"
            page = request.urlopen(jobs_id)
        elif kata_kunci == '' and taggar is not None:
            print('Yang keprint kondisi terakhir')
            taggar_path = taggar_map.get(taggar, '')
            jobs_id = f"https://www.jobs.id/lowongan-kerja-{taggar_path}"
            page = request.urlopen(jobs_id)

        print('Kata kunci: ' + kata_kunci)
        if taggar is not None:
            print('Taggar: ' + taggar)

        results = []
        # Dapatkan data html
        soup = bs.BeautifulSoup(page, 'html.parser')

        list_situs = []
        for semua_halaman in soup.findAll('ul', {"class": "pagination"}):
            for link in semua_halaman.findAll('a'):
                list_situs.append(link['href'])

        hasil = []
        for i in list_situs:
            if i not in hasil:
                hasil.append(i)

        total = 1

        data_array = []
        for crawl in range(total):
            jobsid = 'https://www.jobs.id/lowongan-kerja?kata-kunci='+kata_kunci+'&halaman={0}'.format(crawl+1)

            semua_halaman = request.urlopen(jobsid)
            soup_semua = bs.BeautifulSoup(semua_halaman, 'html.parser')
            div_table_fix = soup.find('div', {'id': 'job-ads-container'})

            for semua_data in div_table_fix.findAll('div', {'class': 'col-xs-8 col-md-10'}):
                detail_array = []
                lowongan_pekerjaan = semua_data.find('a', {'target': '_blank'})
                link = 'Job.id'
                detail_situs = semua_data.find('a', {'target': '_blank'})['href']
                akses_detail_halaman = request.urlopen(detail_situs)
                soup_akses_detail = bs.BeautifulSoup(akses_detail_halaman, 'html.parser')
                tanggal_publish = soup_akses_detail.find('p', {'class': 'text-gray'}).get_text().strip()
                tanggal_publish_fix = tanggal_publish.replace('Diiklankan sejak', '').strip()
                tanggal_konversi = datetime.strptime(tanggal_publish_fix, "%d %B %Y").strftime("%Y-%m-%d")
                pengalaman = semua_data.find('div', {'class': 'CompactOpportunityCardsc__OpportunityInfo-sc-1y4v110-13 ikxvyY'})
                detail_array.append(lowongan_pekerjaan.get_text().strip())
                detail_array.append(link)
                detail_array.append(detail_situs)
                for detail_data in semua_data.findAll('p'):
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

# Example usage:
# if __name__ == "__main__":
#     data_lowongan_jobsid('it', 'komputer_ti')
