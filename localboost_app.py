import streamlit as st
from PIL import Image
import piexif
import os

# Função para converter GPS
def convert_to_deg(value):
    deg = int(value)
    min_ = int((value - deg) * 60)
    sec = round(((value - deg) * 60 - min_) * 60, 6)
    return ((deg, 1), (min_, 1), (int(sec * 100), 100))

# Função para aplicar GPS na imagem
def set_gps_location(image, lat, lng):
    exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "Interop": {}, "1st": {}, "thumbnail": None}
    gps_ifd = {
        piexif.GPSIFD.GPSLatitudeRef: 'S' if lat < 0 else 'N',
        piexif.GPSIFD.GPSLatitude: convert_to_deg(abs(lat)),
        piexif.GPSIFD.GPSLongitudeRef: 'W' if lng < 0 else 'E',
        piexif.GPSIFD.GPSLongitude: convert_to_deg(abs(lng)),
    }
    exif_dict['GPS'] = gps_ifd
    exif_bytes = piexif.dump(exif_dict)

    output_path = "output.jpg"
    image.save(output_path, "jpeg", exif=exif_bytes)

    return output_path

# Interface Streamlit
st.set_page_config(page_title="LocalBoost - SEO Local", page_icon="📍")
st.title("📍 LocalBoost - Otimizador de Imagens para Google Meu Negócio")
st.write("🚀 Suba suas fotos com geolocalização e aumente sua visibilidade no Google!")

with st.form("form"):
    uploaded_file = st.file_uploader("📸 Faça upload da sua imagem", type=["jpg", "jpeg", "png"])
    empresa = st.text_input("🏢 Nome da empresa (use para nome do arquivo)")
    latitude = st.number_input("🌎 Latitude", value=-22.7338, format="%.6f")
    longitude = st.number_input("🌍 Longitude", value=-45.1241, format="%.6f")
    submitted = st.form_submit_button("🚀 Gerar imagem otimizada")

if submitted and uploaded_file:
    image = Image.open(uploaded_file)
    result_path = set_gps_location(image, latitude, longitude)

    novo_nome = f"{empresa.lower().replace(' ', '-')}.jpg"
    os.rename(result_path, novo_nome)

    st.success(f"Imagem otimizada salva como {novo_nome}")
    with open(novo_nome, "rb") as file:
        st.download_button(
            label="📥 Download da imagem otimizada",
            data=file,
            file_name=novo_nome,
            mime="image/jpeg"
        )
