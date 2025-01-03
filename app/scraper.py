import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import logging

# Configurar logs
logging.basicConfig(level=logging.INFO)

def scrape_imoveis_requests(url):
    logging.info("Iniciando scraping com requests.")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao acessar o site: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    imoveis = []
    for card in soup.select('.ImovelCard_card__2FVbS'):
        try:
            title = card.select_one('.ImovelCardInfo_colorOfTitleCondominium__IfTu_').get_text(strip=True)
            price = card.select_one('.ImovelCardInfo_sizeOfPriceSale__KE1ms').get_text(strip=True)
            location = card.select_one('.ImovelCardInfo_colorOfLocalization__frnmZ').get_text(strip=True)
            imoveis.append({'title': title, 'price': price, 'location': location})
        except AttributeError as e:
            logging.warning(f"Erro ao processar card: {e}")
    return imoveis

def scrape_imoveis_selenium(url):
    logging.info("Iniciando scraping com Selenium.")
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        driver.implicitly_wait(10)
    except Exception as e:
        logging.error(f"Erro ao inicializar o driver Selenium: {e}")
        return []

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    imoveis = []
    for card in soup.select('.ImovelCard_card__2FVbS'):
        try:
            title = card.select_one('.ImovelCardInfo_colorOfTitleCondominium__IfTu_').get_text(strip=True)
            price = card.select_one('.ImovelCardInfo_sizeOfPriceSale__KE1ms').get_text(strip=True)
            location = card.select_one('.ImovelCardInfo_colorOfLocalization__frnmZ').get_text(strip=True)
            imoveis.append({'title': title, 'price': price, 'location': location})
        except AttributeError as e:
            logging.warning(f"Erro ao processar card: {e}")
    driver.quit()
    return imoveis

# Teste com Selenium
url = "https://www.marciacorretoradeimoveis.com/"
dados = scrape_imoveis_selenium(url)
logging.info("Resultados obtidos:")
for imovel in dados:
    print(imovel)
