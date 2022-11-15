import streamlit as st  #Web Uygulaması
from PIL import Image #Resim dosyalarını işlemek için kullanıyoruz
import pytesseract #package.txt dosyasındaki tesseract modüllerinin pythonda çalışabilmesi için gerekiyor
import base64 #ocr ile oluşturulmuş metinleri dosya haline getirmek için kullandığımız kütüphane
import os
import fitz #pymupdf modülünü çağırmak için kullanıyoruz


#title
st.title("Optik Karakter Okuyucu - Resim ve PDF dosyalarından metin çıkarımı")

#subtitle
st.markdown("## `streamlit` ve `tesseract` kullanarak geliştirilmiş bir OCR Web uygulaması")

st.markdown("...")
