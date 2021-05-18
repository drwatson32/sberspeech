#!/usr/bin/env python3
import argparse
from itertools import chain
import grpc
import requests
import json
import asr_pb2 as asr_pb2
import asr_pb2_grpc as asr_pb2_grpc

CHUNK_SIZE = 4000

def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))

def gen(model, hypotheses, sample_rate, path):
    audio_encoding = asr_pb2.RecognitionOptions.PCM_S16LE 
    options = asr_pb2.RecognitionOptions(
        audio_encoding=audio_encoding, 
        model=model,
        hypotheses_count=hypotheses,
        enable_profanity_filter=True,
        enable_partial_results=True,
        sample_rate=sample_rate)

    yield asr_pb2.RecognitionRequest(options=options)

    with open(audio_file_name, 'rb') as f:
        data = f.read(CHUNK_SIZE)
        while data != b'':
            yield asr_pb2.RecognitionRequest(audio_chunk=data)
            data = f.read(CHUNK_SIZE)

def run(host, jwt, model, hypotheses, sample_rate, path):
    ssl_cred = grpc.ssl_channel_credentials()
    token_cred = grpc.access_token_call_credentials(jwt)
    channel = grpc.secure_channel( host, grpc.composite_channel_credentials(ssl_cred, token_cred))
    stub = asr_pb2_grpc.SmartSpeechStub(channel)
    con = stub.Recognize(gen(model, hypotheses, sample_rate, path))
    try:
        for resp in con:
            if not resp.eou:
                print('Got partial result:')
            else:
                print('Got end-of-utterance result:')
            for i, hyp in enumerate(resp.result):
                print(' Hyp #{}: {}'.format(i + 1, hyp.normalized_text))
    except Exception as err:
        print('Error:', err)
    else:
        print('Recognition has finished')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', required=True, help='SberSpeech username')
    parser.add_argument('--password', required=True, help='SberSpeech password')
    parser.add_argument('--file', required=True, help='Path to pcm16 or opus audio file for recognition')
    parser.add_argument('--sample-rate', required=False, default=16000, type=int, help='Audio file sample_rate (pcm only)')
    parser.add_argument('--model', required=False, default='general', help='Recognition model name')
    parser.add_argument('--hypotheses', required=False, default=1, type=int, help='Recognition hypotheses count')
    args = parser.parse_args()
    
    jwtrsp = requests.post('https://smartspeech.sber.ru/v1/token', data={}, auth=(args.username, args.password))
    jwt = jwtrsp.json()['tok']

    run('https://smartspeech.sber.ru', jwt, args.model, args.hypotheses, args.sample_rate, args.file)
