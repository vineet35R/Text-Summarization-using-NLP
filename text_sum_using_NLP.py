import streamlit as st
import subprocess
import sys
import spacy
import logging
from langdetect import detect
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Language model mapping
LANG_MODELS = {
    "en": "en_core_web_sm",
    "es": "es_core_news_sm",
    "fr": "fr_core_news_sm",
    "de": "de_core_news_sm"
}

# Load spaCy model for a given language
def load_spacy_model(language_code):
    model = LANG_MODELS.get(language_code, "en_core_web_sm")
    try:
        return spacy.load(model)
    except OSError:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", model])
        return spacy.load(model)

# Summarizer function
def summarizer(raw_text, summary_ratio=0.4):
    if not isinstance(raw_text, str) or not raw_text.strip():
        return "Invalid input: Text must be a non-empty string.", 0, 0

    try:
        detected_lang = detect(raw_text)
        logging.info(f"Detected language: {detected_lang}")
    except Exception as e:
        return f"Language detection error: {str(e)}", 0, 0

    nlp = load_spacy_model(detected_lang)
    stopwords = nlp.Defaults.stop_words
    doc = nlp(raw_text)

    word_freq = {}
    for token in doc:
        word = token.text.lower()
        if word not in stopwords and word not in punctuation:
            word_freq[word] = word_freq.get(word, 0) + 1

    if not word_freq:
        return "Error: No meaningful words found to summarize.", 0, 0

    max_freq = max(word_freq.values())
    word_freq = {word: freq / max_freq for word, freq in word_freq.items()}

    sent_scores = {sent: sum(word_freq.get(token.text.lower(), 0) for token in sent) for sent in doc.sents}

    if not sent_scores:
        return "Error: No meaningful sentences found to summarize.", 0, 0

    select_len = max(1, int(len(list(doc.sents)) * summary_ratio))
    summary_sentences = nlargest(select_len, sent_scores, key=sent_scores.get)

    summary = ' '.join([sent.text for sent in summary_sentences])
    return summary.strip(), len(raw_text.split()), len(summary.split())

# ----------------- Streamlit UI -------------------
st.set_page_config(page_title="Multilingual Text Summarizer", layout="centered")
st.title("🧠 Multilingual Text Summarizer")
st.markdown("Upload a `.txt` file or paste your text below:")

uploaded_file = st.file_uploader("Upload text file", type=["txt"])
default_text = ""

if uploaded_file:
    default_text = uploaded_file.read().decode("utf-8")

text_input = st.text_area("Paste your text here", value=default_text, height=250)

col1, col2 = st.columns(2)
with col1:
    summarize_btn = st.button("🔍 Summarize")
with col2:
    reset_btn = st.button("🔄 Reset")

if "summary_output" not in st.session_state:
    st.session_state.summary_output = ""
    st.session_state.word_stats = (0, 0)

if summarize_btn:
    with st.spinner("Generating summary..."):
        if text_input.strip():
            summary, orig_len, summ_len = summarizer(text_input)
            st.session_state.summary_output = summary
            st.session_state.word_stats = (orig_len, summ_len)
        else:
            st.warning("Please upload or paste some text.")

if reset_btn:
    st.session_state.summary_output = ""
    st.session_state.word_stats = (0, 0)
    st.experimental_rerun()

if st.session_state.summary_output:
    st.subheader("📋 Summary")
    st.write(st.session_state.summary_output)
    st.markdown("---")
    st.write(f"🔹 **Original Length:** {st.session_state.word_stats[0]} words")
    st.write(f"🔹 **Summary Length:** {st.session_state.word_stats[1]} words")

# to run use this code --  streamlit run text_sum_using_NLP.py
