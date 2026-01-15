import requests
import json
from datetime import datetime



try:
    with open("siglas_paises.json","r",encoding="utf-8") as p:
        paises_siglas = json.load(p)
except FileNotFoundError:
    print("Aviso: Arquivo de siglas não encontrado. Usando siglas padrão.")
    paises_siglas = {}

except json.JSONDecodeError:
    print("Erro: Falha ao ler o arquivo de siglas (formato inválido).")
    paises_siglas = {}


def buscar_dados_completos(cidade):
    api_key = "389d09e6c175d65ddd691535ab080dc1"

    # O parâmetro units=metric serve para vir em Celsius
    # O parâmetro lang=pt_br traduz a descrição do clima

    try:
        link_geo = f"https://api.openweathermap.org/geo/1.0/direct?q={cidade}&limit=1&appid={api_key}"

        res_geo = requests.get(link_geo)
        res_geo.raise_for_status()

        dados_geo = res_geo.json()
        if not dados_geo:
            print(f"ERRO: A cidade '{cidade}' não foi encontrada na busca")
            return
        lat = dados_geo[0]["lat"]
        long = dados_geo[0]["lon"]
        pais = dados_geo[0]["country"]
        estado = dados_geo[0].get("state", "N/A")

        link_clima = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&units=metric&lang=pt_br"
        res_clima = requests.get(link_clima)

        if res_geo.status_code != 200 or not res_geo.json():
            print("Erro ao localizar cidade via Geocoding.")
            return


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


            print(f"\n\n--- Clima em {cidade_nome} ---")
            print(f"Condição: {descricao.capitalize()}")
            print(f"Temperatura: {temperatura}°C")
            print(f"Umidade: {umidade}%")
            print(f"latitude {lat}")
            print(f"longitude {long}")
            print(f"País: {paises_siglas.get(pais,pais)}\nEstado: {estado}")

        else:
            print("Erro ao encontrar cidade. Verifique o nome ou sua chave de API.")

        link_poluicao = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={long}&appid={api_key}"
        res_poluicao = requests.get(link_poluicao)

        if res_poluicao.status_code == 200:
            dados_pol = res_poluicao.json()

            tradutor_aqi = {
                1: "Boa",
                2: "Razoável",
                3: "Moderada",
                4: "Pobre",
                5: "Muito Pobre"
            }

            #aqi = indicie de qualidade do ar

            aqi = dados_pol["list"][0]["main"]["aqi"]
            componentes = dados_pol["list"][0]["components"]
            co = componentes["co"]
            no2 = componentes["no2"]
            o3 = componentes["o3"]

            print(f"qualidade do ar (AQI): {tradutor_aqi[aqi]}, {aqi}")
            print(f"\nconcentração de CO: {co} µg/m³")
            print(f"\nconcentração de No2: {no2} µg/m³")
            print(f"\nconcentração de O3: {o3} µg/m³")


        link_previsao = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={long}&appid={api_key}&units=metric&lang=pt_br"
        res_previsao = requests.get(link_previsao)

        if res_previsao.status_code == 200:
            dados_previsao = res_previsao.json()

            lista_previsoes = dados_previsao["list"]

            for prev in lista_previsoes[:3]:
                data_hora = prev['dt_txt']
                obj_data_form = datetime.strptime(data_hora, "%Y-%m-%d %H:%M:%S")
                data_hora_formatada = obj_data_form.strftime("%d/%m/%Y %H:%M")
                temp_prev = prev['main']['temp']
                ceu = prev['weather'][0]['description']
                print(f"\nData e hora prevista: {data_hora_formatada} | temperatura prevista: {temp_prev}°C | situação do céu prevista: {ceu}")
    except requests.exceptions.ConnectionError:
        print("Erro de conexão: Verifique sua internet.")
    except requests.exceptions.HTTPError as err:
        print(f"Erro na API (HTTP): {err}")
    except requests.exceptions.Timeout:
        print("Erro: O tempo de resposta da API esgotou.")
    except Exception as e:
        # Tratamento genérico para qualquer outro erro inesperado (exigido no PDF)
        print(f"Ocorreu um erro inesperado: {e}")

while True:
    cidade_usuario = input("Digite o nome da cidade: ")
    buscar_dados_completos(cidade_usuario)

