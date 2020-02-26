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

    top_left_x = points_coord["left-ear-2"][0]
    top_left_y = points_coord["left-ear-2"][1]
    width = points_coord["right-ear-2"][0] - points_coord["left-ear-2"][0]
    height = points_coord["mouth"][1] - points_coord["left-ear-2"][1]
    points_coord.update({"top_left_y": top_left_y, "width": width, "top_left_x": top_left_x, "height": height})
    return points_coord

def add_roi_box(image, coordinates, color=(19, 199, 109)):
    output = image.copy()

    cv2.line(output, (coordinates["top_left_x"], coordinates["top_left_y"]),
                     (coordinates["top_left_x"] + coordinates["width"], coordinates["top_left_y"]),
                     (19, 199, 109))
    cv2.line(output, (coordinates["top_left_x"] + coordinates["width"], coordinates["top_left_y"]),
                     (coordinates["top_left_x"] + coordinates["width"], coordinates["top_left_y"] + coordinates["height"]),
                     (19, 199, 109))
    cv2.line(output, (coordinates["top_left_x"] + coordinates["width"], coordinates["top_left_y"] + coordinates["height"]),
                     (coordinates["top_left_x"], coordinates["top_left_y"] + coordinates["height"]),
                     (19, 199, 109))
    cv2.line(output, (coordinates["top_left_x"], coordinates["top_left_y"] + coordinates["height"]),
                     (coordinates["top_left_x"], coordinates["top_left_y"]),
                     (19, 199, 109))
    return output

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

def add_eyes(image, left_eye_coordinates, right_eye_coordinates, radius=2, color=(19, 199, 109)):
    output = image.copy()
    output = cv2.circle(output, left_eye_coordinates, radius, color, -1)
    output = cv2.circle(output, right_eye_coordinates, radius, color, -1)
    return output

def get_resized_eye_point_position(img_original, resized_image, original_coordinates):
    original_width = img_original.shape[1]
    original_height = img_original.shape[0]
    resized_width = resized_image.shape[1]
    resized_height = resized_image.shape[0]

    new_x = (original_coordinates[0]/original_width)*resized_width
    new_y = (original_coordinates[1]/original_height)*resized_height

    new_x = round(new_x)
    new_y = round(new_y)
    return (new_x, new_y)

def verify_and_get_valid_roi(rects, left_eye_coordinates, right_eye_coordinates):
    left_eye_x, left_eye_y = left_eye_coordinates[0], left_eye_coordinates[1]
    right_eye_x, right_eye_y = right_eye_coordinates[0], right_eye_coordinates[1]
    for rect in rects:
        x,y,w,h = int(rect[0]), int(rect[1]), int(rect[2]), int(rect[3])
        test_1 = left_eye_y < y + h and left_eye_y > y
        test_2 = left_eye_x > x and left_eye_x < x + w
        if test_1 and test_2:
            return (True, (x, y, w, h))

    return (False, (None, None, None, None))
