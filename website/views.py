#flask libraries
from flask import Blueprint, render_template, request, jsonify, redirect, url_for

#selenium libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#other libraries
from datetime import datetime
import requests
import time
import os
import website.models as bd

views = Blueprint('views', __name__)

def mailsend(mes, ano):
    api_key = '*****'
    domain = '*****'
    
    return requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", api_key),
        data={"from": f"abiec <mailgun@{domain}>",
              "to": ["****, ****, ****"],
              "subject": "Atualização dados Comex Stat",
              "text": f"Os dados de {mes}/{ano} já estão disponíveis!"})
    
  
@views.route('/')
def index():
    
    #CODIGO PARA RODAR LOCAL
    #PATH = 'C:\Program Files (x86)\chromedriver.exe'
    #s=Service(PATH)
    #driver = webdriver.Chrome(service=s)
    
    #options = webdriver.ChromeOptions()
    #options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #driver = webdriver.Chrome(options=options, service=s)
    
    #CODIGO PARA RODAR NO HEROKU
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    
    
    driver.get("http://comexstat.mdic.gov.br/pt/home")
    

    wait = WebDriverWait(driver, 5)
    
    
    #Clicar botao 'acessar dados'

    #element = wait.until(
        #EC.presence_of_element_located(
           #(By.XPATH,'//button[text()="Acesse os Dados"]')
        #)
    #)
    
    #element.click()
    
    #Verficar link de data        
    links = wait.until(
        EC.presence_of_all_elements_located(
           (By.XPATH,"//small[starts-with(text(), 'Dados disponíveis até')]")
        )
    )


    
    #Comparar datas sistema e comexstat
    link_mes = links[0].text[-8:-6]
    link_ano = links[0].text[-4:]
    
    mes = str(datetime.today())[5:7]
    ano = str(datetime.today())[0:4]
    
    
    #Criar banco de dados
    bd.create_db()
    alerta = ''
    
    #Atualizar banco e disparar email
    if (int(link_mes) == int(mes)-1 and link_ano == ano) or (int(link_mes) == 12 and int(mes)==1 and link_ano != ano):
        
        data = str(mes) + '-' + str(ano)
        
        list_item = bd.select_db()
        
        if list_item:
            
            item = bd.select_db()[-1]
            item = (((str(item).replace('(', '')).replace(')','')).replace(',','')).replace("'", "")
        
            if data != item:
                bd.insert_db(data)
                mailsend(mes, ano)
                time.sleep(5)
                driver.quit()
                alerta = 'Email(s) enviado(s) com sucesso!'
            else:
                alerta = 'Registro já existente!'
                time.sleep(5)
                driver.quit()
                
        else:
            bd.insert_db(data)
            mailsend(mes, ano)
            time.sleep(5)
            driver.quit()
            alerta = 'Banco criado. Email(s) enviado(s) com sucesso!'
                
        return render_template('index.html', message=alerta)
                
    else:
        time.sleep(5)
        driver.quit()
        alerta = 'Não foi possível enviar o(s) email(s). Atualização não disponível!'
        
        return render_template('index.html', message=alerta)