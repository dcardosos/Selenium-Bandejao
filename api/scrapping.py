# TODO: tirar o 'segunda' que foi feito para teste
# TODO: construir a API em cima do arquivo json e mandá-lo para uma database
# TODO: considerar os outros restaurantes e os possíveis erros, visto que o `splitado` ta muito cornojob
# TODO: ainda considerar fazer isso sem selenium

from tracemalloc import stop
from selenium.webdriver import Firefox, Chrome, ChromeOptions
from time import sleep, time
from datetime import datetime
import time
import logging

logging.basicConfig(
            filename='app.log', 
            level = logging.INFO,
            format='%(asctime)s:%(levelname)s:%(message)s')

class Scrapping:
    DAYS = {
        'Monday': 'Segunda',
        'Tuesday': 'Terça',
        'Wednesday': 'Quarta',
        'Thursday': 'Quinta',
        'Friday': 'Sexta',
        'Saturday': 'Sabado',
        'Sunday': 'Domingo'
        }

    def __init__(self, ru):
        self.days = {
            'Monday': 'Segunda',
            'Tuesday': 'Terça',
            'Wednesday': 'Quarta',
            'Thursday': 'Quinta',
            'Friday': 'Sexta',
            'Saturday': 'Sabado',
            'Sunday': 'Domingo'
            }
        self.ru_codes =  {'quimica': 9, 'fisica': 8, 'central': 6}
        self.ru = self.ru_codes[ru]
        self.url = self.build_url()

        logging.info('Restaurant: {}'.format(ru))
        logging.info('Restaurant code: {}'.format(self.ru))        
        logging.info('Url used for request: {}'.format(self.url))

    def build_url(self):
        url = 'https://uspdigital.usp.br/rucard/Jsp/cardapioSAS.jsp?codrtn={}'.format(self.ru)
        return url

    def cardapio_now(self):
        logging.info('start')

        today = datetime.today()
        day = today.strftime('%A') 
        diasemana = self.days[day]
        logging.info('Day of the week: {}'.format(diasemana))

        if (diasemana == "sabado" and today.hour > 13) or diasemana == "domingo":
            return 'opa não deu certo'

        if today.hour < 14:
            snack = 'almoco'
        else:
            snack = 'jantar'
    
        logging.info('Snack picked: {}'.format(snack))

        op = ChromeOptions()
        op.add_argument('headless')

        logging.info('Begin of scrapping')
        browser = Chrome(options = op)
        browser.get(self.url)
        logging.info('Selenium log of the request: {}'.format(browser.get_log('browser')))
        
        sleep(5)
        
        self.menu = browser.find_element_by_xpath(f'//*[@id="{snack}{diasemana}"]').text
        browser.close()
        logging.info('End of scrapping')
        return self.menu

    def menu_to_json(self):
        splitado = self.menu.split("\n")

        self.json = {
            "basico": splitado[0],
            "mistura": splitado[1],
            "pvt": splitado[2],
            "salada1": splitado[3],
            "salada2": splitado[4],
            "fruta": splitado[5],
            "complemento": splitado[6]
            }
        return self.json

    def return_log(self):
        with open('app.log', 'r') as f:
            return f.readlines()