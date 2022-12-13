import streamlit as st  #Web Uygulaması
from PIL import Image #Resim dosyalarını işlemek için kullanıyoruz
import pytesseract #package.txt dosyasındaki tesseract modüllerinin pythonda çalışabilmesi için gerekiyor
import base64 #ocr ile oluşturulmuş metinleri dosya haline getirmek için kullandığımız kütüphane
import os
import fitz #pymupdf modülünü çağırmak için kullanıyoruz

#=================================================
#######GEREKLI FONKSIYONLAR TANIMLANIYOR##########
#=================================================
#PDF dosyasından metin çıkarımı fonksiyonu
def extract_text_from_pdf(file, language):
    st.write("PDF dosyasından metin çıkarımı")

    PDF_file = file
    
    
    #işlem devam ederken spinner/dönen yuvarlak gösteriyoruz.
    with st.spinner("PDF'den OCR işlemi çalışıyor!"):
        doc = fitz.open(stream=PDF_file.read(), filetype="pdf") #dosya yükleyiciden gelen pdf dosyasını açıp doc değişkenine kaydediyoruz
        images = [] #tesseracta göndermek için boş bir resim dizisi oluşturuyoruz.
        image_counter = 1 #sayaç
        all_t = "" #bulunan tüm metinler için kullandığımız değişken
        for page in doc: #doc değişkenindeki her bir sayfa için teker teker işlem yapıyoruz.
            pix = page.get_pixmap() #sayfanın görüntüsünü alıyor ve pix değişkenine aktarıyoruz
            filename = "page_" + str(image_counter) + ".JPEG" #dosya adını sayaç ile birlikte değişken isimde oluşturuyoruz
            pix.save(filename) #pix değişkenindeki resim dosyasını kaydediyoruz.
            images.append(filename) #resim dizisine bu dosya adını ekliyoruz
            st.spinner(text='PDF OCR işlemi devam ediyor...')
            text = pytesseract.image_to_string(filename, lang=language) #tesseract'ın resimden metin çıkarımı fonksiyonuna kaydettiğimiz dosya adı ve dil parametresini veriyoruz
            all_t += text #dönen metin sonucunu tüm metinler değişkenimizdeki diğer metinlere ekliyoruz
            image_counter += 1 #sayacı 1 arttırıyoruz.

        download_text_from_result(all_t, file.name, language) #indirilebilir dosya oluşturmak için tüm metin değişkenini, dosya ismini ve dili parametrik olarak gönderiyoruz.

       
    st.balloons() #metin çıkarım işlemi yaptıktan sonra streamlit balonlarını gösteriyoruz (işlem başarılı anlamında)

# Resim dosyasından metin çıkarımı fonksiyonu
def extract_text_from_image(file, language):
    st.write("Resim dosyasından metin çıkarımı")

    input_image = Image.open(file)  # resim dosyasını pillow kütüphanesi yardımı ile okuyoruz
    st.image(input_image)  # resmi ekran gösteriyoruz

    with st.spinner("Resimden OCR işlemi çalışıyor!"):

        result = pytesseract.image_to_string(input_image, lang=language) # tesseract'a resim dosyasını ve dil parametresini gönderiyoruz ve metin çıktısını result olarak alıyoruz

        st.write(result) # dönen metni ekrana yazdırıyoruz. 

        # indirilebilir dosya oluşturmak için result değişkenini, dosya ismini ve dili parametrik olarak gönderiyoruz.
        download_text_from_result(result, file.name, language)
    
    st.balloons()  # metin çıkarım işlemi yaptıktan sonra streamlit balonlarını gösteriyoruz (işlem başarılı anlamında)


# indirilebilir dosya oluşturmak gereken fonksiyon
def download_text_from_result(text_data, filename, ocrdili):
    st.markdown(f'<h4 class="text-danger">{"3. Adım"}</h4>', unsafe_allow_html=True)#ekrana açıklama yazıyoruz
    st.markdown(f'Metini aşağıdaki bağlantıdan indirebilirsiniz', unsafe_allow_html=True)#ekrana açıklama yazıyoruz
    indirilecek_dosya = filename + ocrdili + ".txt" #indirilecek dosyanın adını dil parametresi ile oluşturuyoruz
    b64 = base64.b64encode(text_data.encode()).decode() #dosyayı indirilebilir hale getirmek için encode-decode işlemi yapıyoruz, yoksa streamlit'de oluşmuyor
    href = f'<a class="btn btn-success text-light" href="data:file/txt;base64,{b64}" download="{indirilecek_dosya}"><i class="fa fa-download"></i> Metin Dosyasını İndir</a>' # tıklanıp indirilebilmesi için html etiketi oluşturuyoruz
    st.markdown(href, unsafe_allow_html=True) #linkin ekranda gösterimini sağlıyoruz
    
#=======================================================
####### Kullanıcıya etkilesime girecegi sayfa ##########
#=======================================================

# Degiskenler tanimlaniyor
dil = "Türkçe"
ocr_dil = "tur"

#Sayfa tasarımı için bootstrap css dosyası ve iconlar için font awesome dosyası sisteme ekleniyor.
# unsafe_allow_html=True dememizin sebebi streamlit'e yazılanların text olarak değilde html olarak görünmesini istemek için.
st.markdown("""<link rel="stylesheet" href="https://getbootstrap.com/docs/4.0/dist/css/bootstrap.min.css" >""", unsafe_allow_html=True)
st.markdown("""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" >""", unsafe_allow_html=True)

#Sayfa Basligi
st.markdown(f'<h1 class="mb-2 bg-danger text-white text-center" style="border-radius: 30px 30px 0px 0px;">{"WEB OCR"}</h1>', unsafe_allow_html=True)

#Alt Baslik
st.markdown(f'<h4 class="bg-secondary text-white text-center">{"Resim ve PDF Dosyalarından Metin Çıkarma"}</h4>', unsafe_allow_html=True)
st.markdown("")

# Adım 1 : Dosya Yukleme ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
with st.container():
    st.markdown(f'<h4 class="text-danger">{"1. Adım"}</h4>', unsafe_allow_html=True) #1. adım başlığı
    st.markdown(f'Lütfen Resim veya PDF belgenizi yükleyiniz.', unsafe_allow_html=True) #1. adım yonergesi
    #dosya yükleyici
    file = st.file_uploader(label = "",type=['png','jpg','jpeg', 'pdf']) 
st.markdown("")
# Adım 1 Bitir ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# Adım 2 : Dil Secimi :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if file is not None:
    with st.container():
        st.markdown(f'<h4 class="text-danger">{"2. Adım"}</h4>', unsafe_allow_html=True) #2. adım başlığı
        st.markdown(f' Belgenin hangi dilde okunmasını (OCR) istiyorsunuz?', unsafe_allow_html=True) #2. adım yönergesi
        #streamlit e Türkçe ve İngilizce adında 2 seçenek oluşturması için verilen komut.
        dil = st.radio("", ('Türkçe', 'İngilizce'))
        # Seçim'e göre hangi dilde OCR işleminin yapılacağı hakkında kullanıcıya bilgi veriliyor
        if dil == 'Türkçe':
            st.markdown(f'{"Belge üzerinde"}<span class="text-success font-weight-bold"> Türkçe </span> {" OCR işlemi uygulanacaktır."}', unsafe_allow_html=True)    
        else:
            st.markdown(f'{"Belge üzerinde"}<span class="text-success font-weight-bold"> İngilizce </span> {" OCR işlemi uygulanacaktır."}', unsafe_allow_html=True) 
# Adım 2 : Dil Secimi Bitir :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

#Eğer Türkçe seçilmiş ise tesseract-ocr-tur paketi seçilerek OCR yapılsın diye radio butondan aldığımız değişkenin içeriğini güncelliyoruz.
if dil == "Türkçe":
    ocr_dil = "tur"
elif dil == "İngilizce":
    ocr_dil = "eng"

# Adım 3 : İslem Baslatma Butonu ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if file is not None:  # eğer yüklenen dosya boş değilse, yani herhangi bir dosya yüklenmiş ise
    if st.button('Başlat'): # Eğer başlat butonuna basılmışsa
        if file.type == "application/pdf": #yüklenen dosya türü pdf ise 
            st.markdown(f'<p>{"Dosya Türü:"} <i class="fa fa-file-pdf-o" style="font-size:30px;color:red"></i> PDF</p>', unsafe_allow_html=True) #dosyanın tipini ekrana yazdırıyoruz
            extract_text_from_pdf(file, ocr_dil) #pdfden metin çıkarımı fonksiyonuna git
        elif file.type == "image/png" or " image/jpg" or " image/jpeg":  #yüklenen dosya türü resim dosyalarından biri ise (jpeg, jpg ya da png)
            st.markdown(f'<p>{"Dosya Türü:"} <i class="fa fa-file-image-o" style="font-size:30px;color:green"></i> Resim</p>', unsafe_allow_html=True) #dosyanın tipini ekrana yazdırıyoruz
            extract_text_from_image(file, ocr_dil) #resimden metin çıkarımı fonksiyonuna git
else:
    #yüklenen dosya boş ise ya da desteklenen dosya türünde değilse ekrana uyarı metni göster
    st.markdown(f'<div class="alert alert-danger" role="alert">Lütfen bir Resim veya PDF belgesi yükleyiniz!</div>', unsafe_allow_html=True)
            
st.caption("❤️ @avsaresra tarafından geliştirilmiştir.") 
