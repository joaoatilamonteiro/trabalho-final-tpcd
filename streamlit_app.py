import streamlit as st
import pandas as pd
import requests
from datetime import datetime


def formatar_data(data_str):
    return datetime.strptime(
        data_str, "%Y-%m-%d %H:%M:%S"
    ).strftime("%d/%m %H:%M")


def render_app(openweather):
    st.set_page_config(page_title="Clima - OpenWeather", layout="centered")
    st.title("🌤️ Aplicação de Clima - OpenWeather")

    cidade = st.text_input("Digite o nome da cidade:")

    if not cidade:
        return

    try:
        dados = openweather.executar(cidade)

        if not dados:
            st.error("Cidade não encontrada.")
            return

        local = dados["local"]
        clima = dados["clima"]
        poluicao = dados["poluicao"]
        previsao = dados["previsao"]

        pais = openweather.paises_siglas.get(
            local["country"], local["country"]
        )

        st.subheader(f"📍 {local['name']} - {pais}")

        col1, col2 = st.columns(2)
        col1.metric("🌡️ Temperatura (°C)", clima["main"]["temp"])
        col2.metric("💧 Umidade (%)", clima["main"]["humidity"])

        trad_aqi = {
            1: "Boa",
            2: "Razoável",
            3: "Moderada",
            4: "Ruim",
            5: "Muito Ruim",
        }

        aqi = poluicao["list"][0]["main"]["aqi"]
        st.write(
            f"🌫️ **Qualidade do Ar:** {trad_aqi.get(aqi)} ({aqi})"
        )

        # ---------- TABELA ----------
        st.subheader("📊 Previsão do Tempo")

        registros = [
            {
                "Data": formatar_data(item["dt_txt"]),
                "Temperatura (°C)": item["main"]["temp"],
                "Descrição": item["weather"][0]["description"],
            }
            for item in previsao["list"][:8]
        ]

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
