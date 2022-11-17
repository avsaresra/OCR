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

st.markdown("")

#dosya yükleyici
file = st.file_uploader(label = "Resim veya PDF belgelerinizi buradan yükleyebilirsiniz",type=['png','jpg','jpeg', 'pdf'])

#dil seçeneklerini gösterdiğimiz radio düğmeleri için streamlit'de kullanılan bölüm
dil = st.radio("Belgenin hangi dilde okunmasını (OCR) istiyorsunuz?", ('Türkçe', 'İngilizce'))

ocr_dil = "tur"

#Eğer Türkçe seçilmiş ise tesseract-ocr-tur paketi seçilerek OCR yapılsın diye radio butondan aldığımız değişkenin içeriğini güncelliyoruz.
if dil == "Türkçe":
    ocr_dil = "tur"
elif dil == "İngilizce":
    ocr_dil = "eng"

if dil == 'Türkçe':
    st.write('Belge üzerinde Türkçe OCR işlemi uygulanacaktır.')
else:
    st.write('Belge üzerinde İngilizce OCR işlemi uygulanacaktır.')

#PDF dosyasından metin çıkarımı fonksiyonu
def extract_text_from_pdf(file, language):
    st.write("PDF dosyasından metin çıkarımı")

    PDF_file = file
    #pages = convert_from_bytes(PDF_file.read(), output_folder=".", poppler_path=r'usr\bin')
    
    #işlem devam ederken spinner/dönen yuvarlak gösteriyoruz.
    with st.spinner("PDF'den OCR işlemi çalışıyor!"):
        doc = fitz.open(stream=PDF_file.read(), filetype="pdf") #dosya yükleyiciden gelen pdf dosyasını açıp doc değişkenine kaydediyoruz
        images = [] #tesseracta göndermek için boş bir resim dizisi oluşturuyoruz.
        image_counter = 1 #sayaç
        all_t = "" #bulunan tüm metinler için kullandığımız değişken
        for page in doc: #doc değişkenindeki her bir sayfa için teker teker işlem yapıyoruz.
            pix = page.get_pixmap() #sayfanın görüntüsünü alıyor ve pix değişkenine aktarıyoruz
            filename = "page_" + str(image_counter) + ".JPEG" #dosya adını sayaç ile birlikte değişken isimde oluşturuyoruz
            #st.write(filename)
            pix.save(filename) #pix değişkenindeki resim dosyasını kaydediyoruz.
            images.append(filename) #resim dizisine bu dosya adını ekliyoruz
            st.spinner(text='PDF OCR işlemi devam ediyor...')
            text = pytesseract.image_to_string(filename, lang=language) #tesseract'ın resimden metin çıkarımı fonksiyonuna kaydettiğimiz dosya adı ve dil parametresini veriyoruz
            all_t += text #dönen metin sonucunu tüm metinler değişkenimizdeki diğer metinlere ekliyoruz
            image_counter += 1 #sayacı 1 arttırıyoruz.

        download_text_from_result(all_t, file.name, language) #indirilebilir dosya oluşturmak için tüm metin değişkenini, dosya ismini ve dili parametrik olarak gönderiyoruz.

        #for img in images:
        #   os.remove(img)
    st.balloons() #metin çıkarım işlemi yaptıktan sonra streamlit balonlarını gösteriyoruz (işlem başarılı anlamında)

# Resim dosyasından metin çıkarımı fonksiyonu
def extract_text_from_image(file, language):
    st.write("Resim dosyasından metin çıkarımı")

    input_image = Image.open(file)  # resim dosyasını pillow kütüphanesi yardımı ile okuyoruz
    st.image(input_image)  # resmi ekran gösteriyoruz

    with st.spinner("Resimden OCR işlemi çalışıyor!"):

        result = pytesseract.image_to_string(input_image, lang=language) # tesseract'a resim dosyasını ve dil parametresini gönderiyoruz ve metin çıktısını result olarak alıyoruz
        
        result_text = []  # empty list for results
        
        st.write(result) # dönen metni ekrana yazdırıyoruz. 

        # indirilebilir dosya oluşturmak için result değişkenini, dosya ismini ve dili parametrik olarak gönderiyoruz.
        download_text_from_result(result, file.name, language)
    
    st.balloons()  # metin çıkarım işlemi yaptıktan sonra streamlit balonlarını gösteriyoruz (işlem başarılı anlamında)


# indirilebilir dosya oluşturmak gereken fonksiyon
def download_text_from_result(text_data, filename, ocrdili):
    st.write(" ### Metni aşağıdaki bağlantıdan indirebilirsiniz ###") #ekrana açıklama yazıyoruz
    indirilecek_dosya = filename + ocrdili + ".txt" #indirilecek dosyanın adını dil parametresi ile oluşturuyoruz
    b64 = base64.b64encode(text_data.encode()).decode() #dosyayı indirilebilir hale getirmek için encode-decode işlemi yapıyoruz, yoksa streamlit'de oluşmuyor
    href = f'<a href="data:file/txt;base64,{b64}" download="{indirilecek_dosya}">Buraya Tıklayın!!!</a>' # tıklanıp indirilebilmesi için html etiketi oluşturuyoruz
    st.markdown(href, unsafe_allow_html=True) #linkin ekranda gösterimini sağlıyoruz


if file is not None:  # eğer yüklenen dosya boş değilse, yani herhangi bir dosya yüklenmiş ise
    st.write("Dosya türü: " + file.type) #dosyanın tipini ekrana yazdırıyoruz

    if file.type == "application/pdf": #yüklenen dosya türü pdf ise 
        extract_text_from_pdf(file, ocr_dil) #pdfden metin çıkarımı fonksiyonuna git
    elif file.type == "image/png" or " image/jpg" or " image/jpeg": #yüklenen dosya türü resim dosyalarından biri ise (jpeg, jpg ya da png)
        extract_text_from_image(file, ocr_dil) #resimden metin çıkarımı fonksiyonuna git
    
else:
    st.write("Lütfen bir resim ya da PDF belgesi yükleyiniz") #yüklenen dosya boş ise ya da desteklenen dosya türünde değilse ekrana uyarı metni göster
    

st.caption("❤️ @avsaresra tarafından geliştirilmiştir.")
