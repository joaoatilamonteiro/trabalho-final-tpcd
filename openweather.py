import requests
import json
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
        params = {"q": cidade, "limit": 1, "appid": self.api_key}

        res = requests.get(url, params=params)
        res.raise_for_status()

        dados = res.json()
        return dados[0] if dados else None

    def clima_atual(self, lat, lon):
        return self._get(
            "/data/2.5/weather",
            lat=lat,
            lon=lon,
            units="metric",
            lang="pt_br",
        )

    def poluicao(self, lat, lon):
        return self._get("/data/2.5/air_pollution", lat=lat, lon=lon)

    def previsao(self, lat, lon):
        return self._get(
            "/data/2.5/forecast",
            lat=lat,
            lon=lon,
            units="metric",
            lang="pt_br",
        )

    def _get(self, endpoint, **params):
        params["appid"] = self.api_key
        url = f"{self.base_url}{endpoint}"
        return requests.get(url, params=params).json()

    def executar(self, cidade):
        local = self.buscar_localizacao(cidade)
        if not local:
         return None

        lat, lon = local["lat"], local["lon"]

        keys = ["clima", "poluicao", "previsao"]
        funcs = [self.clima_atual, self.poluicao, self.previsao]

        dados = dict(
            zip(
                keys,
                map(lambda fn: fn(lat, lon), funcs),
            )
        )

        return {"local": local, **dados}

    def formata_data(self,data_str):
        obj_data_form = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
        return obj_data_form.strftime("%d/%m/%Y %H:%M")




