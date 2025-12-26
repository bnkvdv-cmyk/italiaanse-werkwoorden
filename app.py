import streamlit as st
import spacy
from langdetect import detect
from deep_translator import GoogleTranslator

st.set_page_config(page_title="Italiaanse Werkwoorden", layout="wide")

st.title("🇮🇹 Italiaanse werkwoorden → Nederlands")

uploaded_file = st.file_uploader("Upload een Italiaans tekstbestand (.txt)", type="txt")

if uploaded_file:
    text = uploaded_file.read().decode("utf-8")

    try:
        language = detect(text)
    except:
        language = "it"

    if language != "it":
        st.error("Dit is geen Italiaanse tekst.")
    else:
        nlp = spacy.load("it_core_news_sm")
        doc = nlp(text)

        st.subheader("Tekst met werkwoorden")
        output = ""
        uitleg = []

        for token in doc:
            if token.pos_ == "VERB":
                output += f"<u>{token.text}</u> "
                vertaling = GoogleTranslator(source="it", target="nl").translate(token.lemma_)
                uitleg.append(
                    f"**{token.text}** → *{vertaling}*  \n"
                    f"- Infinitief: {token.lemma_}  \n"
                    f"- Grammatica: {token.morph}"
                )
            else:
                output += token.text + " "

        st.markdown(output, unsafe_allow_html=True)

        st.subheader("Uitleg per werkwoord")
        for u in uitleg:
            st.markdown(u)
