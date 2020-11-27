import cv2
import time

if __name__ == '__main__':

    tracker = cv2.TrackerKCF_create()
    cap = cv2.VideoCapture(0)
    size = (800, 600)

    cv2.destroyAllWindows()
    while True:
        time.sleep(2)
        ret, frame = cap.read()
        frame = cv2.resize(frame, size)
        if not ret:
            continue
        bbox = (0,0,10,10)
        bbox = cv2.selectROI(frame, False)
        ok = tracker.init(frame, bbox)
        cv2.destroyAllWindows()
        break

    while True:
        # VideoCaptureから1フレーム読み込む
        ret, frame = cap.read()
        frame = cv2.resize(frame, size)
        if not ret:
            k = cv2.waitKey(1)
            if k == 27 :
                break
            continue

        # トラッカーをアップデートする
        track, bbox = tracker.update(frame)

        # 検出した場所に四角を書く
        if track:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (0,255,0), 2, 1)

        # 加工済の画像を表示する
        cv2.imshow("Tracking", frame)

        # キー入力を1ms待って、k が27（ESC）だったらBreakする
        k = cv2.waitKey(1)
        if k == 27 :
            break

# キャプチャをリリースして、ウィンドウをすべて閉じる
cap.release()
cv2.destroyAllWindows()
