from imutils.video import VideoStream
import cv2
import math
from concurrent.futures import ThreadPoolExecutor
from face_holder import FaceHolder

webcam_angle = math.pi/3


def main():
    window_name = "Face tracking"
    vs = VideoStream(src=1).start()
    cv2.namedWindow(window_name, cv2.WINDOW_GUI_EXPANDED)
    face_cascade = cv2.CascadeClassifier("data/haarcascade_frontalface_default.xml")
    face_holder = FaceHolder()

    with ThreadPoolExecutor(max_workers=2) as executor:
        while True:
            frame = vs.read()
            faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=8, minSize=(10, 10))
            face, centroid = face_holder.update(faces)  # actual face
            if face is not None:
                (x, y, w, h) = face
                executor.submit(calculate_angle, centroid[0], frame.shape[1], webcam_angle)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
            cv2.imshow(window_name, frame)
            cv2.waitKey(1)


def calculate_angle(centroid_x, image_width, camera_angle):
    tan = (((image_width / 2) - centroid_x) / (image_width / 2)) * math.tan(camera_angle/2)
    print(math.atan(tan))


if __name__ == '__main__':
    main()
