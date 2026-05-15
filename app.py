import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi API
# Ganti dengan API Key Anda dari Google AI Studio
API_KEY = "AIzaSyCXCbiOG38k7JZR5yyOruflM1rV1JeWhyY" 
genai.configure(api_key=API_KEY)

# Menggunakan model Gemini 1.5 Flash karena cepat dan sangat baik untuk teks
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Pengaturan Tampilan Halaman Web
st.set_page_config(page_title="AI Asisten Guru", page_icon="💡", layout="centered")

st.title("💡 Generator Ide Sentra Belajar")
st.write("Rancang kegiatan yang menyenangkan, bermakna, dan merangsang tumbuh kembang anak.")

# 3. Form Input untuk Guru
with st.form("form_ide_belajar"):
    col1, col2 = st.columns(2)
    
    with col1:
        tema = st.text_input("Tema Pembelajaran", placeholder="Contoh: Keluargaku, Tanaman Buah, Cuaca")
        usia = st.selectbox("Kelompok Usia", ["Kelompok Bermain (3-4 Tahun)", "TK A (4-5 Tahun)", "TK B (5-6 Tahun)", "SD Kelas Bawah"])
        
    with col2:
        aspek = st.selectbox("Fokus Perkembangan Utama", ["Kognitif & Literasi", "Motorik Kasar/Halus", "Sosial Emosional", "Seni & Kreativitas", "Nilai Agama & Moral"])
        durasi = st.selectbox("Estimasi Durasi", ["15-30 Menit", "30-45 Menit", "60 Menit+"])

    bahan_tersedia = st.text_input("Bahan yang ada di kelas (opsional)", placeholder="Contoh: Kardus bekas, botol plastik, daun kering")
    
    submit_button = st.form_submit_button(label="Rancang Kegiatan Sekarang 🚀")

# 4. Logika Pemrosesan AI
if submit_button:
    if not tema:
        st.error("Mohon isi Tema Pembelajaran terlebih dahulu.")
    else:
        with st.spinner("Menganalisis tema dan menyusun ide kegiatan..."):
            
            # Ini adalah "Secret Sauce" - Prompt terstruktur yang disembunyikan dari user
            prompt_sistem = f"""
            Anda adalah seorang ahli pendidikan anak usia dini dan pengembang kurikulum yang inovatif. 
            Buatkan 1 ide kegiatan sentra belajar atau *loose parts* yang spesifik, praktis, dan kreatif berdasarkan data berikut:
            - Tema: {tema}
            - Usia Anak: {usia}
            - Fokus Perkembangan: {aspek}
            - Durasi: {durasi}
            - Bahan yang tersedia: {bahan_tersedia if bahan_tersedia else 'Bebas, utamakan bahan sehari-hari yang murah'}
            
            Format jawaban Anda harus persis seperti ini (Gunakan Markdown):
            
            ### 🎯 [Nama Kegiatan yang Menarik dan Unik]
            
            **🧠 Tujuan Pembelajaran:**
            (Jelaskan singkat 1-2 kalimat apa yang akan dicapai anak, kaitkan dengan {aspek})
            
            **📦 Alat & Bahan:**
            - (Daftar bahan berbentuk bullet points)
            
            **👣 Langkah-langkah Kegiatan:**
            1. (Langkah 1)
            2. (Langkah 2)
            3. (Langkah 3...)
            
            **💡 Tips Guru:**
            (Berikan 1-2 kalimat saran praktis untuk guru saat mendampingi anak dalam kegiatan ini, misalnya pertanyaan pemantik yang bisa diajukan ke anak).
            """
            
            try:
                # Memanggil API Gemini
                response = model.generate_content(prompt_sistem)
                
                # Menampilkan Hasil
                st.success("Ide kegiatan berhasil dibuat!")
                st.markdown("---")
                st.markdown(response.text)
                st.markdown("---")
                
            except Exception as e:
                st.error(f"Terjadi kesalahan saat menghubungi AI: {e}")
