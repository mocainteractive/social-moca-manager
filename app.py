import streamlit as st
import json
import os
from openai import OpenAI

# Page configuration
st.set_page_config(
    page_title="Social Moca Manager",
    page_icon="🔴",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Also add Google Fonts link
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Figtree:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

load_css()

# Load Instagram posts data
@st.cache_data
def load_posts():
    json_path = os.path.join(os.path.dirname(__file__), "posts_data.json")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def get_sample_posts(posts, n=15):
    """Get sample posts with captions for context"""
    sample_posts = []
    for post in posts[:n]:
        if post.get("caption"):
            sample_posts.append({
                "caption": post["caption"],
                "hashtags": post.get("hashtags", []),
                "type": post.get("type", "Unknown")
            })
    return sample_posts

def generate_post(client, user_request, sample_posts):
    """Generate Instagram post using OpenAI"""
    
    # Build context from sample posts
    posts_context = "\n\n---\n\n".join([
        f"Post ({p['type']}):\n{p['caption']}"
        for p in sample_posts
    ])
    
    # Analyze common hashtags
    all_hashtags = []
    for p in sample_posts:
        all_hashtags.extend(p.get("hashtags", []))
    common_hashtags = list(set(all_hashtags))[:10]
    
    prompt = f"""Sei un copywriter per Moca Interactive, un'agenzia di digital marketing con sede a Treviso, Italia.

Devi scrivere un post Instagram che rispetti ESATTAMENTE lo stile dei post precedenti forniti come riferimento. NON essere creativo, replica fedelmente lo stile.

POST DI RIFERIMENTO DA IMITARE:
{posts_context}

HASHTAG DA USARE (usa SOLO questi, non inventarne altri):
{', '.join(['#' + h for h in common_hashtags])}

REGOLE TASSATIVE:
1. Usa SOLO gli hashtag elencati sopra, NON aggiungerne di nuovi
2. Replica esattamente lo stile di scrittura dei post di riferimento
3. Usa le emoji con la stessa frequenza e stile dei post di riferimento
4. Mantieni la stessa struttura: hook, corpo, CTA (se presente nei riferimenti)
5. Scrivi in italiano
6. NON essere più formale o informale dei post di riferimento
7. La LUNGHEZZA del post deve essere simile a quella dei post di riferimento (non più lungo, non più corto)

RICHIESTA:
{user_request}

Genera SOLO il testo del post, nient'altro."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Sei un esperto copywriter specializzato in social media marketing per agenzie digitali italiane."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    
    return response.choices[0].message.content

# Sidebar configuration
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <img src="https://mocainteractive.com/assets/svg/logo.svg" style="max-width: 120px;">
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚙️ Configurazione")
    
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="sk-...",
        help="Inserisci la tua API key OpenAI"
    )
    
    st.divider()
    
    st.markdown("### ℹ️ Info")
    st.markdown("""
        <div style="font-size: 0.85em; opacity: 0.8;">
        Questa app analizza i tuoi post Instagram precedenti per generare nuovi testi con lo stesso tone of voice.
        </div>
    """, unsafe_allow_html=True)

# Main content
st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <img src="https://mocainteractive.com/assets/svg/logo.svg" style="max-width: 180px;">
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <h1 style="text-align: center; font-family: 'Figtree', sans-serif; font-weight: 700; margin-bottom: 10px;">Social Moca Manager</h1>
    <p style="text-align: center; font-size: 1.1em; color: #8A8A8A; margin-bottom: 30px;">
    Genera testi per i post Instagram mantenendo il tone of voice del brand Moca.
    </p>
""", unsafe_allow_html=True)

# Load posts
posts = load_posts()

st.divider()

# User input
st.markdown("### 📝 Che tipo di post vuoi creare?")

user_request = st.text_area(
    label="Descrivi il contenuto del post",
    placeholder="Descrivimi che testo vuoi creare",
    height=120,
    label_visibility="collapsed"
)

# Additional options
col1, col2 = st.columns(2)
with col1:
    include_cta = st.checkbox("Includi Call-to-Action", value=True)
with col2:
    include_link_bio = st.checkbox("Menziona 'Link in bio'", value=False)

# Generate button
st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)

if st.button("✨ Genera Post", use_container_width=True):
    if not api_key:
        st.error("⚠️ Inserisci la tua API key OpenAI nella sidebar")
    elif not user_request:
        st.error("⚠️ Descrivi il tipo di post che vuoi creare")
    elif not posts:
        st.error("⚠️ Nessun post di riferimento disponibile")
    else:
        # Enhance request with options
        enhanced_request = user_request
        if include_cta:
            enhanced_request += "\n\nIncludi una call-to-action efficace."
        if include_link_bio:
            enhanced_request += "\n\nMenziona 'Link in bio' alla fine."
        
        with st.spinner("🔄 Generazione in corso..."):
            try:
                client = OpenAI(api_key=api_key)
                sample_posts = get_sample_posts(posts, n=15)
                generated_text = generate_post(client, enhanced_request, sample_posts)
                
                st.markdown("### 📄 Post Generato")
                
                # Single styled text area for display and copy
                st.text_area(
                    "Post generato",
                    generated_text,
                    height=300,
                    label_visibility="collapsed",
                    key="generated_output"
                )
                st.info("💡 Seleziona tutto il testo (Cmd+A) e copia (Cmd+C)")
                
            except Exception as e:
                st.error(f"❌ Errore durante la generazione: {str(e)}")

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; color: #8A8A8A; font-size: 0.85em; padding: 20px 0;">
        Fatto con ❤️ per il team Moca
    </div>
""", unsafe_allow_html=True)
