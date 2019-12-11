import tools
import cv2

root_path = "CAT_00"

# Gets all the available image paths
paths = tools.retrieve_img_file_paths(root_path)

# Gets just one image, to debug purposes
random_image_path = tools.choose_random_images(paths, num_of_images=1)
random_image_path = random_image_path[0]

# Visualizates images
tools.read_and_show_image(random_image_path)

# Plots landmark coordinates

coordinates = tools.retrieve_face_coordinates(random_image_path)
image = cv2.imread(random_image_path)
img_with_landmark = tools.add_facial_landmarks(image, coordinates)
tools.show_cv2_image(img_with_landmark)
