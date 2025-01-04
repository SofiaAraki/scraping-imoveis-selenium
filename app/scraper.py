import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import logging

# Configurar logs
logging.basicConfig(level=logging.INFO)

def scrape_imoveis(url, use_selenium=False):
    logging.info(f"Iniciando scraping para {url} com {'Selenium' if use_selenium else 'requests'}.")
    
    page_source = None
    driver = None
    
    try:
        if use_selenium:
            # Configuração do WebDriver
            driver = webdriver.Chrome()
            driver.get(url)
            driver.implicitly_wait(10)
            page_source = driver.page_source
        else:
            response = requests.get(url)
            response.raise_for_status()
            page_source = response.text

        # Parsear o HTML
        soup = BeautifulSoup(page_source, 'html.parser')
        imoveis = []

        for card in soup.select('.imovelcard'):  # Ajuste os seletores conforme necessário
            try:
                title = card.select_one('.imovelcard__info__tag').get_text(strip=True)
                price = card.select_one('.imovelcard__valor__valor').get_text(strip=True)
                location = card.select_one('.imovelcard__info__local').get_text(strip=True)
                imoveis.append({'title': title, 'price': price, 'location': location})
            except AttributeError as e:
                logging.warning(f"Erro ao processar card: {e}")

        return imoveis

    except Exception as e:
        logging.error(f"Erro durante o scraping: {e}")
        return []
    finally:
        if driver:
            driver.quit()

def scrape_all_pages(base_url, use_selenium=False):
    current_page = 1
    all_data = []

    while True:
        logging.info(f"Carregando página {current_page}...")
        url = f"{base_url}?pag={current_page}"  # Ajuste o parâmetro de paginação, se necessário
        data = scrape_imoveis(url, use_selenium=use_selenium)
        
        if not data:  # Se nenhuma informação for encontrada, terminamos
            break

        all_data.extend(data)
        current_page += 1

    return all_data

def scrape_both_types(base_url_venda, base_url_locacao, use_selenium=False):
    # Scraping de imóveis para venda
    logging.info("Iniciando scraping para imóveis de venda...")
    imoveis_venda = scrape_all_pages(base_url_venda, use_selenium)
    
    # Scraping de imóveis para locação
    logging.info("Iniciando scraping para imóveis de locação...")
    imoveis_locacao = scrape_all_pages(base_url_locacao, use_selenium)
    
    # Combinando os dados de venda e locação
    all_imoveis = imoveis_venda + imoveis_locacao
    return all_imoveis

# Teste
if __name__ == "__main__":
    # Defina as URLs para venda e locação
    url_venda = "https://www.luisgpassarelaimoveis.com.br/imovel/venda"
    url_locacao = "https://www.luisgpassarelaimoveis.com.br/imovel/locacao"
    
    # Scraping de imóveis de venda e locação
    all_imoveis = scrape_both_types(url_venda, url_locacao, use_selenium=True)
    
    logging.info(f"Total de imóveis encontrados: {len(all_imoveis)}")
    for imovel in all_imoveis:
        print(imovel)
