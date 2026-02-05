# 📱 Social Moca Manager

App Streamlit per generare testi Instagram con il tone of voice del brand Moca.

![Moca Logo](https://mocainteractive.com/assets/svg/logo.svg)

## 🚀 Funzionalità

- **Analisi del tone of voice**: L'app analizza 100 post Instagram esistenti per replicare lo stile di scrittura
- **Generazione AI**: Utilizza OpenAI GPT-4o per creare testi coerenti con il brand
- **Opzioni personalizzabili**: Call-to-Action e "Link in bio" opzionali
- **Brand Identity**: Design con colori e font Moca

## 🎨 Brand Colors

| Colore | HEX |
|--------|-----|
| Rosso Moca | `#E52217` |
| Rosso Chiaro | `#FFE7E6` |
| Nero | `#191919` |
| Grigio | `#8A8A8A` |

**Font**: Figtree

## 📋 Requisiti

- Python 3.8+
- API key OpenAI

## 🛠️ Installazione Locale

```bash
# Clona il repository
git clone https://github.com/mocainteractive/social-moca-manager.git
cd social-moca-manager

# Installa le dipendenze
pip install -r requirements.txt

# Avvia l'app
streamlit run app.py
```

## 💡 Come Usare

1. **Inserisci la tua API key OpenAI** nella sidebar
2. **Descrivi il post** che vuoi creare (es. "Post per lanciare un nuovo servizio SEO")
3. **Seleziona le opzioni** desiderate (Call-to-Action, Link in bio)
4. **Clicca "Genera Post"** e copia il testo generato

## 📁 Struttura File

```
├── app.py              # App principale Streamlit
├── style.css           # CSS con brand styling
├── posts_data.json     # 100 post Instagram di riferimento
├── requirements.txt    # Dipendenze Python
└── README.md           # Documentazione
```

## 🔑 Configurazione API Key

L'API key OpenAI va inserita nella sidebar dell'app. Per ottenere una API key:
1. Vai su https://platform.openai.com
2. Crea un account o accedi
3. Genera una nuova API key in "API Keys"

---

**Fatto con ❤️ per il team Moca**
