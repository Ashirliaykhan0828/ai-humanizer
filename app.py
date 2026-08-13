import streamlit as st
from groq import Groq

# Səhifə parametrləri və dizayn
st.set_page_config(layout="wide", page_title="AI Humanizer", page_icon="✍️")

st.markdown("""
<style>
    .stTextArea textarea {
        background-color: #1E1E1E;
        color: white;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# Groq API Açarını alırıq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except KeyError:
    st.error("API açarı tapılmadı! Zəhmət olmasa Streamlit 'Secrets' bölməsinə GROQ_API_KEY əlavə edin.")
    st.stop()

st.markdown("<h2 style='text-align: center;'>AI Humanizer Pro</h2>", unsafe_allow_html=True)
st.write("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Orijinal Mətn")
    user_input = st.text_area(
        "Zaman kodlu xam mətni bura yapışdırın:", 
        height=450, 
        placeholder="[00:00] Şü anda, ılıksınız. Bunu fark etmiyor olabilirsiniz..."
    )
    submit_button = st.button("✨ Revizə Et", use_container_width=True)

with col2:
    st.subheader("Varyasyonlar")
    tab1, tab2 = st.tabs(["⚙️ Revize 1 (Peşəkar)", "⚙️ Revize 2 (Səmimi)"])
    
    if submit_button:
        if user_input.strip() == "":
            st.warning("Zəhmət olmasa əvvəlcə mətn daxil edin!")
        else:
            with st.spinner("Süni intellekt mətni insaniləşdirir..."):
                try:
                    # Birinci versiya - Peşəkar ton
                    chat_completion1 = client.chat.completions.create(
                        messages=[
                            {
                                "role": "system",
                                "content": "Sən peşəkar bir məzmun redaktorusan. Göndərilən mətndəki bütün zaman kodlarını (məs. [00:16]) sil. Mətni robotik tondan çıxar, axıcı, təbii və insan tərəfindən yazılmış kimi yenidən formalaşdır. Mənanı mütləq qoru."
                            },
                            {
                                "role": "user",
                                "content": user_input,
                            }
                        ],
                       model="llama-3.1-70b-versatile",
                    )
                    
                    # İkinci versiya - Səmimi ton
                    chat_completion2 = client.chat.completions.create(
                        messages=[
                            {
                                "role": "system",
                                "content": "Sən səmimi bir hekayəçisən. Göndərilən mətndəki zaman kodlarını sil. Mətni dinləyici ilə birbaşa danışırmış kimi səmimi, axıcı bir podcast mətni kimi yenidən yaz. Süni intellekt üslubundan uzaq dur."
                            },
                            {
                                "role": "user",
                                "content": user_input,
                            }
                        ],
                        model="llama-3.1-70b-versatile",
                    )
                    
                    with tab1:
                        st.write(chat_completion1.choices[0].message.content)
                    with tab2:
                        st.write(chat_completion2.choices[0].message.content)
                        
                except Exception as e:
                    st.error(f"Xəta baş verdi: {e}")
