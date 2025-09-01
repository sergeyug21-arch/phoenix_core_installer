from flask import Flask, request, jsonify
import requests
import socket
import os
import openai

app = Flask(__name__)

# Конфигурация
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
current_model = "qwen3:8b"
openai.api_key = "sk-test_fakekey_1234567890abcdef"

# 🔍 Поиск свободного порта
def find_free_port(start_port=8085, max_tries=20):
    port = start_port
    for _ in range(max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                port += 1
    raise RuntimeError("Нет свободных портов!")

# 📡 Запрос в ChatGPT, если Ollama не отвечает
def fallback_to_chatgpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты — разум Феникса. Отвечай глубоко, ясно и по делу."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"[Ошибка ChatGPT]: {str(e)}"

# 🚀 Основной маршрут для Streamlit
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        user_input = data.get("user_input", "")

        if not user_input:
            return jsonify({"error": "Пустой запрос"}), 400

        answer = ""
        try:
            response = requests.post(OLLAMA_URL, json={
                "model": current_model,
                "prompt": user_input
            }, stream=True, timeout=60)

            for line in response.iter_lines():
                if line:
                    try:
                        chunk = line.decode("utf-8")
                        if '"response":"' in chunk:
                            part = chunk.split('"response":"')[1].split('"')[0]
                            answer += part
                    except:
                        continue
        except Exception as e:
            answer = f"[Ошибка Ollama]: {str(e)}"

        # ⛑ Если Ollama промолчал — подключаем ChatGPT
        if not answer.strip() or answer.startswith("[Ошибка"):
            answer = fallback_to_chatgpt(user_input)

        return jsonify({"response": answer})

    except Exception as e:
        return jsonify({"error": f"Ошибка: {str(e)}"}), 500

# 🛠 Ручной маршрут
@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json(force=True)
        prompt = data.get("prompt", "")

        if not prompt:
            return jsonify({"error": "Пустой запрос"}), 400

        answer = ""
        try:
            response = requests.post(OLLAMA_URL, json={
                "model": current_model,
                "prompt": prompt
            }, stream=True, timeout=60)

            for line in response.iter_lines():
                if line:
                    try:
                        chunk = line.decode("utf-8")
                        if '"response":"' in chunk:
                            part = chunk.split('"response":"')[1].split('"')[0]
                            answer += part
                    except:
                        continue
        except Exception as e:
            answer = f"[Ошибка Ollama]: {str(e)}"

        if not answer.strip() or answer.startswith("[Ошибка"):
            answer = fallback_to_chatgpt(prompt)

        return jsonify({"response": answer})

    except Exception as e:
        return jsonify({"error": f"Ошибка: {str(e)}"}), 500

# 🔄 Смена модели
@app.route("/set_model", methods=["POST"])
def set_model():
    global current_model
    data = request.json
    model = data.get("model")
    if not model:
        return jsonify({"error": "Модель не указана"}), 400

    current_model = model
    return jsonify({"status": "OK", "model": current_model})

# 🌐 Корневой маршрут
@app.route("/")
def root():
    return jsonify({"status": "Phoenix API Bridge работает", "model": current_model})

# 🧠 Запуск
if __name__ == "__main__":
    free_port = find_free_port(8085)
    print(f"[API Bridge] Запуск локального моста Феникса на порту {free_port}")
    print(f"Феникс готов принимать запросы на http://127.0.0.1:{free_port}")
    app.run(host="127.0.0.1", port=free_port)
