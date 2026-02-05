# src/weather.py
from typing import Dict, Any, Optional
import requests
import json
import logging
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WeatherAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    def get_weather(self, city: str) -> Optional[Dict[str, Any]]:
        """Получить погоду для города."""
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'ru'
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            weather = {
                'city': data['name'],
                'temp': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure']
            }
            
            logger.info(f"Погода для {city}: {weather['temp']}°C")
            return weather
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка API: {e}")
            return None
        except KeyError as e:
            logger.error(f"Неверный ответ API: {e}")
            return None

class HistoryManager:
    def __init__(self, history_file: str):
        self.history_file = Path(history_file)
        self.history: list[Dict[str, Any]] = []
        self.load()
    
    def load(self):
        """Загрузить историю."""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Не удалось загрузить историю: {e}")
                self.history = []
    
    def save(self, weather_data: Dict[str, Any]):
        """Сохранить запрос."""
        entry = {
            'timestamp': str(weather_data.get('timestamp', '')),
            'city': weather_data['city'],
            'temp': weather_data['temp']
        }
        self.history.append(entry)
        
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except IOError as e:
            logger.error(f"Не удалось сохранить историю: {e}")
    
    def get_last_5(self) -> list[Dict[str, Any]]:
        """Последние 5 запросов."""
        return self.history[-5:]