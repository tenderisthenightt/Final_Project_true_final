from flask import Blueprint, render_template, request, session
import sqlite3

bp = Blueprint('third', __name__, url_prefix='/')

# 3rd test
import torch
import sqlite3
import PIL

# 글그림 모델(yolov5)
#yolo_model = torch.hub.load('yolov5', 'custom', path = 'mci/module/best.pt', force_reload =False, source='local')

@bp.route('/text_to_img')
def text_to_img():
    return render_template('3rd_test.html')


@bp.route("/predict", methods=["GET", "POST"])
def predict():
    # 이미지 받기(blob)
    if request.method == 'POST':
        image = request.files["image"]
        # Save image_binary to a file or a variable
        guest = str(session['guest'])
        img_path = 'drawing/txt_to_img/' + guest + '.png'
        image.save(img_path)



    # with open("image.png", "wb") as f:
    #     f.write(image)
    
    
    # e=open('Base64_dec.png','wb') 
    # e.write(image_binary)
    # e.save(image_binary)
    # e.close()
    
    
    
    # Model(YOLOv5 종속 항목 설치)

    # Image
    img = PIL.Image.open(img_path)
    ########## 이 사진을 어떻게 가지고 올지에 대해서 알아봐야한다. !!
    yolo_model = torch.hub.load('yolov5', 'custom', path = 'mci/module/best.pt', force_reload =False, source='local')
    # 추론
    
    results = yolo_model(img)


    # 결과
    #results.print()
    #results.show()
    #results.save() # Save image to 'runs\detect\exp'
    #results.xyxy[0]  # 예측 (tensor)
    # results.pandas().xyxy[0]  # 예측 (pandas)
    conf = results.pandas().xyxy[0]
    print(conf)
    # 오답 여부
    OX = []
    try:
        if conf.name[0] == 'rabbit':
            OX.append(1)
        else:
            OX.append(0)
    except:
        OX.append(0)
    

    # DB 생성 / 이미 있으면 나중에 주석처리하기.
    # isolation_level = None (auto commit)
    conn = sqlite3.connect('ijm.db', isolation_level=None)
    # 커서
    cursor = conn.cursor()
    # 테이블 생성(데이터 타입 = TEST, NUMERIC, INTEGER, REAL, BLOB(image) 등)
    # 필드명(ex. name) -> 데이터 타입(ex. text) 순서로 입력 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Txt_to_Img (
        session TEXT PRIMARY KEY NOT NULL,
        game text,
        point float,
        OX integer)""")

    # db 에 정보 저장
    game = 'Txt_to_Img'
    point = float(conf.confidence)
    OX = OX[0]

    cursor.execute("""
        INSERT INTO Txt_to_Img (session, game, point, OX) VALUES (?,?,?,?)          
        """, (guest, game, point, OX)
        )

    conn.commit()
    cursor.close()
    conn.close()    
    return render_template('3rd_test.html')