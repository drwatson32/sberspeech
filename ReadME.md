NodeJS (not working now):
cd nodejs
npm install
export SBERSPEECH_USERNAME=<username>
export SBERSPEECH_PASSWORD=<password>
node index.js ../sounds/pepsi16kHz.wav

Python Example (working now):
cd python
python3 main.py --username <username> --password <password> --file ../sounds/pepsi16kHz.wav

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


