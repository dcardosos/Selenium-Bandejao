# TODO: tirar o 'segunda' que foi feito para teste
# TODO: construir a API em cima do arquivo json e mandá-lo para uma database
# TODO: considerar os outros restaurantes e os possíveis erros, visto que o `splitado` ta muito cornojob
# TODO: ainda considerar fazer isso sem selenium

from tracemalloc import stop
from selenium.webdriver import Firefox, Chrome
from time import sleep
from datetime import datetime

days = {'Monday': 'Segunda',
       'Tuesday': 'Terça',
       'Wednesday': 'Quarta',
       'Thursday': 'Quinta',
       'Friday': 'Sexta',
       'Saturday': 'Sabado',
       'Sunday': 'Domingo'}

rus = {'quimica': 9, 'fisica': 8, 'central': 6}

def build_url(ru):
    url = 'https://uspdigital.usp.br/rucard/Jsp/cardapioSAS.jsp?codrtn={}'.format(rus[ru])
    return url

def cardapio_now(browser, url):
    today = datetime.today()
    day = today.strftime('%A') 
    diasemana = days[day]

    if (diasemana == "sabado" and today.hour > 13) or diasemana == "domingo":
        stop

    if today.hour < 14:
        snack = 'almoco'
    else:
        snack = 'jantar'
    
    browser.get(url)

    sleep(5)

    menu = browser.find_element_by_xpath(f'//*[@id="{snack}Segunda"]').text
    
    return menu

def menu_to_json(menu):
    splitado = menu.split("\n")

    json = {
        "basico": splitado[0],
        "mistura": splitado[1],
        "pvt": splitado[2],
        "salada1": splitado[3],
        "salada2": splitado[4],
        "fruta": splitado[5],
        "complemento": splitado[6]
        }
    return json



if __name__ == '__main__':
    chromedriver_path = "/usr/local/bin/chromedriver"
    browser = Chrome()
    ru_url = build_url('central')
    result = cardapio_now(browser, ru_url)
    browser.close()
    print(menu_to_json(result))