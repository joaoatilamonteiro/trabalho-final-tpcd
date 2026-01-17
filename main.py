from openweather import OpenWeatherApp
from streamlit_app import render_app


def main():
    API_KEY = "5d795a0ef3a5d54327f99ce04dec18bd"
    app = OpenWeatherApp(API_KEY)
    render_app(app)


if __name__ == "__main__":
    main()
