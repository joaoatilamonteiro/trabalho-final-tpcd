from openweather import OpenWeatherApp
from streamlit_app import render_app
import os
from dotenv import load_dotenv


def main():
    load_dotenv()
    app = OpenWeatherApp(os.getenv("OPENWEATHER_API_KEY"))
    render_app(app)


if __name__ == "__main__":
    main()
