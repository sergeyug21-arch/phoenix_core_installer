import streamlit as st
import requests

# Настройки интерфейса
st.set_page_config(page_title="Феникс Веб-Чат", page_icon="🕊️")

st.title("🕊️ Phoenix Web Chat")
st.markdown("Добро пожаловать! Задайте вопрос, и Феникс ответит.")

# Инициализация истории
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Отображение истории
for role, msg in st.session_state.chat_history:
    if role == "user":
        st.chat_message("Вы", avatar="🧑").markdown(msg)
    else:
        st.chat_message("Феникс", avatar="🕊️").markdown(msg)

# Ввод пользователя
if prompt := st.chat_input("Введите ваш вопрос..."):
    st.session_state.chat_history.append(("user", prompt))
    st.chat_message("Вы", avatar="🧑").markdown(prompt)

    try:
        response = requests.post(
        "http://localhost:8085/ask",
            json={"prompt": prompt},
            timeout=60
        )
        if response.ok:
            answer = response.json().get("response", "⚠️ Ответ не получен от сервера.")
        else:
            answer = f"⚠️ Ошибка от сервера Феникса: {response.status_code}"
    except Exception as e:
        answer = f"❌ Ошибка соединения с API Феникса:\n```\n{e}\n```"

    st.session_state.chat_history.append(("fenix", answer))
    st.chat_message("Феникс", avatar="🕊️").markdown(answer)
