import glob
import random
import cv2


def retrieve_img_file_paths(path, img_format="jpg"):
    return glob.glob("{}/*.{}".format(path, img_format), recursive=True)

def read_and_show_image(path):
    img = cv2.imread(path)
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_cv2_image(img):
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def choose_random_images(paths, num_of_images=1000):
    return random.choices(paths, k=num_of_images)

def retrieve_face_coordinates(path, text_format="cat"):
    with open("{}.{}".format(path, text_format)) as f: 
        coordinates = str(f.read())
        points = [int(i) for i in coordinates.split(" ") if len(i) > 0]

    points_coord = {"left-eye": (points[1], points[2]),
                    "right-eye": (points[3], points[4]),
                    "mouth": (points[5], points[6]),
                    "left-ear-1": (points[7], points[8]),
                    "left-ear-2": (points[9], points[10]),
                    "left-ear-3": (points[11], points[12]),
                    "right-ear-1": (points[13], points[14]),
                    "right-ear-2": (points[15], points[16]),
                    "right-ear-3": (points[17], points[18]),
                   }
    return points_coord

def add_facial_landmarks(image, coordinates, color=(19, 199, 109)):
    output = image.copy()

    cv2.line(output, coordinates["left-ear-1"], coordinates["left-ear-2"], (19, 199, 109))
    cv2.line(output, coordinates["left-ear-2"], coordinates["left-ear-3"], (19, 199, 109))
    cv2.line(output, coordinates["left-ear-3"], coordinates["right-ear-1"], (19, 199, 109))
    cv2.line(output, coordinates["right-ear-1"], coordinates["right-ear-2"], (19, 199, 109))
    cv2.line(output, coordinates["right-ear-2"], coordinates["right-ear-3"], (19, 199, 109))
    cv2.line(output, coordinates["left-ear-1"], coordinates["left-eye"], (19, 199, 109))
    cv2.line(output, coordinates["right-ear-3"], coordinates["right-eye"], (19, 199, 109))
    cv2.line(output, coordinates["right-eye"], coordinates["mouth"], (19, 199, 109))
    cv2.line(output, coordinates["left-eye"], coordinates["mouth"], (19, 199, 109))

    return output
