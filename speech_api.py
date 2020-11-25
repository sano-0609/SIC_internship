#coding:utf8
import sys
import json
import httplib2
from googleapiclient import discovery
from mutagen.flac import FLAC
from pydub import AudioSegment
import magic
import requests
import time

key = 'AIzaSyAZP7a8ed57dQnZ8s8OqIAQw_3jGsACLRY'

filename = sys.argv[1]
bucketname = 'speech_to'

#GCSから音声データダウンロード
uri = 'https://storage.googleapis.com/' + bucketname + '/' + filename
r = requests.get(uri)
#ダウンロード結果チェック
if r.status_code != 200:
    print('Request to {0} returned {1} error.'.format(uri,r.status_code))
    sys.exit()

#ダウンロードした音声データからencoding、rate、lengthの情報を取得
mime = magic.Magic(mime=True).from_buffer(r.content)
if mime == 'audio/x-wav' and '.wav' in filename.lower():
    encoding = 'LINEAR16'
    sound = AudioSegment(r.content)
    if sound.channels != 1:
        print('Must use single channel (mono) audio')
        sys.exit()
    rate = sound.frame_rate
    length = sound.duration_seconds
elif mime == 'audio/x-flac' and '.flac' in filename.lower():
    encoding = 'FLAC'
    filepath = '/tmp/' + filename
    with open(filepath, 'wb') as f:
        f.write(r.content)
        f.close()
    sound = FLAC(filepath).info
    if sound.channels != 1:
        print('Must use single channel (mono) audio')
        sys.exit()
    rate = sound.sample_rate
    length = sound.length
else:
    print('Acceptable type is only "wav" or "flac".')
    sys.exit()

print('\n-*- audio info -*-')
print('filename   : ' + filename)
print('mimetype   : ' + mime)
print('sampleRate : ' + str(rate))
print('playtime   : ' + str(length) + 's')

#リクエスト作成準備
service = discovery.build(
    'speech',
    'v1',
    http=httplib2.Http(),
    discoveryServiceUrl='https://{api}.googleapis.com/$discovery/rest?version={apiVersion}',
    developerKey=key,
    cache_discovery=False
)

#リクエストボディ定義
body={
    'config': {
        'encoding': encoding,
        'sampleRateHertz': rate,
        'languageCode': 'ja-JP'
    },
    'audio': {
        'uri': 'gs://' + bucketname + '/' + filename
    }
}

if length < 60:
#再生時間が1分未満の場合
    #サービスリクエスト作成
    service_request = service.speech().recognize(body=body)
    #サービスリクエスト実行、実行結果パース
    results = (service_request.execute())["results"]
else:
#再生時間が1分以上の場合
    #サービスリクエスト作成
    service_request = service.speech().longrunningrecognize(body=body)
    #サービスリクエスト実行、オペレーション名パース
    operation_name = (service_request.execute())['name']
    #オペレーションエンドポイント定義
    endpointUri = 'https://speech.googleapis.com/v1/operations/' + operation_name + '?key=' + key
    #長時間実行オペレーション開始（この時点ではまだ音声認識結果は含まれていない）
    content_res = requests.get(endpointUri)
    results = 'Transcribing...'
    print('\n' + results)
    while results == 'Transcribing...':
        time.sleep(10)
        #10秒後にオペレーション結果取得
        content_res = requests.get(endpointUri)
        try:
            #オペレーション結果に音声認識結果が含まれていればパース
            results = (content_res.json())['response']['results']
        except:
            #含まれていなければリトライ
            print(results)

print('\n-*- transcribe result -*-')

#結果をコンソール出力
for index, item in enumerate(results):
    print('[%d]Transcript >>>' % (index + 1), item["alternatives"][0]["transcript"])
    print('[%d]Confidence >>>' % (index + 1), item["alternatives"][0]["confidence"])