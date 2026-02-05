#!/usr/bin/env python3
"""
Weather CLI - Простая утилита для проверки погоды.
Использование: python main.py Москва
"""
import argparse
import sys
from typing import Optional
from src.weather import WeatherAPI, HistoryManager
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Проверить погоду в городе")
    parser.add_argument("city", help="Название города (на русском или английском)")
    parser.add_argument("--history", action="store_true", help="Показать последние запросы")
    
    args = parser.parse_args()
    
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        print("❌ Ошибка: OPENWEATHER_API_KEY не найден в .env")
        sys.exit(1)
    
    weather_api = WeatherAPI(api_key)
    history = HistoryManager(os.getenv('HISTORY_FILE', 'weather_history.json'))
    
    if args.history:
        print("\n📋 Последние 5 запросов:")
        for entry in history.get_last_5():
            print(f"  {entry['city']}: {entry['temp']}°C")
        return
    
    # Получить погоду
    weather = weather_api.get_weather(args.city)
    if not weather:
        print(f"❌ Не удалось получить погоду для {args.city}")
        sys.exit(1)
    
    # Сохранить с timestamp
    weather['timestamp'] = datetime.now().isoformat()
    history.save(weather)
    
    # Красивый вывод
    print("\n🌤️" + "="*40)
    print(f"🏙️  Город: {weather['city']}")
    print(f"🌡️  Температура: {weather['temp']}°C")
    print(f"☁️   Описание: {weather['description'].title()}")
    print(f"💧 Влажность: {weather['humidity']}%")
    print(f"📊 Давление: {weather['pressure']} гПа")
    print("="*40)

if __name__ == "__main__":
    main()