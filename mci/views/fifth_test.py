from flask import Blueprint, render_template, session

bp = Blueprint('fifth', __name__, url_prefix='/')

# 5th test
import os, pyscreenshot
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
import easyocr
import sqlite3

@bp.route('/pygame')
def pygame():
    return render_template('5th_test.html')

@bp.route('/get_screenshot', methods=['POST'])
def get_screenshot():
    
    # 기억력 게임 점수에 대한 함수 정의 
    def get_score(level) :
        if level == 1:
            score = 0
        elif level == 2:
            score = 1
        elif 3 <= level <= 4:
            score = 2
        elif level == 5:
            score = 3
        else:
            score = 4
            
        return level, score

    # 기억력 게임을 완료한 이후 easyocr을 이용해 게임결과 이미지에서 텍스트추출
    guest = str(session['guest'])
    im = pyscreenshot.grab()
    file_name = 'drawing/pygame/{}.png'.format(guest)
    im.save(file_name)
    reader = easyocr.Reader(['ko', 'en'])
    game = 'Memory_Test'
    
    with open(file_name,'rb') as pf:
        img = pf.read()
        result = reader.readtext(img)
        for res in result:
            if res[1][0:10] == 'Your level':
                level = res[1][-1]
                result = get_score(int(level))
            else:
                level=1
                result=0
    
    # 텍스트로 추출한 결과를 DB에 저장
    conn = sqlite3.connect('ijm.db', isolation_level=None)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Memory_Test (session TEXT PRIMARY KEY NOT NULL,
        game TEXT,
        level integer,
        score integer)""")
    cursor.execute("""INSERT INTO Memory_Test(session, game, level, score) 
                    VALUES(?, ?, ?, ?)""", (guest, game, level, result))
    conn.commit()
    cursor.close()
    os.remove(file_name)