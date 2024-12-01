import streamlit as st
import speech_recognition as sr
import ply.lex as lex
import ply.yacc as yacc

# Storing the verses of Surah Ad-Duha in an array
Surat_Al_Alak = (
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

translation = {
    "والضحى": {"fr": "Par le Jour Montant!", "en": "By the morning brightness", "nl": "Bij het ochtendlicht."},
    "والليل": {"fr": "Et par la nuit", "en": "And [by] the night", "nl": "En bij de nacht"},
    "إذا": {"fr": "quand", "en": "when", "nl": "wanneer"},
    "سجى": {"fr": "elle couvre tout", "en": "it covers with darkness", "nl": "het geheel donker is"},
    "ما": {"fr": "ne", "en": "not", "nl": "niet"},
    "ودعك": {"fr": "t'a abandonné", "en": "has taken leave of you", "nl": "heeft jou verlaten"},
    "ربك": {"fr": "ton Seigneur", "en": "your Lord", "nl": "jouw Heer"},
    "وما": {"fr": "et ne", "en": "nor", "nl": "en niet"},
    "قلى": {"fr": "t'a détesté", "en": "has He detested [you]", "nl": "is Hij kwaad [op jou]"},
    "وللآخرة": {"fr": "et la vie dernière", "en": "and the Hereafter", "nl": "en het latere (het Hiernamaals)"},
    "خير": {"fr": "est meilleure", "en": "is better", "nl": "is zeker beter"},
    "لك": {"fr": "pour toi", "en": "for you", "nl": "voor jou"},
    "من": {"fr": "que", "en": "than", "nl": "dan"},
    "الأولى": {"fr": "la vie présente", "en": "the first [life]", "nl": "het eerste (het wereldse leven)"},
    "ولسوف": {"fr": "et certainement", "en": "and surely", "nl": "en zeker"},
    "يعطيك": {"fr": "Il t'accordera", "en": "He will give you", "nl": "zal Hij jou schenken"},
    "فترضى": {"fr": "et alors tu seras satisfait", "en": "and you will be satisfied", "nl": "zodat jij tevreden zult zijn"},
    "ألم": {"fr": "ne", "en": "Did [He] not", "nl": "Heeft [Hij] niet"},
    "يجدك": {"fr": "Il t'a trouvé", "en": "find you", "nl": "jou gevonden"},
    "يتيما": {"fr": "orphelin", "en": "an orphan", "nl": "als wees"},
    "فآوى": {"fr": "alors Il t'a accueilli", "en": "and gave [you] refuge", "nl": "en jou in bescherming genomen"},
    "ووجدك": {"fr": "et Il t'a trouvé", "en": "and found you", "nl": "en Hij heeft jou gevonden"},
    "ضالا": {"fr": "égaré", "en": "lost", "nl": "dwalend"},
    "فهدى": {"fr": "alors Il t'a guidé", "en": "and guided [you]", "nl": "en jou geleid"},
    "عائلا": {"fr": "pauvre", "en": "poor", "nl": "behoeftig"},
    "فأغنى": {"fr": "alors Il t'a enrichi", "en": "and made [you] self-sufficient", "nl": "en rijk gemaakt"},
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


# 2-Add some infos 
def verse_infos(user_input, surat_name):
    # Strip whitespaces from the user input
    stripped_input = user_input.strip()
    try:
        # Find the position of the verse and print it
        position = surat_name.index(stripped_input) + 1
        print(f"The position of the verse: '{stripped_input}' is: {position}")
    except ValueError:
        # Handle cases where the input does not match any verse
        print(f"The verse '{stripped_input}' was not found in the Surah.")


# 3-Translation
def translate_verse(verse, language_choice, translation_dict):
    words = verse.split()  # Split the verse into words
    translated_words = []
    
    for word in words:
        if word in translation_dict:
            if language_choice == "1":  # French
                translated_words.append(translation_dict[word].get("fr", "Translation not available"))
            elif language_choice == "2":  # English
                translated_words.append(translation_dict[word].get("en", "Translation not available"))
            elif language_choice == "3":  #Holland
                translated_words.append(translation_dict[word].get("nl", "Translation not available"))
            else:
                return "Invalid language choice."
        else:
            translated_words.append(f"[{word}]")  # Handle missing words gracefully

    # Join the translated words into a complete sentence
    return " ".join(translated_words)


# Example Usage
user_input = "والليل إذا سجى" 
is_correct = validate_verse(user_input, Surat_Al_Alak)

if is_correct:
    print("Correct! The input matches the verse.\n")
    verse_infos(user_input, Surat_Al_Alak)
    user_choice = input("Would you like to translate the verse Y/n ? ")
    if user_choice.lower() != 'n':  # Handle both 'n' and 'N'
        language_choice = input("Choose a language for translation:\nFrench --> 1\nEnglish --> 2\nHolland --> 3\n")
        tr = translate_verse(user_input, language_choice, translation)
        print(f"Translation: {tr}")
    else:
        print("---- Done ----")
    # play_audio = input("Would you like to hear the verse? Y/n ")
    # if play_audio.lower() != "n":
    #     fctss.play_verse(user_input, audio_file_path)
else:
    print("Incorrect! The input does not match the verse.")
