from app.api import app
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    logging.info("Iniciando o servidor Flask...")
    app.run(debug=True)
