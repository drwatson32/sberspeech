const fs = require('fs');
const https = require('https');
const grpc = require('grpc');
const protoLoader = require('@grpc/proto-loader');
const wav = require('wav');

const username = process.env.SBERSPEECH_USERNAME;
const password = process.env.SBERSPEECH_PASSWORD;

var audio = fs.createReadStream(process.argv[2]);
var reader = new wav.Reader();

const CHUNK_SIZE = 4000;
const FREQUENCY = 250;

const packageDefinition = protoLoader.loadSync('./proto/asr.proto', {
    includeDirs: ['node_modules/google-proto-files', './proto']
});
const packageObject = grpc.loadPackageDefinition(packageDefinition);
const serviceConstructor = packageObject.smartspeech.recognition.v1.SmartSpeech;

const recognitionOptions = {
  audio_encoding: packageObject.smartspeech.recognition.v1.RecognitionOptions.PCM_S16LE,
  sample_rate: 16000,
  language: 'ru-RU',
  hypotheses_count: 1,
  enable_profanity_filter: true,
  enable_partial_results: true,
  model: 'general'
};

var jwtRequestOptions = {
  host: 'smartspeech.sber.ru',
  port: 443,
  path: '/v1/token',
  method: 'POST',
  headers: {
    'Authorization': 'Basic ' + Buffer.from(username + ':' + password).toString('base64')
  }   
};

var jwtRequest = https.get(jwtRequestOptions, function(jwtResponse) {
  var jwtResponseBody = "";
  jwtResponse.on('data', function(jwtResponseData) {
      jwtResponseBody += jwtResponseData;
  });
  jwtResponse.on('end', function() {
    var jwt = JSON.parse(jwtResponseBody).tok;
    console.log(`Token: ${jwt}`);
    var serviceMetadata = new grpc.Metadata();
    serviceMetadata.add('authorization', `Bearer ${jwt}`);
    var grpcCredentials = grpc.credentials.createSsl(fs.readFileSync('./roots.pem'));
    var service = new serviceConstructor('smartspeech.sber.ru:443', grpcCredentials);
    var call = service['Recognize'](serviceMetadata);
    call.write({options: recognitionOptions});

    let i = 1;
    const interval = setInterval(() => {
      if (i * CHUNK_SIZE <= audio.length) {
        const chunk = new Uint16Array(audio.slice((i - 1) * CHUNK_SIZE, i * CHUNK_SIZE));
        const chunkBuffer = Buffer.from(chunk);
        call.write({audio_chunk: chunkBuffer});
        i++;
      } else {
        call.end();
        clearInterval(interval);
      }
    }, FREQUENCY);
    
    call.on('data', (response) => {
      console.log(response);
    });

    call.on('error', (response) => {
      console.log(response);
    });
  })
  jwtResponse.on('error', function(e) {
    console.log("Got error: " + e.message);
  });
});

