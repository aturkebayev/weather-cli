import pytest
from unittest.mock import patch, MagicMock
from src.weather import WeatherAPI, HistoryManager
import os
from pathlib import Path

@pytest.fixture
def api_key():
    return "test_key"

@pytest.fixture
def history_file(tmp_path):
    file = tmp_path / "test_history.json"
    return str(file)

def test_weather_api_success(api_key, tmp_path):
    api = WeatherAPI(api_key)
    
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'name': 'Moscow',
            'main': {'temp': 15.0, 'humidity': 70, 'pressure': 1013},
            'weather': [{'description': 'ясно'}]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = api.get_weather('Moscow')
    
    assert result['city'] == 'Moscow'
    assert result['temp'] == 15.0

def test_history_manager(history_file):
    manager = HistoryManager(history_file)
    
    weather_data = {
        'city': 'TestCity',
        'temp': 20,
        'timestamp': '2023-01-01'
    }
    manager.save(weather_data)
    
    manager.load()
    assert len(manager.history) == 1
    assert manager.history[0]['city'] == 'TestCity'