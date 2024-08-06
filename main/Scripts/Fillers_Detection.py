import assemblyai as aai
import re

def main(video_path):
    # Set up AssemblyAI API key
    aai.settings.api_key = "b50f9891241641f4983408a6fd7d6bf2"

    # Configure transcription with disfluencies enabled
    config = aai.TranscriptionConfig(disfluencies=True)
    transcriber = aai.Transcriber(config=config)

    # Transcribe the audio or video file
    transcript = transcriber.transcribe(video_path)
    # You can also transcribe from a local file like this:
    # transcript = transcriber.transcribe("./my-local-audio-file.wav")

    # Get the transcribed text
    transcribed_text = transcript.text

    # Define patterns for disfluency detection using regular expressions
    disfluency_patterns = [
        r"\bum\b", r"\buh\b", r"\bhmm\b", r"\bmhm\b", r"\buh-huh\b",
        r"\bah\b", r"\bhuh\b", r"\bhm\b", r"\bm\b"
    ]

    # Mapping of patterns to disfluency words
    pattern_to_word = {
        r"\bum\b": "um",
        r"\buh\b": "uh",
        r"\bhmm\b": "hmm",
        r"\bmhm\b": "mhm",
        r"\buh-huh\b": "uh-huh",
        r"\bah\b": "ah",
        r"\bhuh\b": "huh",
        r"\bhm\b": "hm",
        r"\bm\b": "m"
    }

    # Initialize a disfluency counter
    disfluency_counter = {pattern_to_word[pattern]: 0 for pattern in disfluency_patterns}

    # Count occurrences of each disfluency using regular expressions
    for pattern in disfluency_patterns:
        matches = re.findall(pattern, transcribed_text, flags=re.IGNORECASE)
        disfluency_word = pattern_to_word[pattern]
        disfluency_counter[disfluency_word] += len(matches)

    # Display counts of each disfluency
    for disfluency_word, count in disfluency_counter.items():
        print(f"{disfluency_word}: {count}")

    # Overall count of all disfluencies
    total_disfluencies = sum(disfluency_counter.values())
    print(f"Total Disfluencies: {total_disfluencies}")
    score = total_disfluencies
    print("Calculating Score...")
    print(score)
    return score
