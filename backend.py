from flask import Flask, jsonify, request
import re
import os

app = Flask(__name__)

# SQL dosyasını oku
def load_papara_data():
    data = []
    try:
        with open('final.sql', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('('):
                    match = re.search(r'\((\d+),\s*(\d+),\s*\'(.*?)\'', line)
                    if match:
                        data.append({
                            'id': match.group(1),
                            'numara': match.group(2),
                            'ad_soyad': match.group(3)
                        })
        return data
    except:
        return []

papara_data = load_papara_data()

@app.route('/')
def home():
    return "F3 System API"

@app.route('/f3system/api/papara')
def papara_api():
    paparano = request.args.get('paparano', '')
    ad = request.args.get('ad', '')
    soyad = request.args.get('soyad', '')
    
    if not paparano and not ad and not soyad:
        return jsonify({
            "error": "En az bir parametre gerekli",
            "ornekler": [
                "/f3system/api/papara?paparano=1977050442",
                "/f3system/api/papara?ad=UFUK&soyad=DEMİR",
                "/f3system/api/papara?ad=UFUK"
            ]
        }), 400
    
    results = []
    
    for item in papara_data:
        match = True
        
        if paparano and paparano not in item['numara']:
            match = False
        
        if ad and ad.upper() not in item['ad_soyad'].upper():
            match = False
            
        if soyad and soyad.upper() not in item['ad_soyad'].upper():
            match = False
        
        if match:
            results.append(item)
    
    return jsonify({
        "sorgu": {
            "paparano": paparano,
            "ad": ad,
            "soyad": soyad
        },
        "sonuc_sayisi": len(results),
        "sonuclar": results[:50]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
