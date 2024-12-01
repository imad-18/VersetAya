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
    "والضحى": {"fr": "Par le Jour Montant!", "en": "By the morning brightness"},
    "والليل": {"fr": "Et par la nuit", "en": "And [by] the night"},
    "إذا": {"fr": "quand", "en": "when"},
    "سجى": {"fr": "elle couvre tout", "en": "it covers with darkness"},
    "ما": {"fr": "ne", "en": "not"},
    "ودعك": {"fr": "t'a abandonné", "en": "has taken leave of you"},
    "ربك": {"fr": "ton Seigneur", "en": "your Lord"},
    "وما": {"fr": "et ne", "en": "nor"},
    "قلى": {"fr": "t'a détesté", "en": "has He detested [you]"},
    "وللآخرة": {"fr": "et la vie dernière", "en": "and the Hereafter"},
    "خير": {"fr": "est meilleure", "en": "is better"},
    "لك": {"fr": "pour toi", "en": "for you"},
    "من": {"fr": "que", "en": "than"},
    "الأولى": {"fr": "la vie présente", "en": "the first [life]"},
    "ولسوف": {"fr": "et certainement", "en": "and surely"},
    "يعطيك": {"fr": "Il t'accordera", "en": "He will give you"},
    "فترضى": {"fr": "et alors tu seras satisfait", "en": "and you will be satisfied"},
    "ألم": {"fr": "ne", "en": "Did [He] not"},
    "يجدك": {"fr": "Il t'a trouvé", "en": "find you"},
    "يتيما": {"fr": "orphelin", "en": "an orphan"},
    "فآوى": {"fr": "alors Il t'a accueilli", "en": "and gave [you] refuge"},
    "ووجدك": {"fr": "et Il t'a trouvé", "en": "and found you"},
    "ضالا": {"fr": "égaré", "en": "lost"},
    "فهدى": {"fr": "alors Il t'a guidé", "en": "and guided [you]"},
    "عائلا": {"fr": "pauvre", "en": "poor"},
    "فأغنى": {"fr": "alors Il t'a enrichi", "en": "and made [you] self-sufficient"},
    "فأما": {"fr": "quant à", "en": "so as for"},
    "اليتيم": {"fr": "l'orphelin", "en": "the orphan"},
    "فلا": {"fr": "donc ne", "en": "then do not"},
    "تقهر": {"fr": "le maltraite pas", "en": "oppress [him]"},
    "السائل": {"fr": "le demandeur", "en": "the petitioner"},
    "تنهر": {"fr": "le repousse pas", "en": "repel [him]"},
    "بنعمة": {"fr": "au bienfait", "en": "the favor"},
    "ربك": {"fr": "de ton Seigneur", "en": "of your Lord"},
    "فحدث": {"fr": "proclame-le", "en": "report [it]"},
}
# Print the verses
#for verse in translation:
#    print(verse)
#print(Surat_Al_Alak)


# Token list
tokens = (
    'WORD',
)

# Regular expression for tokens
def t_WORD(t):
    r'\S+'
    return t

#tells the lexer to ignore spaces, tabs, and newlines.
t_ignore = ' \t\n'

#handles encountered chars
def t_error(t):
    print(f"Caractère invalide : {t.value[0]}")
    t.lexer.skip(1)

# Analyseur lexical de texte 
lexer = lex.lex()

# --Grammar rules for parsing
def p_text(p):
    '''text : words'''
    # Concatenate words into a single string
    p[0] = " ".join(p[1])

def p_words(p):
    '''words : words WORD
             | WORD'''
    if len(p) == 3:  # If there are multiple words
        p[0] = p[1] + [p[2]]  # Append the word to the list
    else:  # Single word
        p[0] = [p[1]]

def p_error(p):
    print("Syntax error in input!")

# Initialize the parser
parser = yacc.yacc()

# Function to validate the user's input verse
def validate_verse(user_input, correct_verses):
    # Tokenize and parse the input
    result = parser.parse(user_input, lexer=lexer)
    # Check if the parsed result matches any correct verse
    return result in correct_verses

# Example Usage
input("والليل إنذا سجى")  # Simulated user input
is_correct = validate_verse(user_input, Surat_Al_Alak)

if is_correct:
    print("Correct! The input matches the verse.")
else:
    print("Incorrect! The input does not match the verse.")