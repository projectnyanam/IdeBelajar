import streamlit as st
from google import genai

# ==========================================
# 1. KONFIGURASI API & CLIENT
# ==========================================
# Mengambil API Key dari Streamlit Secrets untuk keamanan
API_KEY = st.secrets["GEMINI_API_KEY"] 
client = genai.Client(api_key=API_KEY)

# Tentukan Link Montage Anda di sini agar mudah diubah kapan saja
LINK_MONTAGE = "https://omg10.com/4/10984630"

# ==========================================
# 2. PENGATURAN TAMPILAN HALAMAN (UI)
# ==========================================
st.set_page_config(
    page_title="Sentra Tumbuh Anak - Asisten AI", 
    page_icon="🌱", 
    layout="centered"
)

# Judul dan Deskripsi
st.title("🌱 Sentra Tumbuh Anak")
st.subheader("Generator Ide Belajar")
st.write("Rancang kegiatan kelas yang bermakna, menyenangkan, dan merangsang tumbuh kembang anak sesuai standar PAUD.")
st.markdown("---")

# ==========================================
# 3. FORMULIR INPUT GURU
# ==========================================
with st.form("form_ide_belajar"):
    col1, col2 = st.columns(2)
    
    with col1:
        tema = st.text_input("Tema Pembelajaran", placeholder="Contoh: Keluargaku, Alam Semesta, Cuaca")
        usia = st.selectbox("Kelompok Usia", [
            "Kelompok Bermain (3-4 Tahun)", 
            "TK A (4-5 Tahun)", 
            "TK B (5-6 Tahun)", 
            "SD Kelas Bawah"
        ])
        
    with col2:
        aspek = st.selectbox("Fokus Perkembangan Utama", [
            "Kognitif & Literasi", 
            "Motorik Kasar/Halus", 
            "Sosial Emosional", 
            "Seni & Kreativitas", 
            "Nilai Agama & Moral"
        ])
        durasi = st.selectbox("Estimasi Durasi", [
            "15-30 Menit", 
            "30-45 Menit", 
            "60 Menit+"
        ])

    bahan_tersedia = st.text_input("Bahan yang Ada di Kelas (Opsional)", placeholder="Contoh: Kardus bekas, botol plastik, daun kering")
    
    # Tombol eksekusi
    submit_button = st.form_submit_button(label="Rancang Kegiatan Sekarang 🚀")

# ==========================================
# 4. LOGIKA PEMROSESAN AI DENGAN FALLBACK & OPSI 2
# ==========================================
if submit_button:
    if not tema:
        st.error("Mohon isi Tema Pembelajaran terlebih dahulu.")
    else:
        with st.spinner("Menganalisis tema dan menyusun ide kegiatan..."):
            
            # Prompt terstruktur yang dikirim ke AI
            prompt_sistem = f"""
            Anda adalah seorang ahli pendidikan anak usia dini dan pengembang kurikulum yang inovatif. 
            Buatkan 1 ide kegiatan sentra belajar atau loose parts yang spesifik, praktis, dan kreatif berdasarkan data berikut:
            - Tema: {tema}
            - Usia Anak: {usia}
            - Fokus Perkembangan: {aspek}
            - Durasi: {durasi}
            - Bahan yang tersedia: {bahan_tersedia if bahan_tersedia else 'Bebas, utamakan bahan sehari-hari yang murah dan mudah didapat'}
            
            Format jawaban Anda harus persis seperti ini (Gunakan Markdown):
            
            ### 🎯 [Nama Kegiatan yang Menarik dan Unik]
            
            **🧠 Tujuan Pembelajaran:**
            (Jelaskan singkat 1-2 kalimat apa yang akan dicapai anak, kaitkan dengan fokus perkembangan {aspek})
            
            **📦 Alat & Bahan:**
            - (Daftar bahan berbentuk bullet points)
            
            **👣 Langkah-langkah Kegiatan:**
            1. (Langkah 1)
            2. (Langkah 2)
            3. (Langkah 3...)
            
            **💡 Tips Guru:**
            (Berikan 1-2 kalimat saran praktis, panduan scaffolding, atau pertanyaan pemantik terbuka yang bisa diajukan guru kepada anak saat kegiatan berlangsung).
            """
            
            try:
                # PERCOBAAN PERTAMA: Menggunakan Model 2.5 Flash (Utama)
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt_sistem
                )
                st.success("✨ Ide kegiatan berhasil dibuat!")
                st.markdown(response.text)
                
                # --- IMPLEMENTASI OPSI 2 (Tombol Link Buka Tab Baru) ---
                st.markdown("---")
                st.info("💡 Ingin melihat referensi visual atau materi tambahan?")
                st.link_button("🎥 Buka Link Montage", LINK_MONTAGE)
                
            except Exception as error_utama:
                # JIKA 2.5 GAGAL: Peringatan halus dan beralih ke 2.0
                st.info("Sistem utama sedang menyesuaikan, mencoba server cadangan...")
                
                try:
                    # PERCOBAAN KEDUA (Fallback): Menggunakan Model 2.0 Flash
                    response = client.models.generate_content(
                        model='gemini-2.0-flash',
                        contents=prompt_sistem
                    )
                    st.success("✨ Ide kegiatan berhasil dibuat! (Via server cadangan)")
                    st.markdown(response.text)
                    
                    # --- IMPLEMENTASI OPSI 2 PADA SERVER CADANGAN ---
                    st.markdown("---")
                    st.info("💡 Ingin melihat referensi visual atau materi tambahan?")
                    st.link_button("🎥 Buka Link Montage", LINK_MONTAGE)
                    
                except Exception as error_cadangan:
                    # JIKA KEDUANYA GAGAL
                    st.error("Mohon maaf, semua server AI sedang penuh saat ini. Silakan coba beberapa menit lagi.")

# ==========================================
# 5. FOOTER
# ==========================================
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 12px;'>Dikembangkan untuk mendukung pembelajaran yang menyenangkan & bermakna.</p>", unsafe_allow_html=True)
