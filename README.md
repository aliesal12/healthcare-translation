# Healthcare Translation Web App with Generative AI

## Table of Contents
- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Setup and Installation](#setup-and-installation)
- [Code Structure](#code-structure)
- [Detailed Function Documentation](#detailed-function-documentation)
- [Environment Variables](#environment-variables)
- [Voice and Language Configuration](#voice-and-language-configuration)
- [Cleanup Mechanism](#cleanup-mechanism)
- [Transcription](#transcription)
- [Enhancement](#enhancement)
- [Translation](#translation)
- [Text-to-Speech](#text-to-speech)
- [Audio Processing Pipeline](#audio-processing-pipeline)
- [Gradio Interface](#gradio-interface)
- [FastAPI Integration](#fastapi-integration)
- [Deployment](#deployment)
- [Security and Data Privacy](#security-and-data-privacy)
- [Dependencies](#dependencies)
- [Testing and Quality Assurance](#testing-and-quality-assurance)
- [Security and Privacy](#security-and-privacy)
- [Conclusion](#conclusion)

## Project Overview
The Healthcare Translation Web App with Generative AI is a web-based prototype designed to facilitate real-time, multilingual communication between patients and healthcare providers. Leveraging advanced AI technologies, the application converts spoken input into text, provides live transcripts, translates the text into the desired language, and offers audio playback of the translated text. This ensures effective communication across language barriers in healthcare settings, enhancing patient care and provider efficiency.

## Architecture
The application is built using a combination of Python-based frameworks and services:
- **FastAPI**: Serves as the backend framework to handle API requests.
- **Gradio**: Provides an interactive user interface for users to interact with the application.
- **Azure Cognitive Services**: Utilized for speech recognition and text-to-speech functionalities.
- **OpenAI API**: Employed for enhancing transcription accuracy and simplifying medical terms.
- **Render.com**: Platform used for deploying the web application.

## Setup and Installation

### Clone the Repository
```bash
git clone https://github.com/aliesal12/healthcare-translation.git
cd healthcare-translation
```
### Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```
### Install Dependencies
```bash
pip install -r requirements.txt
```
### Configure Environment Variables
Create a .env file in the root directory and add the following variables:
```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=your_openai_base_url
AZURE_SPEECH_KEY=your_azure_speech_key
AZURE_SPEECH_REGION=your_azure_speech_region
AZURE_TRANSLATOR_KEY=your_azure_translator_key
AZURE_TRANSLATOR_ENDPOINT=your_azure_translator_endpoint
PORT=8000
```
### Run the Application Locally
```bash
uvicorn app:app --host localhost --port 8000
```
The application will be accessible at http://localhost:8000/.

## Code Structure
```bash
healthcare-translation-app/
├── app.py
├── requirements.txt
├── .env
├── translated_files/
├── README.md
└── ... (other files and directories)
```
- app.py: Main application script containing the backend logic and API endpoints.
- requirements.txt: Lists all Python dependencies required for the project.
- .env: Stores environment variables (not included in version control).
- translated_files/: Directory to store temporary translated audio files.
- README.md: Project documentation and setup instructions.

## Detailed Function Documentation

### Environment Variables
- **OPENAI_API_KEY**: API key for accessing OpenAI services.
- **OPENAI_BASE_URL**: Base URL for OpenAI API requests.
- **AZURE_SPEECH_KEY**: API key for Azure Speech Services.
- **AZURE_SPEECH_REGION**: Azure region for Speech Services.
- **AZURE_TRANSLATOR_KEY**: API key for Azure Translator.
- **AZURE_TRANSLATOR_ENDPOINT**: Endpoint URL for Azure Translator.
- **PORT**: Port number for deploying the application (default: 8000).

### Voice and Language Configuration
```python
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
```
- VOICES: Maps each language to its respective Azure Neural Voice for text-to-speech.
- SOURCE_LANGS: Maps each language to its Azure language code for transcription.
- TARGET_LANGS: Maps each language to its ISO 639-1 code for translation.

### Cleanup Mechanism
Ensures that temporary audio files are deleted after 5 minutes to maintain storage hygiene.
```python
def cleanup_old_files():
    # Deletes files older than 5 minutes in 'translated_files' directory
    pass

def start_cleanup_task():
    # Initiates a background thread to periodically clean up old files every 3 minutes.
    pass

```
### Transcription
Converts spoken audio input into text using Azure Speech Services.
```python
def transcribe_audio(audio_file_path, language_code="en-US"):
    # Transcribes audio to text
    pass
```
Parameters:
- audio_file_path: Path to the audio file.
- language_code: Language code for transcription.
Returns: Transcribed text or an error message.

### Enhancement
Enhances the transcription or translation accuracy using OpenAI's GPT-4 model.
```python
def enhance_transcription(transcript, typ):
    # Enhances transcription or translation using GPT-4
    pass
```
Parameters:
- transcript: The text to enhance.
- typ: Type of enhancement ("transcription" or "translation").
Returns: Enhanced text or an error message.

### Translation
Translates the enhanced text into the target language using Azure Translator.
```python
def translate_text(text, target_language):
    # Translates text using Azure Translator
    pass
```
Parameters:
- text: Text to translate.
- target_language: Target language code (ISO 639-1).
Returns: Translated text or an error message.

### Text-to-Speech
Converts the translated text into speech using Azure Speech Services.
```python
def text_to_speech(text, language_code, voice):
    # Converts text to speech and returns the audio file path
    pass
```
Parameters:
- text: Text to convert.
- language_code: Language code for synthesis.
- voice: Voice name for synthesis.
Returns: Path to the synthesized audio file or an error message.

### Audio Processing Pipeline
Handles the end-to-end processing of the uploaded audio file.
```python
def process_audio(audio, source_lang, target_lang):
    # Processes audio: transcription, enhancement, translation, and text-to-speech
    pass
```
Parameters:
- audio: Path to the uploaded audio file.
- source_lang: Source language selected by the user.
- target_lang: Target language selected by the user.
Returns: Tuple containing the original transcript, translated transcript, and translated audio file path or error messages.

### Gradio Interface
Creates an interactive web interface for users to interact with the application.
```python
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
```
Inputs:
- Speak: Audio input for transcription.
- Source Language: Dropdown to select the source language.
- Target Language: Dropdown to select the target language.
Outputs:
- Original Transcript: Displays the transcribed text.
- Translated Transcript: Displays the translated text.
- Translated Audio: Provides audio playback of the translated text.

### FastAPI Integration
Integrates Gradio with FastAPI for deployment.
```python
from fastapi import FastAPI
import gradio as gr

app = FastAPI()
app = gr.mount_gradio_app(app, iface, path="/")
```
Deployment: The application is served using Uvicorn on the specified port.

## Deployment

The application is deployed on Render.com, providing a live link accessible to users. Deployment steps include:

### Push Code to GitHub
- **Ensure the latest code is pushed to the GitHub repository.**

### Connect Repository to Render.com
1. **Log in to Render.com.**
2. **Create a new Web Service.**
3. **Connect your GitHub repository.**

### Configure Build and Run Commands
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python app.py`

### Set Environment Variables
- **Add all necessary environment variables in the Render.com dashboard under the service's settings.**

### Deploy
- **Render.com will handle the deployment process, providing a live URL upon successful deployment.**

## Security and Data Privacy

Given the sensitive nature of healthcare data, the application incorporates basic security measures to ensure patient confidentiality:

- **Environment Variables:** Sensitive API keys and configurations are stored securely using environment variables, preventing exposure in the codebase.
- **Temporary File Storage:** Translated audio files are stored temporarily and deleted after 5 minutes to minimize data retention.
- **HTTPS Deployment:** Ensure the deployment platform (Render.com) uses HTTPS to encrypt data in transit.
- **Input Validation:** The application validates audio file formats and handles errors gracefully to prevent malicious inputs.

## Dependencies

The application relies on several Python libraries and external services:

### Python Libraries:
- **os:** Interacts with the operating system.
- **uuid:** Generates unique identifiers.
- **requests:** Handles HTTP requests.
- **gradio:** Creates interactive web interfaces.
- **openai:** Interfaces with OpenAI's API.
- **azure.cognitiveservices.speech:** Interfaces with Azure Speech Services.
- **tempfile:** Manages temporary files.
- **dotenv:** Loads environment variables from `.env`.
- **time & threading:** Manages timing and concurrency.
- **fastapi:** Builds the backend API.
- **uvicorn:** Serves the FastAPI application.

### External Services:
- **OpenAI API:** Enhances transcription and translation accuracy.
- **Azure Speech Services:** Provides speech-to-text and text-to-speech functionalities.
- **Azure Translator:** Facilitates text translation between languages.
- **Render.com:** Hosts and deploys the web application.

**Ensure all dependencies are listed in the `requirements.txt` file for seamless installation.**

## Testing and Quality Assurance

To ensure the application functions as intended, the following testing and QA measures are implemented:

- **Unit Testing:** Test individual functions like `transcribe_audio`, `enhance_transcription`, `translate_text`, and `text_to_speech` to verify their correctness.
- **Integration Testing:** Validate the end-to-end audio processing pipeline to ensure seamless interaction between transcription, enhancement, translation, and synthesis.
- **Error Handling:** Implement robust error handling to manage failures in transcription, translation, or audio synthesis gracefully.
- **User Interface Testing:** Ensure the Gradio interface is responsive and functions correctly across different devices and screen sizes.
- **Performance Testing:** Assess the application's responsiveness and processing speed, especially under concurrent usage scenarios.
- **Security Testing:** Verify that sensitive data is protected and that the application is resilient against common security threats.

## Security and Privacy

- **Data is processed securely with no storage of sensitive information.**
- **User interactions remain confidential, adhering to data privacy standards.**

## Conclusion

The Healthcare Translation Web App with Generative AI serves as a robust solution to bridge language barriers in healthcare settings. By integrating cutting-edge AI technologies for transcription, translation, and synthesis, the application ensures effective and accurate communication between patients and healthcare providers. The project's rapid development within a 48-hour timeframe showcases technical proficiency, effective use of generative AI tools, and a focus on quality and user experience. Future enhancements will further solidify its position as a valuable tool in the healthcare industry.
