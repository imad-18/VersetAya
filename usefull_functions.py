import time
import pygame

import arabic_reshaper
from bidi.algorithm import get_display

import sys

sys.stdout.reconfigure(encoding="utf-8")

import streamlit as st



# Predefined Ayat of Surat Ad-Duha , Surah Al-Fatiha
valid_ayat1 = [
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
]

valid_ayat2 = [
    "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
    "الرَّحْمَنِ الرَّحِيمِ",
    "مَالِكِ يَوْمِ الدِّينِ",
    "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ",
    "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ",
    "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ",
    "غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ",
]


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

Tafsir_Doha = [
    "أقسم الله بالنهار كله",
    """وبالليل إذا سكن بالخلق واشتد ظلامه, ويقسم الله بما يشاء من مخلوقاته
    , أما المخلوق فلا يجوز له أن يقسم بغير خالقه؟ فإن القسم بغير الله شرك.""",
    "ما تركك- يا محمد- ربك, وما أبغضك بإبطاء الوحي عنك.",
    "وللدار الآخرة خير لك من دار الدنيا,",
    "ولسوف يعطيك ربك- يا محمد- من أنواع الإنعام في الآخرة, فترضى بذلك.",
    "ألم يجدك من قبل يتيما, فآواك ورعاك,",
    "ووجدك لا تدري ما الكتب ولا الإيمان, فعلمك ما لم تكن تعلم, ووفقك لأحسن الأعمال؟",
    "ووجدك فقيرا, فساق لك رزقك, وأغنى نفسك بالقناعة والصبر؟",
    "فأما اليتيم فلا تسيء معاملته,",
    "وأما السائل فلا تزجره, بل أطعمه, واقض حاجته,",
    "وأما بنعمة ربك التي أسبغها عليك فتحدث بها.",
]


translation_Alfatiha = {
    "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ": {
        "fr": "Au nom d'Allah, le Tout Miséricordieux, le Très Miséricordieux.",
        "en": "In the name of Allah, the Most Gracious, the Most Merciful.",
        "nl": "In de naam van Allah, de Meest Barmhartige, de Meest Genadevolle."
    },
    "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ": {
        "fr": "Louange à Allah, Seigneur de l'univers.",
        "en": "Praise be to Allah, the Lord of all the worlds.",
        "nl": "Alle lof zij Allah, de Heer van alle werelden."
    },
    "الرَّحْمَنِ الرَّحِيمِ": {
        "fr": "Le Tout Miséricordieux, le Très Miséricordieux.",
        "en": "The Most Gracious, the Most Merciful.",
        "nl": "De Meest Barmhartige, de Meest Genadevolle."
    },
    "مَالِكِ يَوْمِ الدِّينِ": {
        "fr": "Maître du Jour de la Rétribution.",
        "en": "Master of the Day of Judgment.",
        "nl": "Heerser van de Dag des Oordeels."
    },
    "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ": {
        "fr": "C'est Toi seul que nous adorons, et c'est Toi seul dont nous implorons le secours.",
        "en": "You alone we worship, and You alone we ask for help.",
        "nl": "U alleen aanbidden wij, en U alleen vragen wij om hulp."
    },
    "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ": {
        "fr": "Guide-nous dans le droit chemin.",
        "en": "Guide us on the Straight Path.",
        "nl": "Leid ons op het rechte pad."
    },
    "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ": {
        "fr": "Le chemin de ceux que Tu as comblés de Tes bienfaits.",
        "en": "The path of those who have received Your grace.",
        "nl": "Het pad van degenen aan wie U Uw genade heeft geschonken."
    },
    "غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ": {
        "fr": "Non pas de ceux qui ont encouru Ta colère, ni des égarés.",
        "en": "Not the path of those who have brought down wrath upon themselves, nor of those who have gone astray.",
        "nl": "Niet het pad van degenen die Uw toorn hebben gewekt, noch van degenen die zijn afgedwaald."
    }
}
# French translation
# Access translations like this:
# print(translation["بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ"]["fr"])  




Tafsir_ALfatiha = [
    """سورة الفاتحة سميت هذه السورة بالفاتحة; لأنه يفتتح بها القرآن العظيم
    , وتسمى المثاني; لأنها تقرأ في كل ركعة, ولها أسماء أخر. أبتدئ قراءة القرآن
      باسم الله مستعينا به, (اللهِ) علم على الرب -تبارك وتعالى- المعبود بحق
      دون سواه, وهو أخص أسماء الله تعالى, ولا يسمى به غيره سبحانه. (الرَّحْمَنِ)
      ذي الرحمة العامة الذي وسعت رحمته جميع الخلق, (الرَّحِيمِ) بالمؤمنين, وهما
     اسمان من أسمائه تعالى، يتضمنان إثبات صفة الرحمة لله تعالى كما يليق بجلاله.
     """,
    """الثناء على الله بصفاته التي كلُّها أوصاف كمال, وبنعمه الظاهرة
       والباطنة، الدينية والدنيوية، وفي ضمنه أَمْرٌ لعباده أن يحمدوه,
       فهو المستحق له وحده, وهو سبحانه المنشئ للخلق, القائم بأمورهم,
       المربي لجميع خلقه بنعمه, ولأوليائه بالإيمان والعمل الصالح.
       """,
    """(الرَّحْمَنِ) الذي وسعت رحمته جميع الخلق,
        (الرَّحِيمِ), بالمؤمنين, وهما اسمان من أسماء الله تعالى.
       """,
    """وهو سبحانه وحده مالك يوم القيامة, وهو يوم الجزاء على الأعمال.
        وفي قراءة المسلم لهذه الآية في كل ركعة من صلواته تذكير له باليوم
        الآخر, وحثٌّ له على الاستعداد بالعمل الصالح, والكف عن المعاصي والسيئات.
        """,
    """إنا نخصك وحدك بالعبادة, ونستعين بك وحدك في جميع أمورنا,
        فالأمر كله بيدك, لا يملك منه أحد مثقال ذرة. وفي هذه الآية دليل على أن
        العبد لا يجوز له أن يصرف شيئًا من أنواع العبادة كالدعاء والاستغاثة
        والذبح والطواف إلا لله وحده, وفيها شفاء القلوب من داء
        التعلق بغير اله, ومن أمراض الرياء والعجب, والكبرياء.
        """,
    """دُلَّنا, وأرشدنا, ووفقنا إلى الطريق المستقيم,
        وثبتنا عليه حتى نلقاك, وهو الإسلام، الذي هو الطريق الواضح
        الموصل إلى رضوان الله وإلى جنته, الذي دلّ عليه خاتم رسله وأنبيائه
        محمد صلى الله عليه وسلم, فلا سبيل إلى سعادة العبد إلا بالاستقامة عليه.
        """,
    """طريق الذين أنعمت عليهم من النبيين والصدِّيقين والشهداء والصالحين, فهم أهل الهداية
        والاستقامة, ولا تجعلنا ممن سلك طريق المغضوب عليهم, الذين عرفوا الحق ولم يعملوا به,
        وهم اليهود, ومن كان على شاكلتهم, والضالين, وهم الذين لم يهتدوا, فضلوا الطريق,
        وهم النصارى, ومن اتبع سنتهم.
        """,
]


# 2 -----------------------Add some infos-----------------------
def verse_infos(user_input, surat_name, Tafssir):
    # Strip whitespaces from the user input
    stripped_input = user_input.strip()
    try:
        # Find the position of the verse and print it
        position = surat_name.index(user_input) + 1
        # print(f"The position of the verse: '{stripped_input}' ( {position})")
        # Reshape and display Arabic text for the result
        infos = f"""
        الاية رقم {position} 
        سورة الضحى
        {Tafssir[position-1]}
        """
        reshaped_text = arabic_reshaper.reshape(infos)
        bidi_text = get_display(reshaped_text)
        # print(bidi_text)
        return infos
    except ValueError:
        # Handle cases where the input does not match any verse
        # print(f"The verse '{stripped_input}' was not found in the Surah.")
        return f"The verse '{stripped_input}' was not found in the Surah."



# 3 -----------------------Translation-----------------------
def translate_verse(verse, language_choice, translation_dict):
    words = verse.split()  # Split the verse into words
    translated_words = []

    for word in words:
        if word in translation_dict:
            if language_choice == "1":  # French
                translated_words.append(
                    translation_dict[word].get("fr", "Translation not available")
                )
            elif language_choice == "2":  # English
                translated_words.append(
                    translation_dict[word].get("en", "Translation not available")
                )
            elif language_choice == "3":  # Holland
                translated_words.append(
                    translation_dict[word].get("nl", "Translation not available")
                )
            else:
                return "Invalid language choice."
        else:
            translated_words.append(f"[{word}]")  # Handle missing words gracefully

    # Join the translated words into a complete sentence
    return " ".join(translated_words)


# 4 -----------------------Play the verse-audio-----------------------
# Initialize the mixer
pygame.mixer.init()


# Play specific verse
def play_verse(user_input, verse_timestamps):
    if user_input in verse_timestamps:
        start_time, end_time = verse_timestamps[user_input]
        duration = end_time - start_time

        # Load the audio file
        pygame.mixer.music.load("audios/doha.mp3")

        # Start playback from the specified time
        pygame.mixer.music.play(start=start_time)
        verse = arabic_reshaper.reshape(user_input)
        bidi_text = get_display(verse)
        print(f"Playing verse: '{bidi_text}' (from {start_time}s to {end_time}s)")

        # Wait for the duration of the verse
        time.sleep(duration)

        # Stop playback after the verse duration
        pygame.mixer.music.stop()
        print("Finished playing the verse.")
    else:
        print(f"Verse '{user_input}' not found in timestamps.")


# ---Example usage
# user_input = "والليل إذا سجى".strip()
# play_verse(user_input, verse_timestamps)

# ---Quit the mixer after playback
# pygame.mixer.quit()


# 5 -----------------------Play the verse-translation-----------------------
# def play_translation(text, language="en"):
#     engine = pyttsx3.init()
#     # Set properties like voice (if multiple voices are available for translations)
#     engine.setProperty("rate", 150)  # Speed of speech
#     engine.setProperty("volume", 1)  # Volume (0.0 to 1.0)
#     engine.say(text)  # Queue the text for speaking
#     engine.runAndWait()  # Wait until the speech is finished

# # Example usage
# translation_text = "In the name of Allah, the Most Gracious, the Most Merciful"
# play_translation(translation_text, language="en")


# 5 -----------------------Play the verse-translation-V2-----------------------
# from gtts import gTTS
# import os

# def play_translation(text, language="en"):
#     # Convert text to speech
#     tts = gTTS(text=text, lang=language)
#     tts.save("translation.mp3")  # Save the audio file
#     os.system("start translation.mp3")  # Play the audio file (use 'start' on Windows, 'open' on macOS, or 'xdg-open' on Linux)

# # Example usage
# translation_text = "In the name of Allah, the Most Gracious, the Most Merciful"
# play_translation(translation_text, language="en")


# ------- GUI ------------


