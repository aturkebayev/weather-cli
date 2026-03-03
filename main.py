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
    print("Выберите действие")
    ##parser = argparse.ArgumentParser(description="Выберите действие")
    ##parser.add_argument("getaction", help = "weather для погоды и history для просмотра истории запросов")
        
    args = input("weather для погоды и history для просмотра истории запросов: ")

    getHistory = 0

    if args == "weather":
        city = input("Введите название города: ")
    elif args == "history":
        getHistory = 1
    else:
        exit

    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        print("❌ Ошибка: OPENWEATHER_API_KEY не найден в .env")
        sys.exit(1)
    
    weather_api = WeatherAPI(api_key)
    history = HistoryManager(os.getenv('HISTORY_FILE', 'weather_history.json'))
    
    if getHistory==1:
        print("\n📋 Последние 5 запросов:")
        for entry in history.get_last_5(): 
            timestamp = datetime.fromisoformat(entry['timestamp'])
            print(f"  ", timestamp.strftime("%Y-%m-%d"), entry['city'],":", entry['temp'],"°C")
        return
    
    # Получить погоду
    weather = weather_api.get_weather(city)
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