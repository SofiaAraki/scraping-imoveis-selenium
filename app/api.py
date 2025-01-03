from flask import Flask, jsonify
from app.scraper import scrape_imoveis_selenium

app = Flask(__name__)

@app.route('/api/imoveis')
def get_imoveis():
    print("Rota /api/imoveis acessada")
    url = "https://www.marciacorretoradeimoveis.com/"
    imoveis = scrape_imoveis_selenium(url)
    print(f"Imóveis extraídos: {imoveis}")
    return jsonify(imoveis)
