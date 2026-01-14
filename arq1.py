import requests
import json
try:
    with open("siglas_paises.json","r",encoding="utf-8") as p:
        paises_siglas = json.load(p)
except FileNotFoundError:
    paises_siglas = {}


def buscar_clima(cidade):
    api_key = "389d09e6c175d65ddd691535ab080dc1"

    # O parâmetro units=metric serve para vir em Celsius
    # O parâmetro lang=pt_br traduz a descrição do clima
    link_clima = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&units=metric&lang=pt_br"

    link_geo = f"https://api.openweathermap.org/geo/1.0/direct?q={cidade}&limit=1&appid={api_key}"

    res_geo = requests.get(link_geo)
    res_clima = requests.get(link_clima)
    if res_geo.status_code != 200 or not res_geo.json():
        print("Erro ao localizar cidade via Geocoding.")
        return

    dados_geo = res_geo.json()
    lat = dados_geo[0]["lat"]
    long = dados_geo[0]["lon"]
    pais = dados_geo[0]["country"]
    estado = dados_geo[0].get("state", "N/A")

    #verifica se a conexao foi bem sucedida
    if res_clima.status_code == 200 and res_geo.status_code == 200:
        dados_clima = res_clima.json()

        # Extraindo informações específicas do JSON
        descricao = dados_clima["weather"][0]["description"]
        temperatura = dados_clima["main"]["temp"]
        umidade = dados_clima["main"]["humidity"]
        cidade_nome = dados_clima["name"]
        #previsao de 5 dias pra frente
        #poluição do ar


        print(f"\n--- Clima em {cidade_nome} ---")
        print(f"Condição: {descricao.capitalize()}")
        print(f"Temperatura: {temperatura}°C")
        print(f"Umidade: {umidade}%")
        print(f"latitude {lat}")
        print(f"longitude {long}")
        print(f"País: {paises_siglas.get(pais,pais)}\nEstado: {estado}")

    else:
        print("Erro ao encontrar cidade. Verifique o nome ou sua chave de API.")


cidade_usuario = input("Digite o nome da cidade: ")
buscar_clima(cidade_usuario)

