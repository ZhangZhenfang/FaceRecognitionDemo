import cv2
import dlib


dlib_face_detector = dlib.get_frontal_face_detector()


def detect_and_sub(img, model_path):
    sp = dlib.shape_predictor(model_path)
    dets = dlib_face_detector(img, 1)
    faces = dlib.full_object_detections()
    i = 0
    if len(dets) != 0:
        for detection in dets:
            faces.append(sp(img, detection))
        images = dlib.get_face_chips(img, faces, size=128)
        return images
    return None


def detect_and_label(img):
    dets = dlib_face_detector(img, 1)
    if len(dets) != 0:
        for detection in dets:
            cv2.rectangle(img,
                          (detection.left(), detection.top()),
                          (detection.right(), detection.bottom()),
                          (0, 255, 0),
                          2)


# imread = cv2.imread("20190430094309.jpg")
#
# detect_and_lable(imread)
#
# cv2.imwrite("201904300943090.jpg", imread)
