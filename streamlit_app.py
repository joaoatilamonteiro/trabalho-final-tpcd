import streamlit as st
import pandas as pd
import requests
from datetime import datetime

def formatar_data(data_str):
    # Formata para Dia/Mês Hora:Minuto
    return datetime.strptime(
        data_str, "%Y-%m-%d %H:%M:%S"
    ).strftime("%d/%m %H:%M")

def render_app(openweather):
    st.set_page_config(page_title="Clima - OpenWeather", layout="centered")
    st.title("🌤️ Aplicação de Clima - OpenWeather - AP3 TPCD")

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

        #---------- SEÇÃO CLIMA ATUAL (SIMPLIFICADA) ----------
        #Recuperando dados
        temp_atual = clima["main"]["temp"]
        sensacao = clima["main"]["feels_like"]
        umidade = clima["main"]["humidity"]

        #Colunas para organizar as métricas
        col1, col2, col3 = st.columns(3)

        # Usamos 'delta' para mostrar a diferença entre a real e a sensação
        dif_sensacao = sensacao - temp_atual

        col1.metric(
            label="🌡️ Temperatura", 
            value=f"{temp_atual:.1f} °C", 
            delta=f"{dif_sensacao:.1f} °C (Sensação)"
        )

        col2.metric("💧 Umidade", f"{umidade}%")
        col3.metric("☁️ Nuvens", f"{clima['clouds']['all']}%")

        # BARRA DE TEMPERATURA (Termômetro Linear)
        # Normalizamos a temperatura assumindo que 0°C é vazio e 50°C é cheio
        # Se for menor que 0, fica 0. Se for maior que 50, fica 100%
        progresso_temp = min(max(temp_atual / 50, 0.0), 1.0)

        st.write("Nível de Calor (Escala 0°C a 50°C):")

        # Mudando a cor da barra dependendo da temperatura
        cor_barra = "blue"
        if temp_atual > 20: cor_barra = "green" 
        if temp_atual > 30: cor_barra = "orange"
        if temp_atual > 35: cor_barra = "red"

        # O st.progress nativo usa a cor do tema, mas podemos usar Markdown para colorir
        # Mas para manter simples e nativo, vamos usar o padrão:
        st.progress(progresso_temp)

        if temp_atual > 35:
            st.caption("⚠️ Cuidado: Calor excessivo!")
        elif temp_atual < 15:
            st.caption("❄️ Clima frio.")
        else:
            st.caption("✅ Clima agradável.")
        # ---------- TABELA (MODIFICADO) ----------
        st.subheader("📊  Previsão para 5 Dias (intervalos de 3h)")

        # AQUI FOI FEITA A ALTERAÇÃO PRINCIPAL:
        # Removemos o [:8] para iterar sobre toda a lista (40 itens)
        registros = [
            {
                "Data": formatar_data(item["dt_txt"]),
                "Temperatura (°C)": item["main"]["temp"],
                "Umidade (%)": item["main"]["humidity"], # Adicionei umidade para ficar mais completo
                "Descrição": item["weather"][0]["description"],
            }
            for item in previsao["list"] 
        ]

        df = pd.DataFrame(registros)
        
        # Uso st.dataframe com altura fixa para criar barra de rolagem
        st.dataframe(df, use_container_width=True, hide_index=True, height=300)

        # ---------- GRÁFICO (MODIFICADO) ----------
        st.subheader("📊  Variação de Temperatura (5 Dias)")

        # Converter para datetime para o gráfico ordenar corretamente
        df["Data_Plot"] = pd.to_datetime(df["Data"], format="%d/%m %H:%M")
        
        # O gráfico de linha lida bem com 40 pontos
        st.line_chart(df.set_index("Data_Plot")["Temperatura (°C)"])

        # ---------- SEÇÃO DE POLUIÇÃO ----------
        st.divider()
        st.subheader("🌫️ Qualidade do Ar e Poluição")

        trad_aqi = {
            1: "Boa",
            2: "Razoável",
            3: "Moderada",
            4: "Ruim",
            5: "Muito Ruim",
        }

        # Extraindo dados da poluição
        aqi = poluicao["list"][0]["main"]["aqi"]
        componentes = poluicao["list"][0]["components"]

        st.info(f"Índice de Qualidade do Ar (AQI): **{trad_aqi.get(aqi, 'Desconhecida')} ({aqi})**")
        
        # Dicionário para renomear as siglas para nomes mais legíveis no gráfico
        nomes_poluentes = {
            "co": "CO (Monóxido de Carbono)",
            "no": "NO (Monóxido de Nitrogênio)",
            "no2": "NO2 (Dióxido de Nitrogênio)",
            "o3": "O3 (Ozônio)",
            "so2": "SO2 (Dióxido de Enxofre)",
            "pm2_5": "PM2.5 (Partículas Finas)",
            "pm10": "PM10 (Partículas Inaláveis)",
            "nh3": "NH3 (Amônia)"
        }

        # Criando DataFrame para o gráfico de barras
        # Mapeamos as chaves (ex: 'co') para os nomes legíveis
        dados_poluentes = {
            nomes_poluentes.get(k, k): v 
            for k, v in componentes.items()
        }
        
        df_poluicao = pd.DataFrame.from_dict(
            dados_poluentes, orient='index', columns=['Concentração (μg/m³)']
        )

        st.write("Concentração de poluentes (μg/m³):")
        st.bar_chart(df_poluicao)
    

    except requests.exceptions.ConnectionError:
        st.error("Erro de conexão com a internet.")
    except Exception as e:
        st.error(f"Erro inesperado: {e}")

        