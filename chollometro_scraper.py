import time
import csv
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

# Init the webdriver
driver = webdriver.Chrome(ChromeDriverManager().install())

def getChollosByCategory(pages,option=""):
    lista_chollos = {}
    cont = 1

    # Run all the pages
    for i in range(1,pages+1):
        # Obtenemos la url de forma dinamica
        driver.get('https://www.chollometro.com/%s?page=%s' % (option, i))
        
        # We add sleep to get all the html
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find and get all the deals
        items = soup.find_all('div', {'class', 'thread-clickRoot'})

        # Run each deal info
        for item in items:

            # Name
            nombre = item.find(class_='thread-link').text.strip()

            # Comentaries
            comentarios = item.find(class_='cept-comment-link').text.strip()

            # Shop
            tienda = item.find(class_='cept-merchant-name').text.strip()

            # Owner
            creador = item.find(class_='thread-username').text.strip()

            # Link
            enlace = item.a['href']

            # Votes
            if item.find(class_='cept-vote-temp')!= None:
                votos = item.find(class_='cept-vote-temp').text[:-5].strip()
            elif item.find(class_='space--h-2') != None:
                votos = item.find(class_='text--b').text[:-5].strip()

            # Price
            if item.find(class_='mute--text') != None:
                precio = item.find(class_='mute--text').text[:-1].strip()
            else:
                precio = 0

            # Sold out
            if item.find(class_='cept-show-expired-threads') != None:
                agotado = 'Si'
            else:
                agotado = 'No'

            lista_chollos['chollo_%s' % cont] = {
                'nombre':nombre,
                'votos':votos,
                'precio':precio,
                'comentarios':comentarios,
                'enlace':enlace,
                'tienda':tienda,
                'creador':creador,
                'agotado':agotado
            }

            cont = cont + 1
            
    return lista_chollos

def getCholloDetail(enlace):
    # Init our webdriver
    driver.get(enlace)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    lista_detalle = []
    lista_clases = ['text--b','cept-vote-temp','thread-price','size--all-xxl','thread-username']

    for i in lista_clases:
        lista_detalle.append(soup.find('span', {'class','%s' % i}).text.strip())

    lista_detalle.append(soup.find('div', {'class','space--mt-3'}).a['href'])

    driver.close()

    return lista_detalle


def write_csv(lista_chollos):
    # Write the obtained list in getChollosByCategory method to our csv file
    with open('csv_file.csv','a', encoding='UTF-8') as f:
        header = ['nombre','votos','precio','precio_oferta','comentarios']
        writer = csv.writer(f)
        writer.writerow(header)

        for i in lista_chollos.keys():
            lista_aux = []
            for j in lista_chollos[i].keys():
                lista_aux.append(lista_chollos[i].get(j))

            writer.writerow(lista_aux)

getChollosByCategory(1,"populares")
# x = getCholloDetail('https://www.chollometro.com/ofertas/recopilacion-de-sombras-de-ojos-bourjois-little-round-desde-551-euros-783139')
# print(x)
# write_csv(lista_chollos)
