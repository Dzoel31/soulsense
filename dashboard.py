import streamlit as st

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
    st.header("Get To Know")
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

# Step 2 - Expression Checker
if st.session_state.step >= 2:
    st.session_state.next_clicked = False
    st.header("Expression Checker")
    st.write("""(deskripsi)""")
    # Pilihan mengambil gambar atau upload gambar
    upload_option = st.radio("Choose an option:", ("Open Camera", "Upload From a File"))

    if upload_option == "Open Camera":
        image = st.camera_input("Position your face at the camera and take a picture.")
    else:
        image = st.file_uploader("Select and upload a photo from file explorer.", type=["jpg", "jpeg", "png"])

    if image:
        st.session_state.image_uploaded = True
        st.write('#### Your Expression Is: :orange-background[(hasil)]')
        if st.session_state.step == 2 and not st.session_state.next_clicked:
            if st.button("Next"):
                next_step()
    else:
        st.session_state.image_uploaded = False

# Step 3 - Pulse Monitor
if st.session_state.step >= 3:
    st.session_state.next_clicked = False
    st.header("Pulse Monitor")
    st.write("""(deskripsi)""")
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

        st.write(f'#### Your pulse rate is :orange-background[{heart_rate}] bpm')
        st.write(f'#### Your stress level is {stress_level}')
        st.session_state.heart_rate_checked = True
        if st.session_state.step == 3 and not st.session_state.next_clicked:
            if st.button("Next"):
                next_step()
    else:
        st.session_state.heart_rate_checked = False

# Step 4 - Result
if st.session_state.step >= 4:
    if not st.session_state.image_uploaded:
        st.write('#### :red[Complete your data on] :orange[Expression Checker.]')
    elif st.session_state.heart_rate_checked: 
        st.header("Result")
        st.write(f'##### Hi, :orange[{user_name}]. This is your souls\'s examination result based on your data collect.')
        # Placeholder untuk chatgpt
        message = st.text_area("")
        st.write('#### Thank you, for stepping by. Hope you a better soul :relieved:')
        next_step()
    else: 
        st.write('#### :red[Complete your data on] :orange[Pulse Monitor.]')
