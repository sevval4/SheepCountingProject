import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO("yolov5s.pt")

region1 = np.array([(500, 0), (500, 720), (550, 720), (550, 0)])
region1 = region1.reshape((-1, 1, 2))

total = set()

font = cv2.FONT_HERSHEY_DUPLEX
kamera = cv2.VideoCapture("video.mp4")

while True:
    ret, frame = kamera.read()
    if not ret:
        break

    rgb_img = cv2.resize(frame, (640, 480))

    results = model(rgb_img)

    for output in results.pred:
        for box in output:
            x1, y1, x2, y2, conf, cls = box.tolist()
            name = output.names[int(cls)]

            if name == "sheep" and conf > 0.3:
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                inside_region1 = cv2.pointPolygonTest(region1, (cx, cy), False)
                if inside_region1 > 0:
                    total.add(ids)

    total_str = "TOTAL: " + str(len(total))
    frame[0:70, 0:360] = (102, 0, 153)
    cv2.putText(frame, total_str, (0, 60), font, 2.2, (255, 255, 255), 2)

    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

kamera.release()
cv2.destroyAllWindows()
