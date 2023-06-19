# Pustaka Umum
from flask import Flask, render_template, request, redirect, send_file, session, jsonify
import pandas as pd
import json
import mysql.connector
import numpy as np

# Pustaka Website Lowongan
from website_lowongan.jobs_id import data_lowongan_jobsid
from website_lowongan.glints import data_lowongan_glints
from website_lowongan.jobstreet import data_lowongan_jobstreet
from website_lowongan.karir import data_lowongan_karir
from website_lowongan.loker import data_lowongan_loker

app = Flask("Lowongan Pekerjaan")

import random

def harmony_search(conn, table, solution):
    # Menentukan rentang nilai untuk setiap dimensi solusi
    lower_bound = 32
    upper_bound = 126
    # Menentukan ukuran memori harmoni
    memory_size = 50
    # Menentukan jumlah maksimum iterasi
    max_iter = 50
    
    # Menginisialisasi memori harmoni
    harmony_memory = []
    for i in range(memory_size):
        # Menghasilkan string acak
        new_solution = generate_random_solution(lower_bound, upper_bound)
        
        # Memeriksa apakah solusi sudah ada dalam database
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM {} WHERE nama_loker=%s AND perusahaan=%s".format(table), (new_solution[0], new_solution[1],))
        if cursor.fetchone()[0] == 0:
            # Jika solusi belum ada, tambahkan ke memori harmoni
            harmony_memory.append(new_solution)
        cursor.close()
    
    # Melakukan iterasi hingga mencapai jumlah maksimum iterasi
    for iteration in range(max_iter):
        # Menghasilkan solusi kandidat baru
        new_solution = generate_new_solution(harmony_memory, lower_bound, upper_bound)
        
        # Memeriksa apakah solusi sudah ada dalam database
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM {} WHERE nama_loker=%s AND perusahaan=%s".format(table), (new_solution[0], new_solution[1],))
        if cursor.fetchone()[0] == 0:
            # Jika solusi belum ada, tambahkan ke memori harmoni
            harmony_memory.append(new_solution)
            # Menghapus solusi terburuk dari memori harmoni
            if len(harmony_memory) > memory_size:
                worst_index = harmony_memory.index(max(harmony_memory, key=len))
                harmony_memory.pop(worst_index)
        cursor.close()
    
    # Memasukkan solusi terbaik ke dalam database
    if len(harmony_memory) == 0:
        return 0
    else:
        best_solution = min(harmony_memory, key=len)
        
        # Memasukkan solusi terbaik ke dalam database
        cursor = conn.cursor()
        cursor.execute("INSERT INTO {} (nama_loker, perusahaan, deskripsi, kategori, gaji, tanggal, source, created_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)".format(table), (best_solution[0], best_solution[1], best_solution[2], best_solution[3], best_solution[4], best_solution[5], best_solution[6], best_solution[7], "BARU"))
        conn.commit()
        cursor.close()
        
        return best_solution


def generate_random_solution(lower_bound, upper_bound):
    nama_loker = random.randint(lower_bound, upper_bound)
    perusahaan = random.randint(lower_bound, upper_bound)
    deskripsi = random.randint(lower_bound, upper_bound)
    kategori = random.randint(lower_bound, upper_bound)
    gaji = random.randint(lower_bound, upper_bound)
    tanggal = random.randint(lower_bound, upper_bound)
    source = random.randint(lower_bound, upper_bound)
    created_by = random.randint(lower_bound, upper_bound)
    return [nama_loker, perusahaan, deskripsi, kategori, gaji, tanggal, source, created_by]


def generate_new_solution(harmony_memory, lower_bound, upper_bound, hmcr=0.9):
    new_solution = []
    for i in range(len(harmony_memory[0])):
        if random.random() < hmcr:
            # Memilih nilai acak dari memori harmoni
            random_index = random.randint(0, len(harmony_memory) - 1)
            value = harmony_memory[random_index][i]
        else:
            # Menghasilkan nilai acak dalam rentang
            value = random.randint(lower_bound, upper_bound)
        new_solution.append(value)
    return new_solution


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/post', methods=["POST"])
def testpost():
    input_json = request.get_json(force=True)
    
    dictToReturn = data_lowongan_jobsid(input_json['keyword'], input_json['taggar']) + data_lowongan_glints(input_json['keyword'], input_json['taggar']) + data_lowongan_jobstreet(
        input_json['keyword'], input_json['taggar']) + data_lowongan_karir(input_json['keyword'], input_json['taggar']) + data_lowongan_loker(input_json['keyword'], input_json['taggar'])
    df = pd.DataFrame(dictToReturn)
    df = df.replace('\n', ' ', regex=True)
    
    df['nama_perusahaan'] = df['perusahaan_lokasi'].str.encode('ascii', 'ignore').str.decode('ascii')
    df.columns = df.columns.str.strip()
    df["nama_perusahaan"] = df["nama_perusahaan"].str.replace(r'\s+', ' ', regex=True)
    df["gaji"] = df["gaji"].str.replace(r'\s+', ' ', regex=True)
    df["job_desk"] = df["job_desk"].str.replace(r'\s+', ' ', regex=True)
    df["kategori_awal"] = input_json['taggar']
    df = df.drop(["perusahaan_lokasi"], axis=1)
    df.to_excel("tes.xlsx")
    tanggal_awal = input_json['tanggal_awal']
    tanggal_akhir = input_json['tanggal_akhir']
    df = df.query('tanggal_terbit >= @tanggal_awal and tanggal_terbit <= @tanggal_akhir')
    df.to_excel("filter.xlsx")
    
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sikerja"
    )
    
    cursor = conn.cursor()
    for i in range(len(df)):
        if df.iloc[i]["lowongan_pekerjaan"] == "":
            continue
        
        data = [df.iloc[i]["lowongan_pekerjaan"], df.iloc[i]["nama_perusahaan"], df.iloc[i]["job_desk"], df.iloc[i]["kategori_awal"], df.iloc[i]["gaji"], df.iloc[i]["tanggal_terbit"], df.iloc[i]["detail_situs"], "0"]
        table = "sk_loker"
        solution = [random.randint(32, 126), random.randint(32, 126), random.randint(32, 126), random.randint(32, 126), random.randint(32, 126), random.randint(32, 126), random.randint(32, 126), random.randint(32, 126)]
        
        best_solution = harmony_search(conn, table, solution)
        if best_solution == 0:
            continue
        
        data.append(best_solution)
        
        cursor.execute("INSERT INTO {} (nama_loker, perusahaan, deskripsi, kategori, gaji, tanggal, source, created_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)".format(table), (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], "BARU"))
        conn.commit()
    
    cursor.close()
    conn.close()
    
    return jsonify({"status": "success"})


if __name__ == "__main__":
    app.run(port=8000, debug=True)
