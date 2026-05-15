# 4. Logika Pemrosesan AI
if submit_button:
    if not tema:
        st.error("Mohon isi Tema Pembelajaran terlebih dahulu.")
    else:
        with st.spinner("Menganalisis tema dan menyusun ide kegiatan..."):
            prompt_sistem = f"""
            Anda adalah seorang ahli pendidikan anak usia dini dan pengembang kurikulum yang inovatif. 
            Buatkan 1 ide kegiatan sentra belajar atau loose parts yang spesifik, praktis, dan kreatif berdasarkan data berikut:
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
                # PERCOBAAN PERTAMA: Menggunakan Model 2.5 (Utama)
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt_sistem
                )
                st.success("✨ Ide kegiatan berhasil dibuat!")
                st.markdown("---")
                st.markdown(response.text)
                st.markdown("---")
                
            except Exception as error_utama:
                # JIKA 2.5 GAGAL: Sistem akan memberikan info dan beralih ke 2.0
                st.info("Sistem utama sedang sibuk, beralih ke server cadangan...")
                
                try:
                    # PERCOBAAN KEDUA (Fallback): Menggunakan Model 2.0
                    response = client.models.generate_content(
                        model='gemini-2.0-flash',
                        contents=prompt_sistem
                    )
                    st.success("✨ Ide kegiatan berhasil dibuat! (Via server cadangan)")
                    st.markdown("---")
                    st.markdown(response.text)
                    st.markdown("---")
                    
                except Exception as error_cadangan:
                    # JIKA KEDUANYA GAGAL
                    st.error("Mohon maaf, semua server AI sedang penuh saat ini. Silakan coba beberapa menit lagi.")
