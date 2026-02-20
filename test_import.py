try:
    from src.weather import WeatherAPI
    print("✅ src.weather импортируется!")
except ImportError as e:
    print(f"❌ Импорт сломан: {e}")
    print("sys.path:", [p[-20:] for p in sys.path])  # Последние 20 символов путей