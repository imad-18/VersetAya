import time
import pygame


# 2 -----------------------Add some infos-----------------------
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
        pygame.mixer.music.load("doha.mp3")
        
        # Start playback from the specified time
        pygame.mixer.music.play(start=start_time)
        print(f"Playing verse: '{user_input}' (from {start_time}s to {end_time}s)")

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
