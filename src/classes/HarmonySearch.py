import pandas as pd
import numpy as np
from .Helpers import Helpers
import random
from sklearn.preprocessing import MinMaxScaler
from .QueryBuilder import QueryBuilder
import time


class HarmonySearch():
    def __init__(
        self, data : pd.DataFrame, hms : int, n : int, hmcr: float, par : float
    ) -> None:
        """
        Data harus memiliki kolom tanggal, nama_loker, perusahaan, deskripsi dan kategori
        """

        if not np.all([column in data.columns for column in ['tanggal', 'nama_loker', 'perusahaan', 'deskripsi', 'kategori']]):
            raise Exception('Data harus memiliki kolom tanggal, nama_loker, perusahaan, deskripsi dan kategori')
        if data.shape[0] <= n: raise Exception('Jumlah data harus lebih banyak dari n')
        if hms <= 1: raise Exception('Nilai hms harus lebih besar dari 1')
        if hmcr < 0 or hmcr > 1: raise Exception('hmcr harus berada dalam rentang 0-1')
        if par < 0 or par > 1: raise Exception('par harus berada dalam rentang 0-1')


        self.id_data = list(range(data.shape[0]))
        data['id_data'] = self.id_data

        self.data = data
        self.hms = hms
        self.n = n
        self.hmcr = hmcr
        self.par = par


    def __init_data(self, taggar: str, keyword: str) -> None:
        data = self.data.copy()

        data['selisih_tanggal'] = data.tanggal.apply(Helpers.days_between)
        data['nama_loker'] = data['nama_loker'].str.lower()
        data['perusahaan'] = data['perusahaan'].str.lower()
        data['deskripsi'] = data['deskripsi'].str.lower()
        data['kategori'] = data['kategori'].str.lower()

        taggar = taggar.lower()
        keyword = keyword.lower()
        scaler_tanggal = MinMaxScaler()

        data['score_tanggal'] = scaler_tanggal.fit_transform(data[['selisih_tanggal']]).reshape(-1)
        data['score_nama_loker_keyword'] = data['nama_loker'].apply(lambda w: Helpers.similarity_score(w, keyword))
        data['score_perusahaan_keyword'] = data['perusahaan'].apply(lambda w: Helpers.similarity_score(w, keyword))
        data['score_kategori_taggar'] = data['kategori'].apply(lambda w: Helpers.similarity_score(w, taggar))

        selected_score = ['score_tanggal', 'score_nama_loker_keyword', 'score_perusahaan_keyword', 'score_kategori_taggar']

        data['score'] = (data['score_tanggal'] * 0.1) + (data['score_nama_loker_keyword'] * 0.3) + ( data['score_perusahaan_keyword'] * 0.3) + (data['score_kategori_taggar'] * 0.3)
        # print("socre",data['score'])
        self.__data = data

    def __init_harmony_memory(self) -> list:
        harmony_memory = []
        for i in range(self.hms):
            harmony_memory.append(random.sample(self.id_data, k=self.n))

        return np.array(harmony_memory)

    def __get_new_solution(self, harmony_memory):
            lower_bound = np.min(self.id_data)
            upper_bound = np.max(self.id_data)

            new_solution = []

            for j in range(self.n):

                xj = None


                if random.random() >= self.hmcr:
                    # jika nilai random lebih besar dari hmcr maka
                    # untuk xj nilainya dipiluh secara random dari seluruh data
                    # nilai xj tidak boleh duplikat
                    while (xj is None) or (xj in new_solution):
                        xj = random.sample(self.id_data, k=1)[0]
                else:
                    # jika nilai random lebih kecil dari hmcr maka
                    # xj diambil secara random dari seluruh nilai pada kolom ke j
                    # nilai xj tidak boleh duplikat
                    while (xj is None) or (xj in new_solution):
                        xj = random.sample(sorted(harmony_memory[:, j]), k=1)[0]


                    if random.random()  < self.par:
                        # jika nilai random lebih kecil dari nilai par
                        # maka lakukan mutasi dengan menambahkan nilai xj dengan random nilai
                        # digunakan while true agar hasil mutasi masih ada dalam lower bound, upper boud dan tidak duplikat
                        while True:
                            plus_or_min = random.sample([-1, 1], k=1)[0]
                            random_value = (random.random() * plus_or_min) * (upper_bound - lower_bound)

                            # karena xj harus int maka random value harus int juga
                            random_value = np.round(random_value)
                            xj_mutated = xj + random_value

                            # cek apakah hasil mutasi masih sesuai dengan batasan yang ditentukan
                            if (xj_mutated >= lower_bound) and (xj_mutated <= upper_bound) and (xj_mutated not in new_solution): break
                        xj = xj_mutated

                new_solution.append(xj)

            return new_solution

    def __evaluate_solution(self, solution: list[int]) -> float:
        selected_solution = self.__data[self.__data.id_data.isin(solution)][['id_data', 'score']]
        return selected_solution['score'].mean()

    def __order_harmony_memory_best_to_worst(self, harmony_memory) -> tuple[list[list], list, float]:
        temp = []

        for solution in harmony_memory:
            temp.append({
                'solution': solution,
                'score': self.__evaluate_solution(solution)
            })

        temp = sorted(temp, key=lambda t: t['score'] * -1)

        ordered_hm = [t['solution'] for t in temp]

        return np.array(ordered_hm), temp[-1]['solution'], temp[-1]['score']

    def __get_solution_data(self, solution):
        selected_solution = self.__data[self.__data.id_data.isin(solution)][['id_data', 'score']]
        selected_solution = self.data.merge(selected_solution)


        return (selected_solution
                .sort_values('score', ascending=False)
                .drop(['id_data', 'score'], axis=1)
                .reset_index(drop=True))


    def search(self, taggar: str, keyword: str, max_iter: int):
        self.__init_data(taggar, keyword)

        harmony_memory = self.__init_harmony_memory()

        for i in range(max_iter):
            new_solution = self.__get_new_solution(harmony_memory)
            harmony_memory, worst_solution, worst_solution_score = self.__order_harmony_memory_best_to_worst(harmony_memory)
            new_solution_score = self.__evaluate_solution(new_solution)

            # jika solusi yang baru
            if new_solution_score > worst_solution_score:
                harmony_memory[-1] = new_solution

        best_solution = harmony_memory[0]

        return self.__get_solution_data(best_solution)
    
def harmony_search(taggar: str, keyword: str):
    #  start harmony search
    start_time = time.time()  # Catat waktu mulai eksekusi
    builder = QueryBuilder()
    sk_loker = builder.raw_query("SELECT * FROM sk_loker")
    sk_loker['tanggal'] = sk_loker['tanggal'].astype(str)
    
    harmony_search = HarmonySearch(
            data=sk_loker,
            hms=10,
            n=20,
            hmcr=0.80,
            par=0.80
        )

    solution = harmony_search.search(
        keyword=keyword,
        taggar=taggar,
        max_iter=100
    )
    
    end_time = time.time()  # Catat waktu selesai eksekusi
    elapsed_time = end_time - start_time  # Hitung selisih waktu

    print(f"Elapsed Time: {elapsed_time} seconds")  # Cetak waktu eksekusi
    return solution.to_dict(orient='records')