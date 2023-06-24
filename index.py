from flask import Flask, render_template, request, redirect, send_file, session, jsonify
import pandas as pd
import json
import mysql.connector
import numpy as np
import random
import datetime

# Pustaka Website Lowongan
from website_lowongan.jobs_id import data_lowongan_jobsid
from website_lowongan.glints import data_lowongan_glints
from website_lowongan.jobstreet import data_lowongan_jobstreet
from website_lowongan.karir import data_lowongan_karir
from website_lowongan.loker import data_lowongan_loker

app = Flask("Lowongan Pekerjaan")

def generate_date_range():
    # Mendapatkan tanggal awal bulan saat ini
    today = datetime.date.today()
    start_date = datetime.date(today.year, today.month, 1)

    # Mendapatkan tanggal akhir bulan saat ini
    next_month = start_date.replace(day=28) + datetime.timedelta(days=4)  # Mendapatkan tanggal awal bulan berikutnya
    end_date = next_month - datetime.timedelta(days=next_month.day)

    # Membuat rentang tanggal dari awal bulan hingga akhir bulan
    date_range = []
    current_date = start_date
    while current_date <= end_date:
        date_range.append(current_date.strftime('%Y-%m-%d'))
        current_date += datetime.timedelta(days=1)

    return date_range

def generate_random_solution(date_range):
    # Implementasi pembangkitan solusi acak
    nama_loker = "random_nama_loker"
    perusahaan = "random_perusahaan"
    deskripsi = "random_deskripsi"
    kategori = "random_kategori"
    gaji = "random_gaji"
    tanggal = random.choice(date_range)
    source = "random_source"
    created_by = "random_created_by"
    return [nama_loker, perusahaan, deskripsi, kategori, gaji, tanggal, source, created_by]

def evaluate_solution(conn, table, solution):
    nama_loker = solution[0]
    perusahaan = solution[1]
    tanggal = solution[5]

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM {} WHERE nama_loker=%s AND perusahaan=%s AND tanggal=%s".format(table), (nama_loker, perusahaan, tanggal))
    count = cursor.fetchone()[0]
    
    # Update status data lama jika solusi sudah ada dalam tabel
    if count > 0:
        cursor.execute("UPDATE {} SET status='LAMA' WHERE nama_loker=%s AND perusahaan=%s AND tanggal=%s".format(table), (nama_loker, perusahaan, tanggal))
        conn.commit()
    
    cursor.close()

    return count

def get_existing_solution(conn, table, solution):
    nama_loker = solution[0]
    perusahaan = solution[1]
    tanggal = solution[5]
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM {} WHERE nama_loker=%s AND perusahaan=%s AND tanggal=%s".format(table), (nama_loker, perusahaan, tanggal))
    result = cursor.fetchone()
    cursor.close()
    
    return result

def harmony_search(conn, table, hmcr, par, date_range, data):
    lower_bound = 32
    upper_bound = 126
    memory_size = 50
    max_iter = 50
    
    harmony_memory = []

    for i in range(memory_size):
        solution = generate_random_solution(date_range)
        if evaluate_solution(conn, table, solution) == 0:
            harmony_memory.append(solution)
    
    for iteration in range(max_iter):
        if random.random() < hmcr and len(harmony_memory) > 0:
            idx = random.randint(0, len(harmony_memory)-1)
            new_solution = harmony_memory[idx].copy()
        else:
            new_solution = generate_random_solution(date_range)
        
        for j in range(len(new_solution)):
            if random.random() < par:
                new_solution[j] = random.randint(lower_bound, upper_bound)
        
        if evaluate_solution(conn, table, new_solution) == 0:
            harmony_memory.append(new_solution)
            if len(harmony_memory) > memory_size:
                worst_index = harmony_memory.index(max(harmony_memory, key=len))
                harmony_memory.pop(worst_index)
        else:
            # Solusi sudah ada, update status data lama
            existing_solution = get_existing_solution(conn, table, new_solution)
            if existing_solution is not None:
                existing_solution = existing_solution[:-1] + ["LAMA"]  # Update status menjadi "LAMA"
                cursor = conn.cursor()
                cursor.execute("UPDATE {} SET status=%s WHERE nama_loker=%s AND perusahaan=%s AND tanggal=%s".format(table), tuple(existing_solution))
                conn.commit()
                cursor.close()
            continue
    
    if len(harmony_memory) == 0:
        return None
    else:
        best_solution = min(harmony_memory, key=len)
        nama_loker = best_solution[0]
        perusahaan = best_solution[1]
        tanggal = best_solution[5]

        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM {} WHERE nama_loker=%s AND perusahaan=%s AND tanggal=%s".format(table), (nama_loker, perusahaan, tanggal))
        count = cursor.fetchone()[0]

        if count == 0:  # Data is new, insert it
            cursor.execute("INSERT INTO {} (nama_loker, perusahaan, deskripsi, kategori, gaji, tanggal, source, created_by, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)".format(table), tuple(data + ["BARU"]))
            conn.commit()
        else:  # Data already exists, update the status to "LAMA"
            cursor.execute("UPDATE {} SET status='LAMA' WHERE nama_loker=%s AND perusahaan=%s AND tanggal=%s".format(table), (nama_loker, perusahaan, tanggal))
            conn.commit()

        cursor.close()

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
    # df.to_excel("filter.xlsx")
    date_range = generate_date_range()
    
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
        
        data = [df.iloc[i]["lowongan_pekerjaan"], df.iloc[i]["nama_perusahaan"], df.iloc[i]["job_desk"], df.iloc[i]["kategori_awal"], df.iloc[i]["gaji"],df.iloc[i]["tanggal_terbit"], df.iloc[i]["detail_situs"], "0"]
        harmony_search(conn, "sk_loker", hmcr, par, date_range, data)
    
    conn.close()
    hasil_konversi = df.to_json(orient="records")
    
    data_json = json.loads(hasil_konversi)
    return jsonify(data=data_json)

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
        db[keyword] = jobs

    return render_template("search.html", keyword=keyword, taggar=taggar, jobs=jobs)

if __name__ == '__main__':
    app.run(debug=True)
