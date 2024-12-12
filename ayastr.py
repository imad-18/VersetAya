import ply.yacc as yacc
import ply.lex as lex
from usefull_functions import *

import sys
import arabic_reshaper
from bidi.algorithm import get_display

import streamlit as st

# Ensure UTF-8 encoding is used
sys.stdout.reconfigure(encoding="utf-8")

# Tokens declaration: Position-based tokens for each word in the Ayat
tokens = ["FIRST", "SECOND", "THIRD", "FOURTH", "FIFTH", "SIXTH", "SEVENTH"]

# Regular expressions for each position
t_ignore = " \t\n"

# Words of the Surah based on their positions
t_FIRST = r"والضحى|والليل|ما|وللآخرة|ولسوف|ألم|ووجدك|فأما|وأما|بِسْمِ|الْحَمْدُ|الرَّحْمَنِ|مَالِكِ|إِيَّاكَ|اهْدِنَا|صِرَاطَ|غَيْرِ"
t_SECOND = r"إذا|ودعك|خير|يعطيك|يجدك|ضالا|اليتيم|السائل|بنعمة|اللَّهِ|لِلَّهِ|الرَّحِيمِ|يَوْمِ|نَعْبُدُ|الصِّرَاطَ|الَّذِينَ|الْمَغْضُوبِ"
t_THIRD = (
    r"سجى|ربك|لك|يتيما|فهدى|فلا|ربك|الرَّحْمَنِ|رَبِّ|الرَّحِيمِ|الدِّينِ|وَإِيَّاكَ|مُسْتَقِيمَ|أَنْعَمْتَ|عَلَيْهِمْ"
)
t_FOURTH = r"وما|من|ترضى|فآوى|فهدى|تقهر|تنهر|فحدث|الرَّحِيمِ|الْعَالَمِينَ"
t_FIFTH = r"قلى|الأولى|فأغنى|مَالِكِ|يَوْمِ|الدِّينِ"
t_SIXTH = r"فهدى|إِيَّاكَ|نَعْبُدُ|وَإِيَّاكَ|نَسْتَعِينُ"
t_SEVENTH = r"فأغنى|اهْدِنَا|الصِّرَاطَ|الْمُسْتَقِيمَ"


# Error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

# Predefined Ayat of Surat Ad-Duha , Surah Al-Fatiha


# ----------------------------------------
# YACC: Grammar Rules
# ----------------------------------------


# Helper functions
def validate_verse(verse, surah):
    return verse in surah


# Parsing rules
def p_ayah(p):
    """
    ayah : FIRST
         | FIRST SECOND
         | FIRST SECOND THIRD
         | FIRST SECOND THIRD FOURTH
         | FIRST SECOND THIRD FOURTH FIFTH
         | FIRST SECOND THIRD FOURTH FIFTH SIXTH
         | FIRST SECOND THIRD FOURTH FIFTH SIXTH SEVENTH
    """
    # Perform validation when the validate button is clicked
    if validate_button:
        p[0] = " ".join(data.split())  # Simulate processing of input text
        if p[0] not in valid_ayat1 and valid_ayat2:
            resh = arabic_reshaper.reshape(p[0])
            resh = get_display(resh)
            st.error(f"Invalid Ayah: {p[0]}")
        else:
            resh = arabic_reshaper.reshape(p[0])
            resh = get_display(resh)
            st.success(f"Valid Ayah: {p[0]}")

            # Save valid Ayah in session state
            st.session_state["valid_ayah"] = p[0]

    # Check if a valid Ayah exists in session state
    if "valid_ayah" in st.session_state:
        valid_ayah = st.session_state["valid_ayah"]

        # Display additional buttons
        col1, col2, col3 = st.columns(
            [
                2,
                2,
                2,
            ]
        )
        with col1:
            # Select the language
            language_choice = st.selectbox(
                "",
                options=["French", "English", "Holland"],
                index=None,  # Default value is None
                placeholder="Language...",
            )

        with col2:
            st.markdown('<div class="button-row">', unsafe_allow_html=True)
            play_button = st.button("Play")
            st.markdown("</div>", unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="button-row">', unsafe_allow_html=True)
            info_button = st.button("Show info")
            st.markdown("</div>", unsafe_allow_html=True)

        # Handle info button click
        if info_button:
            st.title("Ayah Information Display")
            verse_info = verse_infos(valid_ayah, valid_ayat1, Tafsir_Doha)
            st.text_area("", value=verse_info, height=200)
        if language_choice:
            translate_button = st.button("Translate")

            # Define the mapping of languages to their corresponding codes
            language_map = {"French": "1", "English": "2", "Holland": "3"}

            # Check if the user has selected a language and inputted a valid Ayah
            if translate_button:
                if language_choice and data:
                    language_code = language_map[language_choice]

                    # Get the translation result
                    st.title(f"{language_choice} Translation:")
                    translate = translate_verse(data, language_code, translation)

                    # Display the translated verse in the text area
                    st.text_area("", value=translate, height=100)
                else:
                    if not data:
                        st.warning("Please enter an Ayah to translate.")
                    if not language_choice:
                        st.warning("Please select a language for translation.")

        if play_button:
            play_verse(data3, verse_timestamps)

        user_choice = input("Would you like to translate the verse Y/n? ").lower()
        if user_choice != "n":
            language_choice = input(
                "Choose a language for translation:\nFrench --> 1\nEnglish --> 2\nHolland --> 3\n"
            )
            if p[0] in valid_ayat1:
                tr = translate_verse(p[0], language_choice, translation)
                print(f"Translation: {tr}")
            else:
                tr = translate_verse(p[0], language_choice, translation_Alfatiha)
                print(f"Translation: {tr}")
        else:
            print("Translation skipped.")

        # Audio playback option
        play_choice = input("Do you want to play this verse? (y/n): ").lower()
        if play_choice == "y":
            print(play_verse(data3, verse_timestamps))
        else:
            print("Audio playback skipped.")


# Build the parser
parser = yacc.yacc()


def p_error(p):
    print("Syntax error in input!")


# ----------------------------------------
# Test Input: Full Surat Ad-Duha
# ----------------------------------------
# Inject custom CSS for better alignment
st.markdown(
    """
    <style>
    .button-row {      
        border-top-width: 1px;
        margin-top: 28px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <style>
    .appTitle{       
        font-size: 34px;
        font-weight: bold;
        display: flex;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Now, wrap the title text with the class in a custom HTML div
st.markdown('<div class="appTitle">آيات من الذكر الحكيم</div>', unsafe_allow_html=True)
col1, col2 = st.columns([4, 1])
with col1:
    data = st.text_input("", placeholder="Enter your Ayah here:")
    # data3 var is needed for the play_verse fct
    # ifcuz the timestamps array is defiened with verses with only 1 whitespaces
    data2 = data.split()
    data3 = " ".join(data2)
    # st.success(data3)
with col2:
    # Create a flex container to align the button
    st.markdown('<div class="button-row">', unsafe_allow_html=True)
    validate_button = st.button("Validate")
    st.markdown("</div>", unsafe_allow_html=True)

# data = st.text_input("Enter your Ayah here:")

lexer.input(data)

# Parse each Ayah
for line in data.split("\n"):
    if line.strip():
        print(f"\nParsing: {get_display(arabic_reshaper.reshape(line.strip()))}")
        parser.parse(line)
