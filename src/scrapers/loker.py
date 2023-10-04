from requests import get
import bs4 as bs
import re
import json
from datetime import datetime


def data_lowongan_loker(kata_kunci, taggar):
    try:
        taggar_map = {
            'komputer_ti': 'information-technology',
            'manufaktur': 'pabrik-dan-manufaktur',
            'keuangan': 'akuntansi-keuangan',
            'telekomunikasi': 'telecommunications',
            'ritel': 'penjualan-pemasaran'
        }

        loker_base = 'https://www.loker.id/cari-lowongan-kerja?q='

        if kata_kunci != '' and taggar == "":
            print('Yang keprint kondisi pertama')
            loker = f"{loker_base}{kata_kunci}"
            page = get(loker, headers={"User-Agent": "Mozilla/5.0"}).content
        elif kata_kunci != '' and taggar is not None:
            print('Yang keprint kondisi kedua')
            taggar_path = taggar_map.get(taggar, '')
            loker = f"{loker_base}{kata_kunci}&category={taggar_path}"
            page = get(loker, headers={"User-Agent": "Mozilla/5.0"}).content
        elif kata_kunci == '' and taggar is not None:
            print('Yang keprint kondisi terakhir')
            taggar_path = taggar_map.get(taggar, '')
            loker = f"https://www.loker.id/lowongan-kerja/{taggar_path}"
            page = get(loker, headers={"User-Agent": "Mozilla/5.0"}).content

        print('Kata kunci: ' + kata_kunci)
        if taggar is not None:
            print('Taggar: ' + taggar)

        results = []
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
            if kata_kunci == '':
                loker_new = loker + f'?q=&page={crawl+1}'
            else:
                loker_new = loker + f'&page={crawl+1}'
            page_semua = get(loker_new, headers={"User-Agent": "Mozilla/5.0"})
            page_semua = page_semua.content
            soup_semua = bs.BeautifulSoup(page_semua, 'html.parser')
            div_table_fix = soup_semua.find('div', {'class': 'm-b-40'})

            for semua_data in div_table_fix.findAll('div', {'class': 'job-box'}):
                detail_array = []
                link = 'Loker'
                detail_situs = semua_data.find('a', {'class': 'btn btn-default btn-block'})['href']

                for detail_data in semua_data.findAll('td'):
                    detail_array.append(detail_data.get_text().strip())

                detail_array.append(link)
                detail_array.append(detail_situs)

                # detail loker
                detail_page = get(detail_array[7], headers={"User-Agent": "Mozilla/5.0"}).content
                soup_detail = bs.BeautifulSoup(detail_page, 'html.parser')
                ambil_data_javascript = soup_detail.find('script', {'type': 'application/ld+json'}).text
                data_json_detail = json.loads(ambil_data_javascript, strict=False)

                tanggal_publikasi = datetime.strptime(data_json_detail['datePosted'], "%Y-%m-%d").strftime("%Y-%m-%d")
                lowongan_pekerjaan = data_json_detail['occupationalCategory']

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
                    'perusahaan_lokasi': detail_array[1] + ', ' + detail_array[5],
                    'gaji': detail_array[9],
                    'lowongan_pekerjaan': lowongan_pekerjaan,
                    'sumber_situs': link,
                    'tanggal_terbit': detail_array[8],
                    'job_desk': detail_array[10]
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
#     data_lowongan_loker('keuangan', 'manufaktur')
