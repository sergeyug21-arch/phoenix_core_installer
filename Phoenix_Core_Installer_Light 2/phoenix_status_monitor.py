
import time
import os

while True:
    print("[Phoenix Monitor] Проверка статуса модулей...")
    modules = [
        "phoenix_api_bridge.py",
        "phoenix_ollama_connector.py"
    ]
    for m in modules:
        if os.path.exists(m):
            print(f"✅ Модуль {m} найден")
        else:
            print(f"⚠ Модуль {m} отсутствует")
    time.sleep(10)
