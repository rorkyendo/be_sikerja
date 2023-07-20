# Pencarian Lowongan Pekerjaan dengan Harmony Search

Aplikasi ini dibangun dengan `python 3.10.12` dan semua library yang digunakan bisa dilihat di `requirements.txt`.

Sebelum menjalankan aplikasinya, hal pertama yang perlu dilakukan adalah mengatur environment variabel `.flaskenv`. Yang perlu diatur adalah databasenya. Selain itu, di repo ini disediakan data dummya pada folder ` data``. Jika databasenya sudah ada bisa import  `dummy_sk_loker.csv`ke tabel`sk_loker`. Jika belum ada maka disediakan juga dump database di file `dummy_data.sql`

Untuk menjalankan ikuti perintah berikut

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
python index.py
```

Aplikasi akan berjalan di port 5000. Sehingga bisa diakses di `http://localhost:5000`. Aplikasi ini akan mengandung 3 route

1. `/`, merupakan halaman home, berisi isian search
2. `/search`, merupakan hasil pencarian dalam bentuk halaman website. Jika request dilakukan pada route ini maka akan dilakukan scaraping terlebih dahulu sebelum melakukan harmony search.
3. `/find`, merupakan hasil pencarian harmony search dalam bentuk json. Misalnya melakukan request ke `http://127.0.0.1:5000/find?keyword=Data&taggar=Keuangan`
