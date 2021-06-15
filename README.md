# Samples for SberSpeech ASR&TTS
## ASR
In asr directory

**NodeJS** (not working):  
cd asr/nodejs
npm install  
export SBERSPEECH_USERNAME=<username>  
export SBERSPEECH_PASSWORD=<password>  
node index.js ../sounds/pepsi16kHz.wav  
  
**Python** (working now):  
cd asr/python  
python3 main.py --username USERNAME --password PASSWORD --file ../sounds/pepsi16kHz.wav  
  
Expected result:  
Got partial result:  
 Hyp #1: Я бы  
Got partial result:  
 Hyp #1: Я бы хотел  
Got partial result:  
 Hyp #1: Я бы хотел большую пепу  
Got partial result:  
 Hyp #1: Я бы хотел большую пепси  
Got partial result:  
 Hyp #1: Я бы хотел большую пепси и 1  
Got partial result:  
 Hyp #1: Я бы хотел большую пепси и 1 пиццу  
Got partial result:  
 Hyp #1: Я бы хотел большую пепси и 1 пиццу с грибами  
Got partial result:  
 Hyp #1: Я бы хотел большую пепси и 1 пиццу с грибами  
Got end-of-utterance result:  
 Hyp #1: Я бы хотел большую пепси и 1 пиццу с грибами  
Recognition has finished  
  
## TTS  
In tts directory  
  
**Python**  
**Text sample**  
cd tts/text/python  
python3 main.py --username USERNAME --password PASSWORD --voice Bys --text 'Примерный текст для озвучки'  

Expected result:  
saved to ca76fbbc-4bb2-48d0-8b48-8fede444879d.wav  

**SSML sample**  
cd tts/ssml/python  
python3 main.py --username <username> --password <password> --voice Bys --ssml example.ssml  

Expected result:  
saved to ca76fbbc-4bb2-48d0-8b48-8fede444879d.wav  
