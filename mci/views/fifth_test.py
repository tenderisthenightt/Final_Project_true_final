from flask import Blueprint, render_template, session, url_for, request, redirect
import random

bp = Blueprint('fifth', __name__, url_prefix='/')

# 5th test
import os, pyscreenshot
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
import easyocr
import sqlite3

# 기억력 게임 점수에 대한 함수 정의    
def get_score(level) :
    if level == 1:
            score = 0
    elif 2<= level <= 3:
            score = 3
    elif 4 <= level <= 5:
            score = 6
    elif 6 <= level <= 7:
            score = 8
    else:
            score = 10
    return level, score

@bp.route('/pygame')
def pygame():
    return render_template('5th_test.html')

@bp.route('/get_screenshot', methods=['POST'])
def get_screenshot():
    try:
        level = int(request.form['score'])
        result = get_score(int(level))
    except:
        level = random.choice([2, 3, 4, 5, 6, 7, 8])
        result = get_score(int(level))

    # 기억력 게임을 완료한 이후 easyocr을 이용해 게임결과 이미지에서 텍스트추출
    guest = str(session['guest'])
    
    print('good')
    
    # try:
    #     im = pyscreenshot.grab()
    #     file_name = 'drawing/pygame/{}.png'.format(guest)
    #     im.save(file_name)
    #     reader = easyocr.Reader(['ko', 'en'])
    # except:
    game = 'Memory_Test'
    
    # try:
    #     with open(file_name,'rb') as pf:
    #         img = pf.read()
    #         result = reader.readtext(img)
    #         for res in result:
    #             if res[1][0:10] == 'Your level':
    #                 level = res[1][-1]
    #                 result = get_score(int(level))
    # except:
    #     print('hi')

    # except:
    #     level = random.choice([2, 3, 4, 5, 6, 7, 8])
    #     result = get_score(int(level))
    print(level)
    print(result)
    # 텍스트로 추출한 결과를 DB에 저장
    conn = sqlite3.connect('ijm.db', isolation_level=None)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Memory_Test (session TEXT PRIMARY KEY NOT NULL,
        game TEXT,
        level integer,
        score integer)""")
    cursor.execute("""INSERT INTO Memory_Test(session, game, level, score) 
                    VALUES(?, ?, ?, ?)""", (guest, game, result[0], result[1]))
    conn.commit()
    cursor.close()
    try:
        os.remove(file_name)
    finally:
        return redirect(url_for('sixth.sound'))