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

def generate_post(client, user_request, all_posts):
    """Generate Instagram post using OpenAI with intelligent post matching"""
    
    # Build full context from ALL posts for the AI to analyze
    posts_context = "\n\n---\n\n".join([
        f"Post #{i+1}:\n{p['caption']}\nHashtags: {', '.join(['#' + h for h in p.get('hashtags', [])])}"
        for i, p in enumerate(all_posts) if p.get("caption")
    ])
    
    prompt = f"""Sei un copywriter per Moca Interactive. Il tuo compito è scrivere un post Instagram basandoti sui post esistenti del brand.

ARCHIVIO COMPLETO DEI POST MOCA:
{posts_context}

RICHIESTA DELL'UTENTE:
{user_request}

ISTRUZIONI:
1. ANALIZZA la richiesta dell'utente e identifica il TIPO di post richiesto (es: benvenuto nuovo membro, annuncio servizio, evento, tips, ecc.)
2. CERCA nell'archivio i post simili per tipologia alla richiesta
3. USA la STRUTTURA di quei post come modello (lunghezza, tono, uso emoji, formattazione)
4. USA SOLO gli hashtag che trovi in quei post simili, NON inventarne di nuovi
5. REPLICA fedelmente lo stile, NON essere più creativo o diverso dai post esistenti

ESEMPIO DI RAGIONAMENTO:
- Se l'utente chiede un post di benvenuto → cerca i post che parlano di "benvenuto", "nuovo arrivo", "team" e usa quella struttura e quegli hashtag
- Se chiede un post su un servizio → cerca i post che parlano di servizi e usa quella struttura
- Se chiede un post motivazionale → cerca i post con quel tono e usa quella struttura

GENERA il post seguendo ESATTAMENTE lo stile dei post simili trovati nell'archivio.
Scrivi SOLO il testo del post finale, nient'altro."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Sei un copywriter che replica esattamente lo stile dei post esistenti. Non sei creativo, sei un imitatore fedele."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
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
                generated_text = generate_post(client, enhanced_request, posts)
                
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
