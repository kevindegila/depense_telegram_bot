from telegram.ext import Updater, MessageHandler, Filters
import os
from google.cloud import speech
from dotenv import load_dotenv
from chatgpt import structured_data, text_to_sql, reformule_answer
from sql_utils import save_to_sql, execute_query


load_dotenv()
speech_key = os.getenv("SPEECH_KEY")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = speech_key

# Cette fonction sera appelée chaque fois qu'un message vocal est reçu
def save_voice(update, context):
    voice = update.message.voice  # Récupère le message vocal
    file_id = voice.file_id
    file = context.bot.get_file(file_id)
    filepath = f"voice_messages/{file_id}.ogg"
    file.download(filepath)  # Sauvegarde le message vocal dans un dossier
    # transcription
    transcript = transcribe_voice(filepath)
    update.message.reply_text(f"Vous avez dit : {transcript}")

    gpt_answer = structured_data(transcript)
    update.message.reply_text(gpt_answer)

    save_to_sql(gpt_answer)
    update.message.reply_text("Entrée Sauvegardée")


def transcribe_voice(file_path):
    client = speech.SpeechClient()

    # Charge le fichier vocal
    with open(file_path, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
        sample_rate_hertz=48000,
        enable_automatic_punctuation=True,
        audio_channel_count=1,
        language_code="fr-FR",  # Changez ceci en fonction de la langue du fichier vocal
        model='phone_call'
    )

    # Envoie la requête pour la transcription
    response = client.recognize(config=config, audio=audio)

    # Récupère les résultats de la transcription
    results = ""
    for result in response.results:
        results += result.alternatives[0].transcript
        
    return results

def get_spending_analytics(update, context):
    user_id = update.message.from_user.id
    text = update.message.text

    sql_query = text_to_sql(text)
    sql_answer = execute_query(sql_query)
    answer = reformule_answer(text, sql_answer)
    update.message.reply_text(answer)


def main():
    # Mettez votre token du bot Telegram
    TOKEN = "6556334256:AAHrsl_zwHq_Ja12zb-eLhfvur9x1uLEdB8"
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Crée un gestionnaire pour les messages vocaux
    dp.add_handler(MessageHandler(Filters.voice, save_voice))
    dp.add_handler(MessageHandler(Filters.text, get_spending_analytics))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    # Crée un dossier pour les messages vocaux s'il n'existe pas déjà
    if not os.path.exists("voice_messages"):
        os.makedirs("voice_messages")
    main()
