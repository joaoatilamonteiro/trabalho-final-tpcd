from openweather import OpenWeatherApp
from streamlit_app import render_app


def main():
    API_KEY = "389d09e6c175d65ddd691535ab080dc1"
    app = OpenWeatherApp(API_KEY)
    render_app(app)


if __name__ == "__main__":
    main()
