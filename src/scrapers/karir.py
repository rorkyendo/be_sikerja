from requests import get
import bs4 as bs
from datetime import datetime
import json


def data_lowongan_karir(kata_kunci, taggar):
    try:
        taggar_map = {
            'komputer_ti': '-91-94-47-92-46-93-45',
            'manufaktur': '-44',
            'keuangan': '-11',
            'telekomunikasi': '-33',
            'ritel': '29'
        }

        karir_base = 'https://www.karir.com/search?q='

        if kata_kunci != '' and taggar == "":
            print('Yang keprint kondisi pertama')
            karir = f"{karir_base}{kata_kunci}"
            page = get(karir, headers={"User-Agent": "Mozilla/5.0"}).content
        elif kata_kunci != '' and taggar is not None:
            print('Yang keprint kondisi kedua')
            taggar_path = taggar_map.get(taggar, '')
            karir = f"{karir_base}{kata_kunci}&sort_order=newest&job_function_ids={taggar_path}&context=welcome_main_favorite_industry_item"
            page = get(karir, headers={"User-Agent": "Mozilla/5.0"}).content
        elif kata_kunci == '' and taggar is not None:
            print("tag:")
            print(taggar)
            print('Yang keprint kondisi terakhir')
            taggar_path = taggar_map.get(taggar, '')
            karir = f"{karir_base}&sort_order=newest&industry_ids={taggar_path}&context=welcome_main_favorite_industry_item"
            page = get(karir, headers={"User-Agent": "Mozilla/5.0"}).content

        print('Kata kunci: ' + kata_kunci)
        if taggar is not None:
            print('Taggar: ' + taggar)

        results = []
        soup = bs.BeautifulSoup(page, 'html.parser')

        div_table_fix = soup.find('ul', {'class': 'opportunities'})

        data_array = []
        for semua_data in div_table_fix.findAll('li', {'class': 'columns opportunity'}):
            detail_array = []
            lowongan_pekerjaan = semua_data.find('h4', {'class': 'tdd-function-name --semi-bold --inherit'})
            link = 'Karir'
            detail_situs = semua_data.find('a', {'class': '--blue'})['href']
            perusahaan = semua_data.find('div', 'tdd-company-name h8 --semi-bold')
            waktu_publikasi = semua_data.find('time', '--h8')
            job_desk = semua_data.find('span', 'tdd-company')
            lokasi = semua_data.find('span', 'tdd-location')
            gaji = semua_data.find('span', 'tdd-salary')
            pengalaman = semua_data.find('span', 'tdd-experience')

            detail_array.append(lowongan_pekerjaan.get_text().strip())
            detail_array.append(link)
            detail_array.append('https://www.karir.com' + detail_situs)
            detail_array.append(perusahaan.get_text().strip())
            detail_array.append(waktu_publikasi.get_text().strip())
            detail_array.append(job_desk.get_text().strip())
            detail_array.append(lokasi.get_text().strip())
            detail_array.append(gaji.get_text().strip())
            detail_array.append(pengalaman.get_text().strip())

            data_array.append(detail_array)

            detail_halaman_situs = detail_array[2]
            page_detail_halaman_situs = get(detail_halaman_situs, headers={"User-Agent": "Mozilla/5.0"})
            page_detail_halaman_situs = page_detail_halaman_situs.content
            soup_detail_halaman_situs = bs.BeautifulSoup(page_detail_halaman_situs, 'html.parser')
            ambil_data_javascript = soup_detail_halaman_situs.find('script', {'type': 'application/ld+json'}).text
            data_json_detail = json.loads(ambil_data_javascript, strict=False)
            waktu_terbit = datetime.strptime(data_json_detail['datePosted'], "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%Y-%m-%d")

            # Menyimpan data website ke pustaka sementara
            job_data = {
                'detail_situs': detail_array[2],
                'perusahaan_lokasi': detail_array[3] + ', ' + detail_array[6],
                'gaji': detail_array[7],
                'lowongan_pekerjaan': detail_array[0],
                'sumber_situs': link,
                'tanggal_terbit': waktu_terbit,
                'job_desk': 'Pengalaman ' + detail_array[8]
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
#     data_lowongan_karir('marketing', 'komputer_ti')
