# Text-Summarization-using-NLP
A multilingual text summarization web app built with Streamlit. Users can upload or paste text, and the app detects language, processes it using spaCy, and returns a concise summary. Features include file upload, live text input, summarization, and reset functionality—all running via Streamlit.
yaml
Copy
Edit
# 🧠 Multilingual Text Summarizer
A simple and powerful Streamlit app for summarizing text in multiple languages using spaCy NLP models and language detection.

## 🌍 Supported Languages
- English 🇬🇧
- Spanish 🇪🇸
- French 🇫🇷
- German 🇩🇪
- 
## 🚀 Features

✅ Automatically detects the input text language  
✅ Uses spaCy’s language-specific models  
✅ Filters out stopwords and punctuation  
✅ Generates summaries based on sentence importance  
✅ Clean, interactive UI with Streamlit

---

## 📸 App Preview
![image](https://github.com/user-attachments/assets/01de3448-29a2-4cfc-b0e9-2e5dc569415d)

## I use Frequency-Based methid
Input Text (English, Short):
"AI is changing the world. It helps in healthcare and education. People use AI for automation."

1. Token Frequency:
Filtered tokens (no stopwords or punctuation):
ai:2, changing:1, world:1, helps:1, healthcare:1, education:1, people:1, use:1, automation:1

👉 Max freq = 2 (for “ai”)

2. Normalized Word Frequencies:
ai: 1.0
changing: 0.5
world: 0.5
helps: 0.5
healthcare: 0.5
education: 0.5
people: 0.5
use: 0.5
automation: 0.5

3. Sentence Scores:
S1: “AI is changing the world.” → Score = 1.0 + 0.5 + 0.5 = 2.0

S2: “It helps in healthcare and education.” → Score = 0.5 + 0.5 + 0.5 = 1.5

S3: “People use AI for automation.” → Score = 0.5 + 0.5 + 1.0 + 0.5 = 2.5

 4. Select Top Sentences (e.g., 50% summary → top 1 or 2 sentences)
Pick top 2: S3 and S1

✅ Final Summary:
"People use AI for automation. AI is changing the world."
