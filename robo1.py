from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.select import Select
import csv
from PIL import Image
from pytesseract import image_to_string
from string import ascii_letters, digits
import ssl
from collections import Counter

def cutImage():
    driver.save_screenshot('scr.png')
    im = Image.open("scr.png")
    left = 300
    top = 920
    right = 700
    bottom = 976
    return im.crop((left, top, right, bottom))

def obter_caracteres(imagem):
    caracteres = [list() for _ in range(6)]
    resultados = tentar_layouts(imagem)
    for posicao in range(6):
        for resultado in resultados:
            for indice, caractere in enumerate(caracteres):
                try:
                    caractere.append(resultado[indice])
                except IndexError:
                    pass
    return caracteres

def tentar_layouts(imagem):
    resultados = []
    layouts = [8, 9, 10]
    for layout in layouts:
        resultados.append(reconhecer_caracteres(imagem, layout))
    return resultados

def reconhecer_caracteres(imagem, layout):
    return image_to_string(imagem, config=f"""--psm {layout} -c tessedit_char_whitelist={ascii_letters + digits}""")

def contar_caracteres(listas):
    for lista in listas:
        mais_comuns = [list() for _ in range(len(listas))]
        for indice, _ in enumerate(mais_comuns):
            try:
                mais_comuns[indice] = Counter(listas[indice]).most_common()[0][0]
            except IndexError:
                pass
    return mais_comuns

def solucionandoCaptchar(captcha):
    img = captcha.convert("1")
    resultados = obter_caracteres(img)
    return contar_caracteres(resultados)

def gerarCsv(cont):
    print("Gravando dados no arquivo dados.csv...")
    with open("dados.csv", "w", newline="") as data:
        escritor = csv.writer(data)
        escritor.writerow(["id", "comprador", "descrição", "link"])
        for c in range(cont):
            indice = c + 1
            xPathDescricao = "//*[@id='tCompradores']/tbody/tr[" + str(indice) + "]/td[4]"
            xPathid = "//*[@id='tCompradores']/tbody/tr[" + str(indice) + "]/td[3]"
            xPathcomprador = "//*[@id='tCompradores']/tbody/tr[" + str(indice) + "]/td[2]"
            id = driver.find_element_by_xpath(xPathid).text
            comprador = driver.find_element_by_xpath(xPathcomprador).text
            xPathHref = "//*[@id='" + id + "']"
            descricao = driver.find_element_by_xpath(xPathDescricao).text
            path = driver.find_element_by_xpath(xPathHref).get_attribute('onclick').split("'")[1]
            escritor.writerow([id, comprador, descricao, path])
            print(comprador)

#definição de constantes
ssl._create_default_https_context = ssl._create_unverified_context
url = "https://www.licitacoes-e.com.br/aop/pesquisar-licitacao.aop?opcao=preencherPesquisar"
xpath_situacao = "//*[@id='licitacaoPesquisaSituacaoForm']/div[5]/span/input"
xpath_captchar = "//*[@id='pQuestionAvancada']"
xpath_quantidade = "//*[@id='conteudo']/fieldset/legend"
xpath_total_por_pagina = "//*[@id='tCompradores_length']/label/select"

print("Iniciando robo...")
print("Conectando a url " + url)
driver = webdriver.Chrome()
driver.get(url)

time.sleep(4)

campo = driver.find_element_by_xpath(xpath_situacao)
campo.clear()
campo.send_keys("Publicada")

div = driver.find_element_by_xpath("//*[@id='bodyPrincipal']")
div.send_keys(Keys.END)

print("Print screen da tela...")
image_cut = cutImage()
print("Completando o captchar...")
captchar = driver.find_element_by_xpath(xpath_captchar)
solved_captchar = solucionandoCaptchar(image_cut)
#captchar.send_keys(solved_captchar)
#captchar.send_keys("ghb26")
captchar.send_keys(Keys.RETURN)

time.sleep(2)

qtdade = driver.find_element_by_xpath(xpath_quantidade).text.split('(')[1].split(')')[0]
print(qtdade + " resultados capturados na pesquisa.")

print("Mostrando todos por página...")
select = Select(driver.find_element_by_xpath(xpath_total_por_pagina))
select.select_by_visible_text("Todos")
cont = int(driver.find_element_by_xpath("//*[@id='tCompradores_info']").text.split(' ')[4])

gerarCsv(cont)
print("Extração concluida...")
driver.close()