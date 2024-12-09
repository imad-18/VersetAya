import ply.yacc as yacc
import ply.lex as lex
from usefull_functions import *

import sys
import arabic_reshaper
from bidi.algorithm import get_display

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
    p[0] = " ".join(p[1:])  # Combine tokens into a string representing the Ayah
    if p[0] not in valid_ayat1 and valid_ayat2:
        resh = arabic_reshaper.reshape(p[0])
        resh = get_display(resh)
        print(f"Invalid Ayah: {resh}")
    else:
        resh = arabic_reshaper.reshape(p[0])
        resh = get_display(resh)
        print(f"Valid Ayah: {resh}")
        if p[0] in valid_ayat1:
            verse_infos(p[0], valid_ayat1, Tafsir_Doha)
        else:
            verse_infos(p[0], valid_ayat2, Tafsir_ALfatiha)
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
            print(play_verse(p[0], verse_timestamps))
        else:
            print("Audio playback skipped.")


# Build the parser
parser = yacc.yacc()


def p_error(p):
    print("Syntax error in input!")


# ----------------------------------------
# Test Input: Full Surat Ad-Duha
# ----------------------------------------

data = """
والضحى
والليل إذا سجى
ما ودعك ربك وما قلى
والضحى إذا
"بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ
"""

lexer.input(data)

# Parse each Ayah
for line in data.split("\n"):
    if line.strip():
        print(f"\nParsing: {get_display(arabic_reshaper.reshape(line.strip()))}")
        parser.parse(line)
