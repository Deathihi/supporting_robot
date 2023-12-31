import cv2
import numpy as np

# Global variables for perspective transformation
src_points = np.float32([(200, 720), (1100, 720), (590, 450), (690, 450)])
dst_points = np.float32([(300, 720), (980, 720), (300, 0), (980, 0)])

# Function to apply perspective transform
def warp_image(img):
    M = cv2.getPerspectiveTransform(src_points, dst_points)
    warped_img = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_LINEAR)
    return warped_img

# Callback function for track bars
def update_perspective(val):
    global src_points, dst_points
    src_points[0, 0] = cv2.getTrackbarPos('Top-Left X', 'Perspective Adjustment')
    src_points[0, 1] = cv2.getTrackbarPos('Top-Left Y', 'Perspective Adjustment')
    src_points[1, 0] = cv2.getTrackbarPos('Top-Right X', 'Perspective Adjustment')
    src_points[1, 1] = cv2.getTrackbarPos('Top-Right Y', 'Perspective Adjustment')
    src_points[2, 0] = cv2.getTrackbarPos('Bottom-Left X', 'Perspective Adjustment')
    src_points[2, 1] = cv2.getTrackbarPos('Bottom-Left Y', 'Perspective Adjustment')
    src_points[3, 0] = cv2.getTrackbarPos('Bottom-Right X', 'Perspective Adjustment')
    src_points[3, 1] = cv2.getTrackbarPos('Bottom-Right Y', 'Perspective Adjustment')

# Function to set up track bars for perspective adjustment
def setup_trackbars():
    cv2.createTrackbar('Top-Left X', 'Perspective Adjustment', src_points[0, 0], 1920, update_perspective)
    cv2.createTrackbar('Top-Left Y', 'Perspective Adjustment', src_points[0, 1], 1080, update_perspective)
    cv2.createTrackbar('Top-Right X', 'Perspective Adjustment', src_points[1, 0], 1920, update_perspective)
    cv2.createTrackbar('Top-Right Y', 'Perspective Adjustment', src_points[1, 1], 1080, update_perspective)
    cv2.createTrackbar('Bottom-Left X', 'Perspective Adjustment', src_points[2, 0], 1920, update_perspective)
    cv2.createTrackbar('Bottom-Left Y', 'Perspective Adjustment', src_points[2, 1], 1080, update_perspective)
    cv2.createTrackbar('Bottom-Right X', 'Perspective Adjustment', src_points[3, 0], 1920, update_perspective)
    cv2.createTrackbar('Bottom-Right Y', 'Perspective Adjustment', src_points[3, 1], 1080, update_perspective)

# Capture video from the camera
cap = cv2.VideoCapture(0)

# Set up track bars
cv2.namedWindow('Perspective Adjustment')
setup_trackbars()

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Crop the region of interest
    roi = frame[450:720, 200:1100]

    # Apply color detection (you can replace this with your color detection code)
    # For example, you can use cv2.inRange to filter a specific color range
    lower_white = np.array([200, 200, 200], dtype=np.uint8)
    upper_white = np.array([255, 255, 255], dtype=np.uint8)
    mask_white = cv2.inRange(roi, lower_white, upper_white)
    result = cv2.bitwise_and(roi, roi, mask=mask_white)

    # Apply perspective transform
    bird_eye_view = warp_image(result)

    # Display the frame, region of interest, and bird's eye view
    cv2.imshow('Original Frame', frame)
    cv2.imshow('Region of Interest', roi)
    cv2.imshow('Bird Eye View', bird_eye_view)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
