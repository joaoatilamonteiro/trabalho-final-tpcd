import requests
import json
import streamlit as st
import pandas as pd
from datetime import datetime


class OpenWeatherApp:

    def __init__(self, api_key, arquivo_siglas_paises="siglas_paises.json"):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org"
        self.paises_siglas = self._carregar_siglas(arquivo_siglas_paises)

    def _carregar_siglas(self, arquivo):
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def buscar_localizacao(self, cidade):
        url = f"{self.base_url}/geo/1.0/direct"
        params = {
            "q": cidade,
            "limit": 1,
            "appid": self.api_key
        }

        res = requests.get(url, params=params)
        res.raise_for_status()
        dados = res.json()

        if not dados:
            return None
        return dados[0]

    def clima_atual(self, lat, lon):
        url = f"{self.base_url}/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric",
            "lang": "pt_br"
        }
        return requests.get(url, params=params).json()

    def poluicao(self, lat, lon):
        url = f"{self.base_url}/data/2.5/air_pollution"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key
        }
        return requests.get(url, params=params).json()

    def previsao(self, lat, lon):
        url = f"{self.base_url}/data/2.5/forecast"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric",
            "lang": "pt_br"
        }
        return requests.get(url, params=params).json()

    def formatar_data(self, data_str):
        return datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S").strftime("%d/%m %H:%M")

    def executar(self, cidade):
        local = self.buscar_localizacao(cidade)
        if not local:
            return None

        lat, lon = local["lat"], local["lon"]

        return {
            "local": local,
            "clima": self.clima_atual(lat, lon),
            "poluicao": self.poluicao(lat, lon),
            "previsao": self.previsao(lat, lon)
        }


# ===================== STREAMLIT APP =====================

st.set_page_config(page_title="Clima - OpenWeather", layout="centered")

st.title("🌤️ Aplicação de Clima - OpenWeather")

API_KEY = "389d09e6c175d65ddd691535ab080dc1"
app = OpenWeatherApp(API_KEY)

cidade = st.text_input("Digite o nome da cidade:")

if cidade:
    try:
        dados = app.executar(cidade)

        if not dados:
            st.error("Cidade não encontrada.")
        else:
            local = dados["local"]
            clima = dados["clima"]
            poluicao = dados["poluicao"]
            previsao = dados["previsao"]

            pais = app.paises_siglas.get(local["country"], local["country"])

            st.subheader(f"📍 {local['name']} - {pais}")

            st.metric("🌡️ Temperatura (°C)", clima["main"]["temp"])
            st.metric("💧 Umidade (%)", clima["main"]["humidity"])

            trad_aqi = {
                1: "Boa",
                2: "Razoável",
                3: "Moderada",
                4: "Ruim",
                5: "Muito Ruim"
            }

            aqi = poluicao["list"][0]["main"]["aqi"]
            st.write(f"🌫️ **Qualidade do Ar:** {trad_aqi.get(aqi)} ({aqi})")

            # ---------- TABELA ----------
            st.subheader("📊 Previsão do Tempo (próximas horas)")

            registros = []
            for item in previsao["list"][:8]:
                registros.append({
                    "Data": app.formatar_data(item["dt_txt"]),
                    "Temperatura (°C)": item["main"]["temp"],
                    "Descrição": item["weather"][0]["description"]
                })

            df = pd.DataFrame(registros)
            st.table(df)

            # ---------- GRÁFICO ----------
            st.subheader("📈 Gráfico de Temperatura")

            df["Data"] = pd.to_datetime(df["Data"], format="%d/%m %H:%M")
            st.line_chart(df.set_index("Data")["Temperatura (°C)"])

    except requests.exceptions.ConnectionError:
        st.error("Erro de conexão com a internet.")
    except Exception as e:
        st.error(f"Erro inesperado: {e}")
