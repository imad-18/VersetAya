import streamlit as st
import speech_recognition as sr
import ply.lex as lex
import ply.yacc as yacc

from usefull_functions import *


# Storing the verses of Surah Ad-Duha in an array
Surat_Doha = (
    "والضحى",
    "والليل إذا سجى",
    "ما ودعك ربك وما قلى",
    "وللآخرة خير لك من الأولى",
    "ولسوف يعطيك ربك فترضى",
    "ألم يجدك يتيما فآوى",
    "ووجدك ضالا فهدى",
    "ووجدك عائلا فأغنى",
    "فأما اليتيم فلا تقهر",
    "وأما السائل فلا تنهر",
    "وأما بنعمة ربك فحدث",
)

# Define timestamps for each verse (in seconds) to play it later
verse_timestamps = {
    "والضحى": (0, 8),
    "والليل إذا سجى": (8.2, 11.4),
    "ما ودعك ربك وما قلى": (11.5, 16),
    "وللآخرة خير لك من الأولى": (16.2, 21.5),
    "ولسوف يعطيك ربك فترضى": (21.6, 26.5),
    "ألم يجدك يتيما فآوى": (26.8, 32),
    "ووجدك ضالا فهدى": (32.35, 39.7),
    "ووجدك عائلا فأغنى": (39.6, 46),
    "فأما اليتيم فلا تقهر": (46.2, 51.2),
    "وأما السائل فلا تنهر": (51.4, 57.7),
    "وأما بنعمة ربك فحدث": (58, 64),
}

translation = {
    "والضحى": {
        "fr": "Par le Jour Montant!",
        "en": "By the morning brightness",
        "nl": "Bij het ochtendlicht.",
    },
    "والليل": {
        "fr": "Et par la nuit",
        "en": "And [by] the night",
        "nl": "En bij de nacht",
    },
    "إذا": {"fr": "quand", "en": "when", "nl": "wanneer"},
    "سجى": {
        "fr": "elle couvre tout",
        "en": "it covers with darkness",
        "nl": "het geheel donker is",
    },
    "ما": {"fr": "ne", "en": "not", "nl": "niet"},
    "ودعك": {
        "fr": "t'a abandonné",
        "en": "has taken leave of you",
        "nl": "heeft jou verlaten",
    },
    "ربك": {"fr": "ton Seigneur", "en": "your Lord", "nl": "jouw Heer"},
    "وما": {"fr": "et ne", "en": "nor", "nl": "en niet"},
    "قلى": {
        "fr": "t'a détesté",
        "en": "has He detested [you]",
        "nl": "is Hij kwaad [op jou]",
    },
    "وللآخرة": {
        "fr": "et la vie dernière",
        "en": "and the Hereafter",
        "nl": "en het latere (het Hiernamaals)",
    },
    "خير": {"fr": "est meilleure", "en": "is better", "nl": "is zeker beter"},
    "لك": {"fr": "pour toi", "en": "for you", "nl": "voor jou"},
    "من": {"fr": "que", "en": "than", "nl": "dan"},
    "الأولى": {
        "fr": "la vie présente",
        "en": "the first [life]",
        "nl": "het eerste (het wereldse leven)",
    },
    "ولسوف": {"fr": "et certainement", "en": "and surely", "nl": "en zeker"},
    "يعطيك": {
        "fr": "Il t'accordera",
        "en": "He will give you",
        "nl": "zal Hij jou schenken",
    },
    "فترضى": {
        "fr": "et alors tu seras satisfait",
        "en": "and you will be satisfied",
        "nl": "zodat jij tevreden zult zijn",
    },
    "ألم": {"fr": "ne", "en": "Did [He] not", "nl": "Heeft [Hij] niet"},
    "يجدك": {"fr": "Il t'a trouvé", "en": "find you", "nl": "jou gevonden"},
    "يتيما": {"fr": "orphelin", "en": "an orphan", "nl": "als wees"},
    "فآوى": {
        "fr": "alors Il t'a accueilli",
        "en": "and gave [you] refuge",
        "nl": "en jou in bescherming genomen",
    },
    "ووجدك": {
        "fr": "et Il t'a trouvé",
        "en": "and found you",
        "nl": "en Hij heeft jou gevonden",
    },
    "ضالا": {"fr": "égaré", "en": "lost", "nl": "dwalend"},
    "فهدى": {
        "fr": "alors Il t'a guidé",
        "en": "and guided [you]",
        "nl": "en jou geleid",
    },
    "عائلا": {"fr": "pauvre", "en": "poor", "nl": "behoeftig"},
    "فأغنى": {
        "fr": "alors Il t'a enrichi",
        "en": "and made [you] self-sufficient",
        "nl": "en rijk gemaakt",
    },
    "فأما": {"fr": "quant à", "en": "so as for", "nl": "wat betreft"},
    "اليتيم": {"fr": "l'orphelin", "en": "the orphan", "nl": "de wees"},
    "فلا": {"fr": "donc ne", "en": "then do not", "nl": "beledig hem niet"},
    "تقهر": {"fr": "le maltraite pas", "en": "oppress [him]", "nl": "beledig hem niet"},
    "السائل": {"fr": "le demandeur", "en": "the petitioner", "nl": "de bedelaar"},
    "تنهر": {"fr": "le repousse pas", "en": "repel [him]", "nl": "wijs hem niet af"},
    "بنعمة": {"fr": "au bienfait", "en": "the favor", "nl": "de gunsten"},
    "ربك": {"fr": "de ton Seigneur", "en": "of your Lord", "nl": "van jouw Heer"},
    "فحدث": {"fr": "proclame-le", "en": "report [it]", "nl": "spreek daarover"},
}


# Token list
tokens = ("WORD",)


# Regular expression for tokens
def t_WORD(t):
    r"\S+"
    return t


# tells the lexer to ignore spaces, tabs, and newlines.
t_ignore = " \t\n"


# handles encountered chars
def t_error(t):
    print(f"Caractère invalide : {t.value[0]}")
    t.lexer.skip(1)


# Analyseur lexical de texte
lexer = lex.lex()


# --Grammar rules for parsing
def p_text(p):
    """text : words"""
    # Concatenate words into a single string
    p[0] = " ".join(p[1])


def p_words(p):
    """words : words WORD
    | WORD"""
    if len(p) == 3:  # If there are multiple words
        p[0] = p[1] + [p[2]]  # Append the word to the list
    else:  # Single word
        p[0] = [p[1]]


def p_error(p):
    print("Syntax error in input!")


# Initialize the parser
parser = yacc.yacc()


# 1-Function to validate the user's input verse
def validate_verse(user_input, surat_name):
    # Tokenize and parse the input
    result = parser.parse(user_input, lexer=lexer)
    # Check if the parsed result matches any correct verse
    return result in surat_name




# Example Usage
user_input = "والضحى"
print(user_input)
is_correct = validate_verse(user_input, Surat_Doha)

if is_correct:
    print("Correct! The input matches the verse.\n")
    verse_infos(user_input, Surat_Doha)
    user_choice = input("Would you like to translate the verse Y/n ? ")
    if user_choice.lower() != "n":  # Handle both 'n' and 'N'
        language_choice = input(
            "Choose a language for translation:\nFrench --> 1\nEnglish --> 2\nHolland --> 3\n"
        )
        tr = translate_verse(user_input, language_choice, translation)
        print(f"Translation: {tr}")
    else:
        print("---- Done ----")
    # Audio_Player_fct
    play_choice = input("Do you want to play this verse? (y/n): ").lower()
    if play_choice == "y":
        print(play_verse(user_input, verse_timestamps))  # Only call if user chooses 'y'
    else:
        print("You chose not to play the verse.")

else:
    print("Incorrect! The input does not match the verse.")
