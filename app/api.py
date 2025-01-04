from flask import Flask, jsonify, request
from flask_cors import CORS
from app.scraper import scrape_imoveis
import logging

app = Flask(__name__)
CORS(app)  # Permitir requisições de qualquer origem
logging.basicConfig(level=logging.INFO)

@app.route('/api/imoveis')
def get_imoveis():
    logging.info("Rota /api/imoveis acessada")
    
    try:
        # Obter o filtro de localização
        location_filter = request.args.get("location", "").strip().lower()

        # Definir as URLs de venda e locação
        url_venda = "https://www.luisgpassarelaimoveis.com.br/imovel/venda"
        url_locacao = "https://www.luisgpassarelaimoveis.com.br/imovel/locacao"
        
        # Buscar imóveis de venda e locação
        imoveis_venda = scrape_imoveis(url_venda)
        imoveis_locacao = scrape_imoveis(url_locacao)
        
        # Combinar os resultados de venda e locação
        imoveis = imoveis_venda + imoveis_locacao
        
        # Filtrar os imóveis pela localização, se fornecido
        if location_filter:
            imoveis = [
                item for item in imoveis
                if location_filter in item["location"].lower()
            ]
        
        logging.info(f"{len(imoveis)} imóveis encontrados (venda e locação).")
        return jsonify(imoveis)

    except Exception as e:
        logging.error(f"Erro ao buscar imóveis: {e}")
        return jsonify({"error": "Não foi possível buscar os imóveis no momento."}), 500
