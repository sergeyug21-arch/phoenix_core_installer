
import os
import subprocess

def install_phoenix():
    print("=== Установка Феникса начата ===")
    try:
        os.makedirs("Phoenix_Core", exist_ok=True)
        subprocess.run(["python3", "phoenix_api_bridge.py"], check=True)
        subprocess.run(["python3", "phoenix_ollama_connector.py"], check=True)
        subprocess.run(["python3", "phoenix_status_monitor.py"], check=True)
        print("=== Установка завершена успешно! ===")
    except Exception as e:
        print(f"Ошибка установки: {e}")

if __name__ == "__main__":
    install_phoenix()
