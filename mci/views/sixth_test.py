from flask import Blueprint, render_template, request, jsonify, session, g
import sqlite3 as sql
from time import sleep
import urllib3
import json
import base64

bp = Blueprint('sixth', __name__, url_prefix='/')



# sound_target = '강아지가 방에 들어오면 고양이는 의자 밑에 숨는다' # 정답Text
# print(sound_target)

@bp.before_app_request
def before_sixth():
    g.sound_target = '강아지가 방에 들어오면 고양이는 의자 밑에 숨는다'
    g.DATABASE_URI = 'ijm.db'
@bp.route('/sound')
def sound():
    sound_target = g.sound_target
    return render_template('6th_test.html', target=sound_target)
@bp.route('/loading')
def roading():
    # 결과를 HTML 페이지에 삽입
    return render_template('6-2.html')

@bp.route('/STT', methods=['POST', 'GET'])
def STT():
    String_sound = ''  # 녹음파일 Text
    String_target = '' # 정답 Text
    sleep(5)
    count = 1
    
    #---------------------------------------------------------------------------
    #      STT Open API
    #---------------------------------------------------------------------------
    if request.method == 'POST':
        sound_target = g.sound_target
        openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
        accessKey = "f0f9fd15-daef-4655-b516-d7a9711c696a" 
        audioFilePath = request.files['recode'] # 다운로드한 음성파일을 여기에 넣어서 Text로 바꾸기

        # audioFilePath.save('녹음파일.wav')
        languageCode = "korean"
        #file = open('nefile', "rb")
        #audioContents= wavfile.read("녹음파일.wav") ## !!
        #print(audioContents)
        #audio_binary = tf.io.read_file(audioFilePath)
        # audioFile = request.files['recode']
        data = audioFilePath.read()
        audioContents = base64.b64encode(data).decode("utf8")
        # inMemoryFile = BytesIO(audioContents)


        #audioContents = base64.b64encode(file.read()).decode("utf8")
        # audioContents = base64.b64encode(inMemoryFile.getvalue()).decode("utf8")
        #file.close()
        
        requestJson = {    
            "argument": {
                "language_code": languageCode,
                "audio": audioContents
            }
        }
        
        http = urllib3.PoolManager()
        response = http.request(
        "POST",
            openApiURL,
            headers={"Content-Type": "application/json; charset=UTF-8","Authorization": accessKey},
            body=json.dumps(requestJson)
        )
        
        print("[responseCode] " + str(response.status))
        print("[responBody]")
        print("===== 결과 확인 ====")

        # 출력결과는 쓸때없는 내용이 들어가기 때문에 필요한 부분만 가져오기
        string = str(response.data,"utf-8")
        List = string.split('"')
        List = List[-2]
        List = List[:-1]
        print(List)
        # 녹음한 음성을 처리한 결과를 List변수에 담는다.
        
        
        # dic = {'1' : "안녕하세요. 오늘도 멋진 하루 되세요"}
        
        
        # NLP 유사도검사를 위해 정답Text와 녹음하고 Text로 바꾼 결과를 변수에 담에서 NLP모델에 넘긴다.
        # 녹음파일 Text
        String_sound = List
        
        # 정답Text
        String_target = sound_target
        
        
        
        #---------------------------------------------------------------------------
        #       유사도 검사 NLP Open API
        #---------------------------------------------------------------------------
        
        openApiURL = "http://aiopen.etri.re.kr:8000/ParaphraseQA"
        accessKey = "f0f9fd15-daef-4655-b516-d7a9711c696a"
        sentence1 = String_sound
        sentence2 = String_target
        
        requestJson = {
        "argument": {
            "sentence1": sentence1,
            "sentence2": sentence2
            }
        }
        
        http = urllib3.PoolManager()
        response = http.request(
            "POST",
            openApiURL,
            headers={"Content-Type": "application/json; charset=UTF-8","Authorization" :  accessKey},
            body=json.dumps(requestJson)
        )
        
        print("[responseCode] " + str(response.status))
        print("[responBody]")
        print(str(response.data,"utf-8"))

        NLP_String = str(response.data,"utf-8")
        NLP_List = NLP_String.split('"')
        print(NLP_List)
        
        NLP_reuslt = NLP_List[-2]
        # NLP_reuslt = NLP_target[:-1]
        print(NLP_reuslt)
        
        #--------------------------------------------------------------------------
        #     검증 결과 추출 및 전송
        #--------------------------------------------------------------------------
        
        String = ''
        Score = 0
        if NLP_reuslt == 'paraphrase' :
            String += 'O'
            Score = 1
        else:
            String += 'X'
            
        # os.remove(audioFilePath)
        print(sentence2)
        print(sentence1)
        print(String)
        
        conn = sql.connect(g.DATABASE_URI, isolation_level=None)
        cur = conn.cursor()
        cur.execute(
        """CREATE TABLE IF NOT EXISTS STT (session TEXT PRIMARY KEY NOT NULL,
        game TEXT,
        target TEXT,
        user_sound TEXT,
        ck TEXT,
        score integer)""")
        guest = str(session['guest'])
        game = 'STT'
        


        cur.execute("""
        INSERT INTO STT (session, game, target, user_sound, ck, score) VALUES (?,?,?,?,?,?)          
        """, (guest, game, sound_target, sentence1, String, Score)
        )
        
        conn.commit()
        cur.close()
        
        #-----------------------------------------------------------------------------
        
        # conn = sql.connect(DATABASE_URI, isolation_level=None)
        # cur = conn.cursor()
                
        # cur.execute("SELECT * FROM STT")
        # STT_Data = str(cur.fetchmany(size=1))
        # STT_Data = STT_Data.split("'")
        # cur.close()
        
        # stt_id = STT_Data[1]
        # stt_target = STT_Data[3]
        # stt_user_sound = STT_Data[5]
        # stt_ck = STT_Data[7]
        # stt_score = STT_Data[9]
        
        #                                             정답문장          TTS        체크 결과
    # return render_template('6th_test.html', target = sentence2, sound = sentence1, ck=String)
    return jsonify({'sound':sentence2})