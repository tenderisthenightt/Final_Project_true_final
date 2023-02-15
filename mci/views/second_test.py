from flask import Blueprint, render_template, request, session, redirect, g
import sqlite3
from random import choice
bp = Blueprint('second', __name__, url_prefix='/')

def s_quiz(stroop, dic):
        key = choice(stroop)
        stroop.remove(key)
        h_path = dic[key][0]
        answer = dic[key][1]
        return key, h_path, answer, stroop


# s_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']   
# s_answer = ''
# OX = []
# s_count = 0
# key = ''


dic = {'01':['/static/2/img/001.png', '빨강'], '02':['/static/2/img/002.png', '파랑'], '03':['/static/2/img/003.png', '노랑'],
    '04':['/static/2/img/004.png', '빨강'], '05':['/static/2/img/005.png', '파랑'], '06':['/static/2/img/006.png', '검정'],
    '07':['/static/2/img/007.png', '노랑'], '08':['/static/2/img/008.png', '빨강'], '09':['/static/2/img/009.png', '파랑'],
    '10':['/static/2/img/010.png', '검정']}



# @bp.before_request
# def before_second():
#     print('hi')
#     g.s_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
#     g.s_answer = ''
#     g.OX = []
#     g.s_count = 0
#     g.key = ''
@bp.route('/stroop', methods=['GET', 'POST']) ## 여기에 들어가야하는거 넣어주세요~!!!1 지영
def stroop():
    count = session['s_count']
    OX = session['OX']
    s_list = session['s_list']
    key = session['key']
    print(count)
    if count != len(OX): #해당 페이지에서 새로고침만 계속하면 문제가 고갈되기에 추가할 조건문
        if len(OX)>0:
            s_list.append(key)
        else:
            s_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
        count = len(OX)
    count += 1
    print(s_list)
    global dic
    session['key'], h_path, answer, s_list = s_quiz(s_list, dic)
    print(len(s_list))
    print(h_path)
    print(answer)
    session['s_answer']= answer
    print(len(OX))
    session['s_count'] = count
    return render_template('2nd_test.html', h_path = h_path)



@bp.route("/save",methods=['POST']) #flask 웹 페이지 경로
def save(): # 경로에서 실행될 기능 선언
    
    OX = session['OX']
    print(type(OX))
    print(OX)
    ans = str(request.form['answer'])
    # s_answer = session['s_answer']
    if ans == session['s_answer']:
        OX.append(1)
    else:
        OX.append(0)
    session['OX'] = OX
    # # 확인용
    # check = request.form['check']
    # print(check)
    if len(OX) >= 10:
    # DB 생성 / 이미 있으면 나중에 주석처리하기.
    # isolation_level = None (auto commit)
        conn = sqlite3.connect('ijm.db', isolation_level=None)
        # 커서
        cursor = conn.cursor()
        # 테이블 생성(데이터 타입 = TEST, NUMERIC, INTEGER, REAL, BLOB(image) 등)
        # 필드명(ex. name) -> 데이터 타입(ex. text) 순서로 입력 
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Stroop (
            session TEXT PRIMARY KEY NOT NULL,
            game text,
            OX1 integer,
            OX2 integer,
            OX3 integer,
            OX4 integer,
            OX5 integer,
            OX6 integer,
            OX7 integer,
            OX8 integer,
            OX9 integer,
            OX10 integer)""")
    
    # db 에 정보 저장
        game = 'Stroop'
        guest = str(session['guest'])
        print('111111111')
        cursor.execute("""
            INSERT INTO Stroop (session, game, OX1, OX2, OX3, OX4, OX5, OX6, OX7, OX8, OX9, OX10) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)          
            """, (guest, game, OX[0], OX[1], OX[2], OX[3], OX[4], OX[5], OX[6], OX[7], OX[8], OX[9])
            )

        print('222222222')

        conn.commit()
        cursor.close()
        conn.close()
        session['OX'] = []
        session['s_count'] = 0
        session['s_list'] = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
        return render_template('3rd_test.html')
    return redirect('/stroop')