# 📱 Social Moca Manager

App Streamlit per generare testi Instagram con il tone of voice del brand Moca.

![Moca Logo](https://mocainteractive.com/assets/svg/logo.svg)

## 🚀 Funzionalità

- **Analisi intelligente**: L'AI analizza il tuo input e cerca post simili nell'archivio per replicarne stile e struttura
- **Matching per tipologia**: Se chiedi un post di benvenuto, l'AI usa come riferimento i post di benvenuto esistenti
- **Hashtag coerenti**: Usa SOLO hashtag già presenti nei post di riferimento
- **Memoria modifiche**: Ricorda l'ultimo testo generato per applicare modifiche successive
- **Copia veloce**: Pulsante per copiare il testo con un click

## 📋 Requisiti

- Python 3.8+
- API key OpenAI (già integrata via secrets)

## 🛠️ Installazione Locale

```bash
# Clona il repository
git clone https://github.com/mocainteractive/social-moca-manager.git
cd social-moca-manager

# Installa le dipendenze
pip install -r requirements.txt

# Crea il file secrets (se non esiste)
mkdir -p .streamlit
echo '[openai]
api_key = "LA_TUA_API_KEY"' > .streamlit/secrets.toml

# Avvia l'app
streamlit run app.py
```

## 💡 Come Usare

1. **Descrivi il post** - Includi info specifiche (nomi, ruoli, dettagli)
2. **Genera** - L'AI trova post simili e ne replica lo stile
3. **Modifica** - Chiedi modifiche al testo appena generato (es. "accorcia", "cambia tono")
4. **Copia** - Usa il pulsante rosso per copiare

### Esempi di input

**Post di benvenuto:**
> Post benvenuto. Marco, nuovo SEO Specialist. Ama i videogiochi e il trekking.

**Richiesta modifica:**
> Accorcia il testo e togli l'ultimo paragrafo

## 🔗 Deploy su Streamlit Cloud

1. Vai su https://share.streamlit.io
2. Connetti il repository: `mocainteractive/social-moca-manager`
3. Main file: `app.py`
4. **Settings → Secrets** → Aggiungi:
```toml
[openai]
api_key = "sk-..."
```
5. Deploy!

## 📁 Struttura File

```
├── app.py              # App principale
├── style.css           # Styling Moca
├── posts_data.json     # Archivio post di riferimento
├── requirements.txt    # Dipendenze
├── .streamlit/
│   └── secrets.toml    # API key (non su Git)
└── README.md
```

---

**Fatto con ❤️ per il team Moca**
