
import requests

def test_ollama():
    try:
        resp = requests.get("http://localhost:11434/api/tags")
        if resp.status_code == 200:
            print("Ollama подключен!")
        else:
            print("Ollama отвечает, но неактивен.")
    except Exception:
        print("Ошибка подключения к Ollama.")

if __name__ == "__main__":
    test_ollama()
