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

def generate_post(client, user_request, all_posts, previous_output=None):
    """Generate Instagram post using OpenAI with intelligent post matching"""
    
    # Build full context from ALL posts for the AI to analyze
    posts_context = "\n\n---\n\n".join([
        f"Post #{i+1}:\n{p['caption']}\nHashtags: {', '.join(['#' + h for h in p.get('hashtags', [])])}"
        for i, p in enumerate(all_posts) if p.get("caption")
    ])
    
    # Add previous output context if modifying
    modification_context = ""
    if previous_output:
        modification_context = f"""\n\nTESTO PRECEDENTE DA MODIFICARE:
{previous_output}

L'utente vuole modificare questo testo. Applica le modifiche richieste mantenendo lo stile."""
    
    prompt = f"""Sei un copywriter per Moca Interactive.

ESEMPI DI POST REALI DI MOCA (studia lo stile):
{posts_context}

INPUT DA ELABORARE:
{user_request}

IL TUO COMPITO:
1. Identifica il TIPO di post richiesto cercando esempi simili sopra
2. Dall'input, ESTRAI solo 2-3 fatti chiave sulla persona/argomento (nome, ruolo, 1-2 caratteristiche uniche)
3. RISCRIVI completamente quei fatti nello stile Moca - NON copiare frasi dall'input!
4. Usa SOLO hashtag che vedi negli esempi simili sopra

REGOLE FERREE:
❌ NON copiare MAI frasi intere dall'input dell'utente
❌ NON usare le stesse parole/espressioni dell'utente
❌ NON inventare hashtag - usa SOLO quelli degli esempi simili
❌ NON scrivere post più lunghi di quelli negli esempi

✅ SINTETIZZA le info in poche righe come fanno i post di esempio
✅ USA lo stesso tono e struttura degli esempi simili
✅ SELEZIONA solo i dettagli più interessanti/unici da menzionare
✅ RISCRIVI tutto con parole tue nello stile Moca

Il post DEVE sembrare originale, scritto da zero, NON un riassunto dell'input.
{modification_context}

Scrivi SOLO il testo del post finale."""

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
                # Check if this is a modification request
                previous_output = st.session_state.get('last_generated_text', None)
                generated_text = generate_post(client, enhanced_request, posts, previous_output)
                
                st.markdown("### 📄 Post Generato")
                
                # Store in session state for future modifications
                st.session_state['last_generated_text'] = generated_text
                
                # Single styled text area for display
                st.text_area(
                    "Post generato",
                    generated_text,
                    height=300,
                    label_visibility="collapsed",
                    key="generated_output"
                )
                
                # Copy button using base64 encoding to avoid character issues
                import base64
                encoded_text = base64.b64encode(generated_text.encode('utf-8')).decode('utf-8')
                st.markdown(f'''
                    <button onclick="navigator.clipboard.writeText(atob('{encoded_text}')).then(() => {{
                        this.innerHTML = '✅ Copiato!';
                        setTimeout(() => this.innerHTML = '📋 Copia tutto il testo', 2000);
                    }})"
                        style="background-color: #E52217; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-family: 'Figtree', sans-serif; font-weight: 600; margin-top: 10px;">
                        📋 Copia tutto il testo
                    </button>
                ''', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Errore durante la generazione: {str(e)}")

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; color: #8A8A8A; font-size: 0.85em; padding: 20px 0;">
        Fatto con ❤️ per il team Moca
    </div>
""", unsafe_allow_html=True)
