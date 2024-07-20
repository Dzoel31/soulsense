import streamlit as st
from deepface import DeepFace
import cv2 as cv
import os
import numpy as np

# Inisialisasi session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'image_uploaded' not in st.session_state:
    st.session_state.image_uploaded = False
if 'heart_rate_checked' not in st.session_state:
    st.session_state.heart_rate_checked = False
if 'next_clicked' not in st.session_state:
    st.session_state.next_clicked = False

# Fungsi untuk handle setiap button diklik
def next_step():
    st.session_state.step += 1
    st.session_state.next_clicked = True

# Judul utama aplikasi
st.title("SoulSense")
st.markdown("""<hr style="height:3px;border:none;color:#fec76f;background-color:#fec76f;" /> """, unsafe_allow_html=True)

# Step 1 - Personal Info
if st.session_state.step >= 1:
    #st.header("Get To Know")
    st.write("""
    Hi, welcome to SoulSense! We\'d love to know your name.
    """)
    user_name = st.text_input("What should we call you? ")

    if user_name:
        st.write(f'### Hi, :orange[{user_name}] :wave:')
        st.write('#### Welcome to SoulSense :innocent:')
        if st.session_state.step == 1 and not st.session_state.next_clicked:
            if st.button("Next"):
                next_step()

# Step 2 - Emotion Checker
if st.session_state.step >= 2:
    st.session_state.next_clicked = False
    st.markdown("""<hr style="height:1px;border:none;color:#fec76f;background-color:#fec76f;" /> """, unsafe_allow_html=True)
    st.header("Emotion Checker")
    st.write(""":orange-background[In this part, you can take a picture of your face using the camera or upload an image from your device. 
    The uploaded image will be analyzed to detect your facial expression.]""")
    # Pilihan mengambil gambar atau upload gambar
    upload_option = st.radio("Choose an option:", ("Open Camera", "Upload From a File"))

    if upload_option == "Open Camera":
        image_file = st.camera_input("Position your face at the camera and take a picture.")
        if image_file is not None:
            # Membaca gambar dari camera input
            image = cv.imdecode(np.frombuffer(image_file.read(), np.uint8), cv.IMREAD_COLOR)
    else:
        image_file = st.file_uploader("Choose a file.")  #, type=["jpg", "jpeg", "png"])
        if image_file is not None:
            input_path = f"temp_{image_file.name}"
            with open(input_path, "wb") as temp_file:
                temp_file.write(image_file.read())
            image = cv.imread(input_path)
            if os.path.exists(input_path):
                os.remove(input_path)

    if image_file is not None:
        st.session_state.image_uploaded = True
        # Analisis gambar menggunakan DeepFace
        prediction = DeepFace.analyze(image, actions=["emotion"], enforce_detection=False)
        st.write(f'#### You are feeling: :red-background[{prediction[0]["dominant_emotion"]}]')
        if st.session_state.step == 2 and not st.session_state.next_clicked:
            if st.button("Next"):
                next_step()
    else:
        st.session_state.image_uploaded = False

# Step 3 - Pulse Monitor
if st.session_state.step >= 3:
    st.session_state.next_clicked = False
    st.markdown("""<hr style="height:1px;border:none;color:#fec76f;background-color:#fec76f;" /> """, unsafe_allow_html=True)
    st.header("Pulse Monitor")
    st.write(""":orange-background[In this part, you will use a device to check your pulse rate. Based on the entered pulse rate, 
    your stress level will be calculated and displayed.]""")
    # Sebagai contoh pake inputan manual, nanti ini diubah
    heart_rate = st.number_input("Enter your pulse rate ", min_value=0) #

    if heart_rate > 0:
        # Contoh perhitungan sementara stress level
        if heart_rate < 60:
            stress_level = ":blue[Low]"
        elif 60 <= heart_rate <= 100:
            stress_level = ":green[Normal]"
        else:
            stress_level = ":red[High]"

        st.write(f'#### Your pulse rate is :red-background[{heart_rate}] bpm; resulting {stress_level} stress level')
        st.session_state.heart_rate_checked = True
        if st.session_state.step == 3 and not st.session_state.next_clicked:
            if st.button("Next"):
                next_step()
    else:
        st.session_state.heart_rate_checked = False

# Step 4 - Result
if st.session_state.step >= 4:
    st.markdown("""<hr style="height:1px;border:none;color:#fec76f;background-color:#fec76f;" /> """, unsafe_allow_html=True)
    if not st.session_state.image_uploaded:
        st.write('#### :red[Complete your data on] :orange[Emotion Checker.]')
    elif st.session_state.heart_rate_checked: 
        st.header("Result")
        st.write(f'##### Hi, :orange[{user_name}]. This is your souls\'s examination result based on your data collect.')
        # Placeholder untuk hasil simpulan
        message = st.text_area("")
        st.write('#### Thank you for using SoulSense!. Hope you a better soul :relieved:')
        next_step()
    else: 
        st.write('#### :red[Complete your data on] :orange[Pulse Monitor.]')
