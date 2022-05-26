import requests
import os
from bs4 import BeautifulSoup
from babel.numbers import format_currency

countries = []
#user-agent setting
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"
headers = {'User-Agent': user_agent}

def find_countries():
  url = "https://www.iban.com/currency-codes"


  request = requests.get(url)
  soup = BeautifulSoup(request.text, 'html.parser')

  table = soup.find("table")
  rows = table.find_all("tr")[1:]

  for row in rows:
    items = row.find_all("td")
    name = items[0].text
    code = items[2].text
    if code != "":
      country = {
      'name': name,
      'code': code
      }
      countries.append(country)
    
def menu():
  find_countries()
  for index, country in enumerate(countries):
    print(f"{index} -> {country['name']}")
  
  print("Bem-vindo ao negociador de Moedas!!")
  print("Escolha os numeros dos paises que deseja negociar!\n")
  try:
    choice = int(input())
    if choice > len(countries):
      print("nao tem, escolha um item da lista")
    else:
      country = countries[choice]
      print(f"(x) {country['name']} \nMoeda: {country['code']}")
      choice_1 = country['code']
      print("Para qual país quer converter?")
      try:
        choice = int(input())
        country = countries[choice]
        print(f"(x) {country['name']} \nMoeda: {country['code']}")
        choice_2 = country['code']
        return convert(choice_1,choice_2)
      except:
        print("Voce tem que digitar um numero!")
    
  except:
    print("Voce tem que digitar um numero!")

 
def convert(choice_1,choice_2):
  valor = int(input("Digite o valor a ser convertido \n"))
  url = f"https://wise.com/gb/currency-converter/{choice_1}-to-{choice_2}-rate?amount={valor}"
  r_url = requests.get(url, headers={'User-Agent': user_agent})
  soup = BeautifulSoup(r_url.text, "html.parser")
  rate = float(soup.find('span', class_='text-success').string)
  rate_math = valor * rate
  print(format_currency(rate_math, choice_2))
  restart()

def restart():
    option = input("Deseja converter mais alguma moeda? S/n\n").lower()
    
    if option == "s":
      os.system('clear')
      menu()
      
    elif option == "n":
      print("Programa finalizado")
    else:
      print("Opção invalida!")
      restart()

menu()

