from flask import Flask, render_template, request, redirect, send_file, session, jsonify
import pandas as pd
import json
import mysql.connector
import numpy as np
import random

app = Flask("Lowongan Pekerjaan")

def generate_random_solution():
    # Implementasi pembangkitan solusi acak
    nama_loker = "random_nama_loker"
    perusahaan = "random_perusahaan"
    deskripsi = "random_deskripsi"
    kategori = "random_kategori"
    gaji = "random_gaji"
    tanggal = "random_tanggal"
    source = "random_source"
    created_by = "random_created_by"
    return [nama_loker, perusahaan, deskripsi, kategori, gaji, tanggal, source, created_by]

def evaluate_solution(conn, table, solution):
    # Implementasi evaluasi solusi
    nama_loker = solution[0]
    perusahaan = solution[1]

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM {} WHERE nama_loker=%s and perusahaan=%s".format(table), (nama_loker, perusahaan,))
    count = cursor.fetchone()[0]
    cursor.close()

    return count

def harmony_search(conn, table, hmcr, par):
    lower_bound = 32
    upper_bound = 126
    memory_size = 50
    max_iter = 50
    
    harmony_memory = []

    for i in range(memory_size):
        solution = generate_random_solution()
        if evaluate_solution(conn, table, solution) == 0:
            harmony_memory.append(solution)
    
    for iteration in range(max_iter):
        if random.random() < hmcr and len(harmony_memory) > 0:
            idx = random.randint(0, len(harmony_memory)-1)
            new_solution = harmony_memory[idx].copy()
        else:
            new_solution = generate_random_solution()
        
        for j in range(len(new_solution)):
            if random.random() < par:
                new_solution[j] = random.randint(lower_bound, upper_bound)
        
        if evaluate_solution(conn, table, new_solution) == 0:
            harmony_memory.append(new_solution)
            if len(harmony_memory) > memory_size:
                worst_index = harmony_memory.index(max(harmony_memory, key=len))
                harmony_memory.pop(worst_index)
    
    if len(harmony_memory) == 0:
        return None
    else:
        best_solution = min(harmony_memory, key=len)
        return best_solution

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
    df=df.drop(["perusahaan_lokasi"],axis=1)
    df.to_excel("tes.xlsx")
    if input_json['tanggal_awal'] != '' and input_json['tanggal_akhir'] != '':
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
    
    hmcr = 0.8  # Nilai HMCR (Harmony Memory Considering Rate)
    par = 0.3  # Nilai PAR (Pitch Adjustment Rate)
    
    for i in range(len(df)):
        if df.iloc[i]["lowongan_pekerjaan"] == "":
            continue
        
        data = [df.iloc[i]["lowongan_pekerjaan"], df.iloc[i]["nama_perusahaan"], df.iloc[i]["job_desk"], df.iloc[i]["kategori_awal"], df.iloc[i]["gaji"], df.iloc[i]["tanggal_terbit"], df.iloc[i]["detail_situs"], "0"]
        table = "sk_loker"
        
        best_solution = harmony_search(conn, table, hmcr, par)
        if best_solution is None:
            cursor = conn.cursor()
            cursor.execute("UPDATE {} SET status='LAMA' WHERE kategori='{}'".format(table, df.iloc[i]["kategori_awal"]))
            conn.commit()
            cursor.close()
        else:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO {} (nama_loker, perusahaan, deskripsi, kategori, gaji, tanggal, source, created_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)".format(table), (best_solution[0], best_solution[1], best_solution[2], best_solution[3], best_solution[4], best_solution[5], best_solution[6], best_solution[7], "BARU"))
            conn.commit()
            cursor.close()
    
    conn.close()
    hasil_konversi = df.to_json(orient="records")
    data_json = json.loads(hasil_konversi)
    
    return data_json

@app.route("/search")
def search():
    db = {}
    keyword = request.args.get("keyword")
    taggar = request.args.get("taggar")
    if keyword == None or keyword == '':
        if taggar == None:
            return redirect("/")

    if keyword in db:
        jobs = db[keyword]
    else:
        jobs = data_lowongan_jobsid(keyword, taggar) + data_lowongan_glints(keyword, taggar) + data_lowongan_jobstreet(
            keyword, taggar) + data_lowongan_karir(keyword, taggar) + data_lowongan_loker(keyword, taggar)
        # jobs = data_lowongan_loker(keyword, taggar)
        print(jobs)

        db[keyword] = jobs

    return render_template("cari.html", kata_kunci=keyword, jobs=jobs)

app.run(debug=True, threaded=True, port=5001)
