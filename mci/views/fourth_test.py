from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3

bp = Blueprint('fourth', __name__, url_prefix='/')

# 4th test
import random

@bp.route('/find_diff')
def find_diff():
    return render_template('4th_test.html')

#global 변수
wrong_image_count = 0
test_class = ['나비','지렁이','컴퓨터']
# 밑에 next를 안 넣고 count>=3 을 하면 오류남 (인덱스 에러)/ 왜인진 모르겠지만 맨 마지막 인덱스는 안 나온다.-># 해결 
wrong_ox = list() #db 저장용 
# html 렌더링
@bp.route('/wrong_img',  methods=['POST','GET'])
def wrong_img():
    # OX list에 결과값 저장
    global wrong_ox
    if request.method == 'POST':
        image = str(request.form['button'])
        if 'X' in image:
            wrong_ox.append(1)
        else: wrong_ox.append(0)
    # 이미지 불러오기
    global wrong_image_count
    global test_class
    if len(test_class) == 0:
        test_class.append('나비')
        test_class.append('지렁이')
        test_class.append('컴퓨터')
    if wrong_image_count >=3 :
        wrong_image_count = 0 # 전역변수 횟수 0으로 바꿔주기
        return redirect(url_for('fourth.end')) # redirect를 할때는 route 옆에 오는 글자를 넣어줘야함(함수이름이 아님) 
    
    else:
        # 변수에 이미지 이름 넣기
        random.shuffle(test_class)
        img1 =test_class[0] + '1'
        img2=test_class[0] + '2'
        img3= test_class[0] + '3'
        img4= test_class[0] + 'X'
        # 랜덤으로 텍스트 보내기
        random_class =[img1,img2,img3,img4 ]
        random.shuffle(random_class)
        img1 = random_class[0]
        img2 = random_class[1]
        img3 = random_class[2]
        img4 = random_class[3]
        
        # 처음엔 for문으로 작성하려고 했으나 렌더링 될 때는 마지막 것만 되기 때문에 필요가 없음    
        # for i in test_class :   
        #     # str = test_class[i]    
        #     random_list = [i+'1', i+'2',i+'3',i+'X']
        #     random_list_2 = []
        #     random.shuffle(random_list)
        #     for  j in random_list:
        #         random_list_2.append(j)
        #     img1 = random_list_2[0]
        #     img2 = random_list_2[1]
        #     img3 = random_list_2[2]
        #     img4 = random_list_2[3]
            
        # 누른 버튼의 text 를 받아서 정답인지 오답인지 판별하기
        
        test_class.remove(test_class[0]) #  사용한 str 은 삭제해서 test_class 가 중복이 안되게 함.
        wrong_image_count += 1
        return render_template('4th_test.html',img1 = img1, img2=img2,img3=img3,img4=img4) 
   

@bp.route('/end',  methods=['POST','GET'])
def end():
    # DB 저장 
    conn = sqlite3.connect('ijm.db', isolation_level=None)
    # 커서
    cursor = conn.cursor()
    # 테이블 생성(데이터 타입 = TEST, NUMERIC, INTEGER, REAL, BLOB(image) 등)
    # 필드명(ex. name) -> 데이터 타입(ex. text) 순서로 입력 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Wrong_Image (
        session TEXT PRIMARY KEY NOT NULL,
        game text,
        OX1 integer,
        OX2 integer,
        OX3 integer)""")
    
    # db 에 정보 저장
    game = 'Wrong_Image'
    OX1 = wrong_ox[0]
    OX2 = wrong_ox[1]
    OX3 = wrong_ox[2]
    guest = str(session['guest'])
    
    cursor.execute("""
        INSERT INTO Wrong_Image (session, game, OX1,OX2,OX3) VALUES (?,?,?,?,?)          
        """, (guest, game, OX1,OX2,OX3)
        )
    conn.commit()
    cursor.close()
    conn.close() 
    return render_template('5th_test.html')