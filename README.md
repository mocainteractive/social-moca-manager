# 📱 Social Moca Manager

App Streamlit per generare testi Instagram con il tone of voice del brand Moca.

![Moca Logo](https://mocainteractive.com/assets/svg/logo.svg)

## 🚀 Funzionalità

- **Analisi intelligente**: L'AI analizza il tuo input e cerca post simili nell'archivio per replicarne lo stile
- **Generazione fedele**: Usa SOLO hashtag e strutture presenti nei post esistenti
- **Memoria modifiche**: L'app ricorda l'ultimo testo generato per applicare modifiche successive
- **Copia veloce**: Pulsante per copiare il testo con un click
- **Brand Identity**: Design con colori Moca e font Figtree

## 🎨 Brand Colors

| Colore | HEX |
|--------|-----|
| Rosso Moca | `#E52217` |
| Rosso Chiaro | `#FFE7E6` |
| Nero | `#191919` |
| Grigio | `#8A8A8A` |

## 📋 Requisiti

- Python 3.8+
- API key OpenAI

## 🛠️ Installazione

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
2. **Descrivi il post** - Puoi includere info specifiche (nomi, ruoli, dettagli)
3. **Genera** - L'AI trova post simili e ne replica lo stile
4. **Modifica** - Chiedi modifiche al testo appena generato
5. **Copia** - Usa il pulsante rosso per copiare

### Esempi di input

**Post di benvenuto:**
> Post benvenuto. Marco, nuovo SEO Specialist. Ama i videogiochi e il trekking.

**Richiesta modifica:**
> Accorcia il testo e togli l'ultimo paragrafo

## 📁 Struttura File

```
├── app.py              # App principale Streamlit
├── style.css           # CSS con brand styling
├── posts_data.json     # Archivio post Instagram di riferimento
├── requirements.txt    # Dipendenze Python
└── README.md           # Documentazione
```

## � Deploy

**Repository GitHub:** https://github.com/mocainteractive/social-moca-manager

**Streamlit Cloud:**
1. Vai su https://share.streamlit.io
2. Connetti il repository GitHub
3. Seleziona `app.py` come main file
4. Deploy!

---

**Fatto con ❤️ per il team Moca**
