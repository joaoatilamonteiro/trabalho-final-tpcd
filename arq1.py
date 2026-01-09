import requests


def buscar_clima(cidade):
    api_key = "389d09e6c175d65ddd691535ab080dc1"

    # O parâmetro units=metric serve para vir em Celsius
    # O parâmetro lang=pt_br traduz a descrição do clima
    link_xyz = (f"https://api.openweathermap.org/data/2.5/weather?q="
            f"{cidade}&appid={api_key}&units=metric&lang=pt_br")

    requisicao = requests.get(link_xyz)

#verifica se a conexao foi bem sucedida
    if requisicao.status_code == 200:
        dados = requisicao.json()

        # Extraindo informações específicas do JSON
        descricao = dados['weather'][0]['description']
        temperatura = dados['main']['temp']
        humidade = dados['main']['humidity']
        cidade_nome = dados[2]['name']
        #previsao de 5 dias pra frente
        #poluição do ar
        lat = dados['coord']['lat']
        long = dados['coord']['lon']
        pais = dados[0]['country']


        print(f"\n--- Clima em {cidade_nome} ---")

        print(f"Condição: {descricao.capitalize()}")
        print(f"Temperatura: {temperatura}°C")
        print(f"Umidade: {humidade}%")
        print(f"latitude {lat}")
        print(f"latitude {long}")
        print(f"País {pais}")
    else:
        print("Erro ao encontrar cidade. Verifique o nome ou sua chave de API.")


# Testando o código
cidade_usuario = input("Digite o nome da cidade: ")
buscar_clima(cidade_usuario)

