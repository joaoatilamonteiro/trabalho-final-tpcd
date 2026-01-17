1. Aplicação de Clima \- OpenWeather (AP3)

  Este projeto é a Avaliação Prática (AP3) da disciplina Técnicas de Programação para Ciência de Dados. A aplicação foi desenvolvida em Python utilizando a biblioteca Streamlit para interface gráfica e a API da OpenWeatherMap para exibir dados climáticos em tempo real.

2. Equipe:

João Átila de Oliveira Monteiro - 588072
Rômulo Emanuel Marinho Barbosa - 579586
Gabriel Garcia Colares - 581964
João Gabriel Aquino Ferreira - 582424


3. Funcionalidades

 A aplicação cumpre os requisitos de modularização e uso de API, oferecendo as seguintes funcionalidades:  
3.1.  Busca por Cidade: O usuário pode digitar o nome de qualquer cidade para buscar sua localização geográfica (GeoCoding API).  
3.2.  Clima Atual: Exibe temperatura, sensação térmica, umidade e cobertura de nuvens com indicadores visuais de calor/frio.  
3.3.  Previsão de 5 Dias (Tabela): Uma tabela detalhada com previsões a cada 3 horas, contendo data formatada, temperatura e descrição do tempo.  
3.4.  Variação de Temperatura (Gráfico): Um gráfico de linha interativo mostrando a evolução da temperatura ao longo dos próximos dias.  
3.5.  Qualidade do Ar: Exibe o índice AQI (Índice de Qualidade do Ar) e um gráfico de barras com a concentração de poluentes (CO, NO2, O3, etc.).

4. Tecnologias Utilizadas

4.1. Linguagem: Python 3  
4.2. Interface: Streamlit  
4.3. Manipulação de Dados: Pandas  
4.4. Requisições HTTP: Requests  
4.5. API: OpenWeatherMap (Endpoints: Weather, Forecast, Air Pollution, Geocoding)

5. Estrutura do Projeto

  O código foi organizado seguindo princípios de orientação a objetos e modularização:  
5.1. “main.py”: Arquivo principal que inicializa a aplicação e injeta as dependências.  
5.2. “streamlit\_app.py”: Módulo responsável por toda a interface visual (View) e exibição dos dados.  
5.3. “openweather.py”: Módulo contendo a classe \`OpenWeatherApp\`, responsável pela lógica de conexão com a API e tratamento de dados (Model/Controller).  
5.4. “siglas\_paises.json”: Arquivo auxiliar para tradução de siglas de países.

6. Como Executar o Projeto

 Certifique-se de ter o Python instalado e todos os arquivos em uma mesma pasta. Em seguida, instale as bibliotecas necessárias executando o seguinte comando no terminal:  
streamlit run main.py  
