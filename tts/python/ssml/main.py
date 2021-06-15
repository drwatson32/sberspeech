#!/usr/bin/env python3
import uuid
import argparse
from itertools import chain
import requests
import json
import shutil

def run(host, jwt, voice, ssml):
    local_filename = f'{uuid.uuid4()}.wav'
    file = open(f'{ssml}', 'rb')
    data = file.read()
     
    with requests.post('https://smartspeech.sber.ru/rest/v1/text:synthesize', 
                       params={'format':'wav16', 'voice': f'{voice}_24000'},
                       data=data,
                       headers={
                           'Authorization':f'Bearer {jwt}',
                           'Content-Type':'application/ssml'
                       },
                       stream=True) as r:

        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    print(f'saved to {local_filename}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', required=True, help='SberSpeech username')
    parser.add_argument('--password', required=True, help='SberSpeech password')
    parser.add_argument('--voice', required=True, help='Voice for TTS (May, Tur or Bys)')
    parser.add_argument('--ssml', required=True, help='SSML file for TTS')
    args = parser.parse_args()
    
    jwtrsp = requests.post('https://smartspeech.sber.ru/v1/token', data={}, auth=(args.username, args.password))
    jwt = jwtrsp.json()['tok']

    run('smartspeech.sber.ru', jwt, args.voice, args.ssml)
