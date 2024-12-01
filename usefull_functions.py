from pydub import AudioSegment
from pydub.playback import play

# Dictionary for verses and their timestamps (in seconds)
timestamps = {
    "والضحى": (0, 5),
    "والليل إذا سجى": (5, 12),
    "ما ودعك ربك وما قلى": (12, 20),
    "وللآخرة خير لك من الأولى": (20, 28),
    "ولسوف يعطيك ربك فترضى": (28, 35),
    "ألم يجدك يتيما فآوى": (35, 42),
    "ووجدك ضالا فهدى": (42, 50),
    "ووجدك عائلا فأغنى": (50, 58),
    "فأما اليتيم فلا تقهر": (58, 65),
    "وأما السائل فلا تنهر": (65, 72),
    "وأما بنعمة ربك فحدث": (72, 80),
}

def play_verse(verse, audio_file):
    """
    Play the specific verse from the audio file based on timestamps.
    :param verse: The verse to play
    :param audio_file: Path to the audio file
    """
    if verse in timestamps:
        start, end = timestamps[verse]
        audio = AudioSegment.from_file(audio_file)
        verse_audio = audio[start * 1000:end * 1000]  # Convert seconds to milliseconds
        print(f"Playing verse: {verse}")
        play(verse_audio)
    else:
        print("Verse not found in the timestamps dictionary.")

# Example usage
#user_input = input("Enter the verse: ")
audio_file_path = "audios/Surah_Doha.m4a"  # Replace with your audio file path
play_verse(user_input, audio_file_path)
