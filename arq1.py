import requests
import json
from datetime import datetime

class OpenWeatherApp:

    def __init__(self,api_key,arquivo_silgas_paises = "siglas_paises.json"):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org"
        self.paises_siglas = self._carregar_siglas(arquivo_silgas_paises)

    def _carregar_siglas(self,arquivo):
        try:
            with open("siglas_paises.json", "r", encoding="utf-8") as p:
                paises_siglas = json.load(p)
        except FileNotFoundError:
            print("Aviso: Arquivo de siglas não encontrado. Usando siglas padrão.")
            paises_siglas = {}

        except json.JSONDecodeError:
            print("Erro: Falha ao ler o arquivo de siglas (formato inválido).")
            paises_siglas = {}
        return paises_siglas

    def buscar_localizacao(self,cidade):
        api_key = "389d09e6c175d65ddd691535ab080dc1"

        # O parâmetro units=metric serve para vir em Celsius
        # O parâmetro lang=pt_br traduz a descrição do clima

        link_geo = f"{self.base_url}/geo/1.0/direct?q={cidade}&limit=1&appid={self.api_key}"

        res_geo = requests.get(link_geo)
        res_geo.raise_for_status()
        dados_geo = res_geo.json()

        if not dados_geo:
            print(f"ERRO: A cidade '{cidade}' não foi encontrada na busca")
            return None
        return dados_geo[0]


    def clima_atual(self,lat,lon):
            link_clima = f"{self.base_url}/data/2.5/weather?lat={lat}&lon={lon}&appid={self.api_key}&units=metric&lang=pt_br"
            return requests.get(link_clima).json()


    def poluicao(self,lat,lon):
            link_poluicao = f"{self.base_url}/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={self.api_key}"
            return requests.get(link_poluicao).json()


    def obt_previsao(self, lat, lon):
            link_previsao = f"{self.base_url}/data/2.5/forecast?lat={lat}&lon={lon}&appid={self.api_key}&units=metric&lang=pt_br"
            return requests.get(link_previsao).json()

    def formata_data(self,data_str):
        obj_data_form = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
        return obj_data_form.strftime("%d/%m/%Y %H:%M")


    def exec(self,cidade):
        trad_aqi = {
            1: "Boa",
            2: "Razoável",
            3: "Moderada",
            4: "Pobre",
            5: "Muito Pobre"
        }

        try:
            local = self.buscar_localizacao(cidade)

            if not local:
                print(f"Cidade não encontrada: {cidade}")
                return
            lat, long = local["lat"], local["lon"]

            clima = self.clima_atual(lat,long)
            poluicao = self.poluicao(lat,long)
            previsao = self.obt_previsao(lat,long)

            print(f"\n=== RELATÓRIO===\n{local['name']} ({local.get('state', 'N/A')})")
            print(f"País: {self.paises_siglas.get(local['country'], local['country'])}")
            print(f"Temperatual Atual: {clima['main']['temp']}°C | Umidade: {clima['main']['humidity']}%")

            aqi = poluicao['list'][0]['main']['aqi']


            aqi_texto_filt = trad_aqi.get(aqi,"Desconhecido")
            print(f"Qualidade do Ar (AQI): {aqi_texto_filt} ({aqi})")

            print("\n--- PRÓXIMAS PREVISÕES (Para Tabela) ---")
            for item in previsao['list'][:3]:
                data = self.formata_data(item['dt_txt'])
                print(f"{data} | {item['main']['temp']}°C | {item['weather'][0]['description']}")


        except requests.exceptions.ConnectionError:
            print("Erro de conexão: Verifique sua internet.")

        except Exception as e:
            # Tratamento genérico para qualquer outro erro inesperado
            print(f"Ocorreu um erro inesperado: {e}")


while True:
    if __name__ == "__main__":
        minha_chave = "389d09e6c175d65ddd691535ab080dc1"
        key = OpenWeatherApp(minha_chave)
        cidade_input = input("Digite o nome da cidade: ")
        key.exec(cidade_input)

