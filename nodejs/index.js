const fs = require('fs');
const grpc = require('grpc');
const protoLoader = require('@grpc/proto-loader');
const wav = require('wav');

const username = process.env.SBERSPEECH_USERNAME;
const password = process.env.SBERSPEECH_PASSWORD;

var file = fs.createReadStream(process.argv[2]);
var reader = new wav.Reader();

const request = {
    options: {
        audio_encoding: 1, // PCM_S16LE
        sample_rate: 16000,
        language: 'ru-RU',
        hypotheses_count: 1,
        enable_profanity_filter: true,
        enable_multi_utterance: false,
        enable_partial_results: true,
        model: 'general'
    }
};
