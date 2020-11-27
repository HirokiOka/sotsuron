#環境変数:export GOOGLE_APPLICATION_CREDENTIALS="/Users/Hiroki/Downloads/cloud vision sample-2a137975417a.json"
import cv2
import io
import socket
import wikipedia
import time
import os
from google.cloud import vision
from google.cloud.vision import types
from natto import MeCab

port1 = 10001
port2 = 10002
port3 = 10003

host = "192.168.100.108"
img = "photo.jpg"

wikipedia.set_lang("ja")

client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client1.connect((host, port1))
client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client2.connect((host, port2))
client3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client3.connect((host, port3))

book_tracker = cv2.TrackerKCF_create()
cap = cv2.VideoCapture(0) #デバイスの指定(0:PCwebカメラ，1:USB接続webカメラ)
size = (800, 600)
client = vision.ImageAnnotatorClient()


#テキストを画像ファイルから検出し，text_annotationsを返す
def detect_text(path):

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    return texts


#text_annotationsから名詞を抽出し，配列に格納して返す
def noun_extraction(text_annotations):
    words = []
    with MeCab('-F%m,%f[0],%h') as nm:
        try:
            for n in nm.parse(texts[0].description, as_nodes=True):
                node = n.feature.split(',');
                if len(node) != 3:
                    continue
                if node[1] == '名詞' and len(node[0]) > 1:
                    words.append(node[0])
        except IndexError:
            print("IndexError from noun_extraction")
    return words


#文字領域を追跡
def calibration():
    cv2.destroyAllWindows()
    while True:
        time.sleep(2)
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.resize(frame, size)

        bbox2 = (0,0,10,10)
        bbox2 = cv2.selectROI(frame, False)
        ok2 = book_tracker.init(frame, bbox2)

        cv2.destroyAllWindows()
        break


calibration()
while True:

    ret, frame = cap.read()
    frame = cv2.resize(frame, size)
    if not ret:
        k = cv2.waitKey(1)
        if k == 27 :
            break
        continue
    timer = cv2.getTickCount()

    # トラッカーをアップデートする
    book_track, bbox2 = book_tracker.update(frame)

    if book_track:
        # Tracking success
        p3 = (int(bbox2[0]), int(bbox2[1]))
        p4 = (int(bbox2[0] + bbox2[2]), int(bbox2[1] + bbox2[3]))
        cv2.rectangle(frame, p3, p4, (0,255,0), 2, 1)
        tx = (p3[0] - 130) * 1.8
        ty = (p3[1] - 130) * 1.8

        coordinate = str(tx) + '\n' + str(ty)
        client1.send(coordinate.encode('utf-8'))

    cv2.imshow("Tracking", frame)

    k = cv2.waitKey(1)

    if k == ord('s'):
        cv2.imwrite(img, frame)  #画像を保存
        texts = detect_text(img)
        words = noun_extraction(texts)
        i = 0
        nouns = ""
        for word in words:
            i += 1
            nouns += "["  + word + "] " + '\n'
        if(words == None):
            client2.send("None".encode('utf-8'))
        else:
            client2.send(nouns.encode('utf-8'))
            while True:
                mode = 1
                if(mode == 1):  #wikipediaモード
                #変数indexに選択した名詞のインデックスを入れる
                    server2_data = client2.recv(4096)
                    index = int(server2_data.decode('utf-8'))
                    print(index)

                    try:
                        result = wikipedia.summary(words[index], sentences=1)
                        message = words[index] + "\n" + result
                        client3.send(message.encode('utf-8'))
                        break
                    except wikipedia.exceptions.DisambiguationError as error:
                        title = "曖昧さ回避:" + error.args[1][0]
                        result =  wikipedia.summary(error.args[1][0], sentences=1)
                        message = title + "\n" + result
                        client3.send(message.encode('utf-8'))
                        break
                    except wikipedia.exceptions.PageError:
                        message = "ページが存在しません．"
                        client3.send(message.encode('utf-8'))
                        break

    if k == ord('c'):
        calibration()

    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
