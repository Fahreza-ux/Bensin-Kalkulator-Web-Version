from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

def simpan_history(jenis, data1, data2, hasil):
    """Menyimpan history ke file CSV"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("history.csv", "a", encoding="utf-8") as file:
        file.write(f"{timestamp},{jenis},{data1},{data2},{hasil}\n")

@app.route('/')
def home():
    """Halaman utama"""
    return render_template('index.html')

@app.route('/hitung-konsumsi', methods=['POST'])
def hitung_konsumsi():
    """API untuk hitung konsumsi bensin"""
    try:
        # Ambil data dari form
        jarak = float(request.form['jarak'])
        bensin = float(request.form['bensin'])
        
        # Hitung konsumsi
        konsumsi = (bensin / jarak) * 100
        
        # Simpan ke history
        simpan_history("konsumsi", jarak, bensin, f"{konsumsi:.2f}")
        
        # Return hasil sebagai JSON
        return jsonify({
            'success': True,
            'hasil': f"{konsumsi:.2f}",
            'satuan': "liter/100km",
            'detail': f"Untuk jarak {jarak} km dengan {bensin} liter bensin"
        })
        
    except Exception as e:
        return jsonify({
            'success': False, 
            'error': 'Input harus angka!'
        })

@app.route('/hitung-jarak', methods=['POST'])
def hitung_jarak():
    """API untuk hitung jarak tempuh"""
    try:
        # Ambil data dari form
        bensin = float(request.form['bensin'])
        konsumsi = float(request.form['konsumsi'])
        
        # Hitung jarak
        jarak = (bensin / konsumsi) * 100
        
        # Simpan ke history
        simpan_history("jarak", bensin, konsumsi, f"{jarak:.2f}")
        
        # Return hasil sebagai JSON
        return jsonify({
            'success': True,
            'hasil': f"{jarak:.2f}",
            'satuan': "km", 
            'detail': f"Dengan {bensin} liter dan konsumsi {konsumsi} L/100km"
        })
        
    except Exception as e:
        return jsonify({
            'success': False, 
            'error': 'Input harus angka!'
        })

if __name__ == '__main__':
    app.run(debug=True)
