import streamlit as st
import keras
import requests
import json
import numpy as np
from streamlit_chat import message
from dotenv import load_dotenv
import os
import time
from statistics import mean
import math
from streamlit_option_menu import option_menu

load_dotenv(verbose=True)


LOCALHOST = os.getenv("IP4_ADDRESS")
PORT = os.getenv("PORT")

url = "http://localhost:11434/api/chat"
headers = {"Content-Type": "application/json"}


st.set_page_config(page_title="SoulSense", page_icon=":heart:")

def create_prompt(emotion, heart_rate):
    prompt = f"""Buatkan langkah-langkah yang harus dilakukan untuk menjaga kesehatan mental berdasarkan kondisi berikut:
    
    Ekspresi wajah: {emotion}
    Detak jantung: {heart_rate}

    Jelaskan dalam bahasa Indonesia bentuk poin-poin agar mudah dipahami dan dengan panjang maksimum 300 karakter.
    """
    return prompt

def continous_prompt(message: str, **last_context):
    prompt = f"""Jawab dan jelaskan dalam bahasa Indonesia dengan panjang maksimum 300 karakter.
    
    pertanyaan: {message}

    """

    return prompt

def test_prompt():
    return "Test"

def stream_response(response):
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode("utf-8")
            try:
                json_response = json.loads(decoded_line)
                if "message" in json_response:
                    yield json_response["message"]["content"]
            except json.JSONDecodeError:
                pass

def get_response(content):
    response = requests.post(url, headers=headers, json=content)
    if response.status_code == 200:
        return json.loads(response.content)['message']['content']
    return None

@st.cache_data
def cache_emotion(emotion):
    return emotion

@st.cache_data
def cache_heart_rate(heart_rate):
    return heart_rate

@st.cache_data
def cache_name(name):
    return name

# Inisialisasi session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'image_uploaded' not in st.session_state:
    st.session_state.image_uploaded = False
if 'heart_rate_checked' not in st.session_state:
    st.session_state.heart_rate_checked = False
if 'next_clicked' not in st.session_state:
    st.session_state.next_clicked = False
if 'chatbot_container' not in st.session_state:
    st.session_state.chatbot_container = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'assistant_started ' not in st.session_state:
    st.session_state.assistant_started = False
if 'data_heart_rate' not in st.session_state:
    st.session_state.data_heart_rate = None


# Fungsi untuk handle setiap button diklik
def next_step():
    st.session_state.step += 1
    st.session_state.next_clicked = True

with st.sidebar:
    selected = option_menu(
        "Menu",
        ["Dashboard", "Our Team"],
        icons=["house", "person"]

    )
if selected == "Dashboard":
    # Judul utama aplikasi
    st.title("SoulSense")
    st.markdown("""<hr style="height:3px;border:none;color:#fec76f;background-color:#fec76f;" /> """, unsafe_allow_html=True)

    # Step 1 - Personal Info
    if st.session_state.step >= 1:
        st.write("""
        Selamat datang di SoulSense! Yuk lengkapi data diri kamu terlebih dahulu.
        """)
        user_name = st.text_input("Masukkan nama kamu")
        cache_name(user_name)

        if user_name:
            st.write(f'### Halo, :orange[{user_name}] :wave:')
            if st.session_state.step == 1 and not st.session_state.next_clicked:
                if st.button("lanjut"):
                    next_step()

    # Step 2 - Expression Checker
    if st.session_state.step >= 2:
        st.session_state.next_clicked = False
        st.header("Emotion Checker")
        st.write(""":orange-background[Tahap ini akan membantu anda mengetahui ekspresi wajah anda. Silahkan pilih opsi di bawah ini untuk melanjutkan.]""")
        # Pilihan mengambil gambar atau upload gambar
        upload_option = st.radio("Pilih opsi berikut:", ("Buka kamera", "Unggah dari perangkat"))

        if upload_option == "Buka kamera":
            image = st.camera_input("Ambil foto dengan kamera")
        else:
            image = st.file_uploader("Pilih dan unggah gambar anda", type=["jpg", "jpeg", "png"])

        if image:
            st.session_state.image_uploaded = True
            st.image(image, caption="Uploaded Image", use_column_width=True)
            model = keras.models.load_model("./model/model_adam_leaky_relu_1.h5")

            img = keras.preprocessing.image.load_img(image, target_size=(48, 48))
            img_array = keras.preprocessing.image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)

            prediction = model.predict(img_array)

            class_name = ['marah', 'takut', 'bahagia', 'netral', 'sedih', 'terkejut']
            index_class = np.argmax(prediction)

            cache_emotion(class_name[index_class])

            st.write(f'#### Ekspresi anda: :orange-background[{class_name[index_class]}]')
            if st.session_state.step == 2 and not st.session_state.next_clicked:
                if st.button("lanjut"):
                    next_step()

        else:
            st.session_state.image_uploaded = False

    # Step 3 - Pulse Monitor
    if st.session_state.step >= 3:
        st.session_state.next_clicked = False
        st.header("Pulse Monitor")
        st.write(
            """:orange-background[Pada tahap ini, aplikasi akan mengambil data detak jantung anda dari sensor. Silakan klik tombol di bawah ini dan letakkan jari anda pada sensor.]"""
        )
        # Note
        st.write(
            """Note: Kami mengukur rata-rata detak jantung anda dalam 1 menit."""
        )

        check_heart_rate = st.button("Cek detak jantung")

        if check_heart_rate:
            if not st.session_state.data_heart_rate:
                with st.status("Mengambil data detak jantung..."):
                    while True:
                        response = requests.get(
                            f"http://{LOCALHOST}:{PORT}/api/sensor/get_data"
                        ).json()
                        if response["status"] and len(response["data"]) > 0:
                            st.session_state.data_heart_rate = response["data"]
                            break
                        time.sleep(10)

        if st.session_state.data_heart_rate:
            heart_rate_list = [data["value"] for data in st.session_state.data_heart_rate]
            heart_rate = math.ceil(mean(heart_rate_list))
        

            dict_stress_level = {
                "Rendah" : ":blue[Rendah]",
                "Normal" : ":green[Normal]",
                "Tinggi" : ":red[Tinggi]"
            }

            if heart_rate > 0:
                # Contoh perhitungan sementara stress level
                if heart_rate < 60:
                    stress_level = "Rendah"
                elif 60 <= heart_rate <= 100:
                    stress_level = "Normal"
                else:
                    stress_level = "Tinggi"

                st.write(f'#### Denyut nadi anda :orange-background[{heart_rate}] bpm')
                st.write(f'#### Tingkat stress anda {dict_stress_level[stress_level]}')
                st.session_state.heart_rate_checked = True
                if st.session_state.step == 3 and not st.session_state.next_clicked:
                    if st.button("lanjut"):
                        requests.delete(f"http://{LOCALHOST}:{PORT}/api/sensor/delete_all_data")
                        st.session_state.data_heart_rate = None
                        next_step()
            else:
                st.session_state.heart_rate_checked = False

    def create_chatbot_container():
        return st.container()

    # Step 4 - Result
    if st.session_state.step >= 4:
        if not st.session_state.image_uploaded:
            st.write('#### :red[Lengkapi data anda dahulu pada] :orange[Emotion Checker").]')
        elif st.session_state.heart_rate_checked:
            if len(st.session_state.chat_history) == 0:
                conclusion_json = {
                    "model": "llama3",
                    "messages": [
                        {
                            "role": "user",
                            "content": create_prompt(class_name[index_class], heart_rate)
                        }
                    ],
                    "stream": False
                }
                response = get_response(conclusion_json)
                st.session_state.chat_history.append(
                    {
                        "user": None,
                        "bot": response
                    }
                )

            if True:
                st.write(f'##### Hi, :orange[{user_name}]. Berikut adalah hasil dari data yang telah anda inputkan.')
                with st.container():
                    for chat in st.session_state.chat_history:
                        if chat["user"]:
                            message(chat["user"], is_user=True)
                        if chat["bot"]:
                            message(chat["bot"])

                    # assistant_response = ""
                    user_input = st.chat_input("Type your response here")

                    if user_input:
                        user_input_json = {
                            "model": "llama3",
                            "messages": [
                                {
                                    "role": "user",
                                    "content": continous_prompt(user_input)
                                }
                            ],
                            "stream": False
                        }
                        bot_response = get_response(user_input_json)
                        st.session_state.chat_history.append({"user": user_input, "bot": bot_response})

                        st.rerun()
                
                st.write('#### Thank you, for stepping by. Hope you a better soul :relieved:')
                next_step()
        else: 
            st.write('#### :red[Complete your data on] :orange[Pulse Monitor.]')

elif selected == "Our Team":
    def display_member(image_path, name, major, link):
        # Membaca gambar dari path
        with open(image_path, "rb") as img_file:
            img_bytes = img_file.read()
        # Menggunakan base64 encoding untuk gambar
        import base64
        img_base64 = base64.b64encode(img_bytes).decode()

        st.markdown(
            f"""
            <div style='border: 2px solid #ccc; border-radius: 10px; padding: 10px; text-align: center;'>
                <img src="data:image/jpeg;base64,{img_base64}" style='border-radius: 50%; width: 150px; height: 150px;' />
                <p style='font-weight: bold; margin: 10px 0;'>{name}</p>
                <p>{major}</p>
                <p><a href="https://{link}" target="_blank">LinkedIn Profile</a></p>
            </div>
            """,
            unsafe_allow_html=True
        )

    members = [
        {"image": "./dashboard/1.jpg", "name": "Salma Nabila Lovyanti", "major": "Informatics", "link": "www.linkedin.com/in/salma-nabila-lovyanti"},
        {"image": "./dashboard/2.jpg", "name": "Dzulfikri Adjmal", "major": "Informatics", "link": "www.linkedin.com/in/dzulfikri-adjmal"},
        {"image": "./dashboard/3.png", "name": "Defita Rahmawati", "major": "Information System", "link": "www.linkedin.com/in/defitarahmawati"},
    ]

    st.title("Team Members")
    st.markdown("""<hr style="height:3px;border:none;color:#fec76f;background-color:#fec76f;" /> """, unsafe_allow_html=True)
    st.write(f'## Group 20')

    cols = st.columns(3)

    for idx, member in enumerate(members):
        with cols[idx % 3]:
            display_member(member["image"], member["name"], member["major"], member["link"])

