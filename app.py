import os
import uuid
import requests
import gradio as gr
from openai import OpenAI
import azure.cognitiveservices.speech as speechsdk
import tempfile
from dotenv import load_dotenv
import time
import threading

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")
AZURE_TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
AZURE_TRANSLATOR_ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT")

VOICES = {
    "English": "en-US-BrianNeural",
    "Spanish": "es-US-PalomaNeural",
    "French": "fr-FR-LucienMultilingualNeural",
    "Deutsch": "de-DE-ChristophNeural",
    "Urdu": "ur-PK-AsadNeural"
}

SOURCE_LANGS = {
    "English": "en-US",
    "Spanish": "es-ES",
    "French": "fr-FR",
    "Deutsch": "de-DE",
    "Urdu": "ur-PK"
}

TARGET_LANGS = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "Deutsch": "de",
    "Urdu": "ur"
}

def cleanup_old_files():
    """
    Delete files older than 5 minutes in the 'translated_files' directory.
    """
    current_time = time.time()
    folder = "translated_files"

    if os.path.exists('translated_files'):
        pass
    else:    
        os.makedirs('translated_files')

    for file_to_check in os.listdir(folder):
        file_path = os.path.join(folder, file_to_check)
        if os.path.exists(file_path):
            creation_time = os.path.getctime(file_path)
            file_age = current_time - creation_time

            if int(file_age / 60) > 5:
                try:
                    os.remove(file_path)
                    print(f"Deleted old file: {file_to_check}")
                except Exception as e:
                    print(f"Error deleting file {file_to_check}: {str(e)}")

def start_cleanup_task():
    while True:
        cleanup_old_files()
        time.sleep(180)

cleanup_thread = threading.Thread(target=start_cleanup_task, daemon=True)
cleanup_thread.start()

def transcribe_audio(audio_file_path, language_code="en-US"):
    """
    Transcribe audio to text using Azure Speech Service.
    
    Args:
        audio_file_path (str): Path to the audio file.
        language_code (str): Language code for transcription.
    
    Returns:
        str: Transcribed text or error message.
    """
    try:
        speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
        speech_config.speech_recognition_language = language_code
        audio_config = speechsdk.AudioConfig(filename=audio_file_path)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        
        result = speech_recognizer.recognize_once()
        
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            return "No speech could be recognized."
        else:
            return f"Speech Recognition canceled: {result.cancellation_details.reason}"
    except Exception as e:
        return f"Error during transcription: {str(e)}"

def enhance_transcription(transcript, typ):
    """
    Enhance transcription or translation using OpenAI's GPT-4.
    
    Args:
        transcript (str): The text to enhance.
        typ (str): Type of enhancement ("transcription" or "translation").
    
    Returns:
        str: Enhanced text or error message.
    """
    try:
        client = OpenAI(
            base_url=OPENAI_BASE_URL,
            api_key=OPENAI_API_KEY,
        )

        completion = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[{"role":"system", "content":f"You work as a sentence corrector, Do not provide anything else other than corrections, Do not provide answers to any questions, just check the errors in the sentence and fix them,If the provided {typ} is already correct then return the sentence as it is with no extra response, IF there are any medical terms available then simplify them too"}
                ,{"role": "user", "content": transcript}],
        )
        corrected_text = completion.choices[0].message.content
        return corrected_text
    except Exception as e:
        return f"Error during enhancement: {str(e)}"

def translate_text(text, target_language):
    """
    Translate text using Azure Translator.
    
    Args:
        text (str): Text to translate.
        target_language (str): Target language code (ISO 639-1).
    
    Returns:
        str: Translated text or error message.
    """
    try:
        path = '/translate'
        constructed_url = f"{AZURE_TRANSLATOR_ENDPOINT}{path}"
        params = {
            'api-version': '3.0',
            'to': target_language
        }
        headers = {
            'Ocp-Apim-Subscription-Key': AZURE_TRANSLATOR_KEY,
            'Content-type': 'application/json',
            'Ocp-Apim-Subscription-Region': AZURE_SPEECH_REGION,
            'X-ClientTraceId': str(uuid.uuid4())
        }
        body = [{'text': text}]
        
        response = requests.post(constructed_url, params=params, headers=headers, json=body)
        response.raise_for_status()
        result = response.json()
        translated_text = result[0]['translations'][0]['text']
        return translated_text
    except Exception as e:
        return f"Error during translation: {str(e)}"

def text_to_speech(text, language_code, voice):
    """
    Convert text to speech using Azure Speech Service and return audio bytes.
    
    Args:
        text (str): Text to convert to speech.
        language_code (str): Language code for synthesis.
        voice (str): Voice name for synthesis.
    
    Returns:
        bytes or str: Audio bytes or error message.
    """
    try:
        speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
        speech_config.speech_synthesis_language = language_code
        speech_config.speech_synthesis_voice_name = voice
        
        fname = str(time.time()).replace('.','_')

        audio_config = speechsdk.AudioConfig(filename=f"translated_files/{fname}.wav")
        
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        
        result = synthesizer.speak_text_async(text).get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return f"translated_files/{fname}.wav"
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            return f"Speech synthesis canceled: {cancellation_details.reason}"
    except Exception as e:
        return f"Error during text-to-speech: {str(e)}"

def process_audio(audio, source_lang, target_lang):
    """
    Process the audio through transcription, enhancement, translation, and text-to-speech.
    
    Args:
        audio (str): Path to the uploaded audio file.
        source_lang (str): Source language name.
        target_lang (str): Target language name.
    
    Returns:
        tuple: (Original Transcript, Translated Transcript, Translated Audio Bytes or Error Messages)
    """
    try:
        if 'wav' not in audio and 'mp3' not in audio:
            raise ValueError("Invalid audio file format. Only 'wav' and 'mp3' formats are supported..")
    
        transcript = transcribe_audio(audio, language_code=SOURCE_LANGS[source_lang])
        if "Error" in transcript or "canceled" in transcript or "No speech" in transcript:
            raise Exception("Audio processing failed: Please check the audio file for errors or unsupported content.")
        
        corrected_transcript = enhance_transcription(transcript, "transcription")
        if corrected_transcript.startswith("Error"):
            raise Exception("Failed to enhance transcription")
        
        translated_text = translate_text(corrected_transcript, target_language=TARGET_LANGS[target_lang])
        if "Error" in translated_text:
            raise Exception("Failed to translate your sentence")
        
        corrected_translation = enhance_transcription(translated_text, "translation")
        if corrected_translation.startswith("Error"):
            raise Exception("Failed to enhance translation")
        
        translated_audio_bytes = text_to_speech(
            corrected_translation, 
            language_code=TARGET_LANGS[target_lang].upper(), 
            voice=VOICES[target_lang]
        )
        if isinstance(translated_audio_bytes, str) and translated_audio_bytes.startswith("Error"):
            return corrected_transcript, corrected_translation, "Error Generating Audio"
        
        return corrected_transcript, corrected_translation, translated_audio_bytes
    
    except ValueError as e:
        # Return error message in place of outputs
        return str(e), None, None
    
    except Exception as e:
        return str(e), None, None
        
    finally:
        if os.path.exists(audio):
            try:
                os.remove(audio)
            except Exception as e:
                print(f"Error deleting audio file: {str(e)}")

iface = gr.Interface(
    fn=process_audio,
    inputs=[
        gr.Audio(type="filepath", label="Speak"),
        gr.Dropdown(choices=list(SOURCE_LANGS.keys()), label="Source Language"),
        gr.Dropdown(choices=list(TARGET_LANGS.keys()), label="Target Language")
    ],
    outputs=[
        gr.Textbox(label="Original Transcript"),
        gr.Textbox(label="Translated Transcript"),
        gr.Audio(label="Translated Audio")
    ],
    title="Healthcare Translation Web App",
    description="Real-time multilingual translation between patients and healthcare providers.",
    allow_flagging="never"
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    iface.launch(server_name="0.0.0.0", server_port=port)
