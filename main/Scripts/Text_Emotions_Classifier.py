import os
import moviepy.editor as mp
import speech_recognition as sr
from transformers import pipeline
import re
from collections import Counter
import assemblyai as aai

# Initialize the sentiment analysis pipeline
emotion = pipeline('sentiment-analysis', model='arpanghoshal/EmoRoBERTa')

def transcribe(video_path):
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
    return transcribed_text

# Function to predict emotion for each sentence in the transcribed text
def get_emotion_label(text):
    # Split the text into sentences using regex
    sentences = re.split(r'\.\s+', text)

    # Predict emotion for each sentence
    emotions = {}
    for sentence in sentences:
        # Ignore empty sentences
        if sentence.strip():
            emotion_label = emotion(sentence)[0]['label']
            emotions[sentence] = emotion_label

    return emotions

# Function to get emotion summary
def get_emotion_summary(emotions):
    # Count the occurrences of each emotion
    emotion_counts = Counter(emotions.values())
    total_sentences = len(emotions)
    
    # Calculate emotion percentages
    emotion_percentages = {emotion: count / total_sentences * 100 for emotion, count in emotion_counts.items()}
    return emotion_percentages

def main(video_path):
    # Transcribe the audio file into text
    transcription = transcribe(video_path)
    if transcription:
        print("Transcription:", transcription)
        
        # Get individual sentence emotions
        emotions = get_emotion_label(transcription)

        # Print emotion for each sentence
        print("\nIndividual Sentence Emotions:")
        for sentence, emotion_label in emotions.items():
            print(f"Sentence: {sentence.strip()} | Emotion: {emotion_label}")

        # Get emotion summary
        emotion_summary = get_emotion_summary(emotions)

        # Print emotion summary
        print("\nEmotion Summary:")
        score = 0
        for emotion, percentage in emotion_summary.items():
            print(f"{emotion}: {percentage:.2f}%")
            if emotion.lower() in ['disapproval', 'fear' , 'anger', 'disappointment', 'annoyance', 'confusion', 'disgust', 'grief', 'nervousness', 'sadness']:
                score += int(percentage)
        print("Calculating Score...")
        print("Score:", score)
        return score

if __name__ == "__main__":
    video_path = 'D:/Koleya/InstaJobAppFinal/InstaJobApp/Testing/Tell Me About Yourself.mp4'
    main(video_path)
