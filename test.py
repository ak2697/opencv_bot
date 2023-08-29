import cv2
import numpy as np

# Define the text to put on the frame
text = "Hello World!"

# Define the font parameters
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
thickness = 2

# Define the margin around the text
margin = 10

# Create a VideoCapture object to capture frames from the default camera
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    if not ret:
        # Exit the loop if there is an error reading the frame
        break

    # Determine the size of the text
    textSize, _ = cv2.getTextSize(text, font, fontScale, thickness)

    # Calculate the coordinates of the black box
    boxTopLeft = (0, 0)
    boxBottomRight = (textSize[0] + 2 * margin, textSize[1] + 2 * margin)

    # Create a black background for the black box
    background = np.zeros((boxBottomRight[1], boxBottomRight[0], 3), dtype=np.uint8)

    # Draw the black box on the background
    cv2.rectangle(background, boxTopLeft, boxBottomRight, (0, 0, 0), -1)

    # Put the text inside the black box
    textOrg = (margin, textSize[1] + margin)
    cv2.putText(background, text, textOrg, font, fontScale, (255, 255, 255), thickness)

    # Overlay the black box with text onto the frame
    frame[0:boxBottomRight[1], 0:boxBottomRight[0], :] = background

    # Display the frame
    cv2.imshow("Camera Feed", frame)

    # Check for key press events
    key = cv2.waitKey(1)
    if key == ord("q"):
        # Exit the loop if the 'q' key is pressed
        break

# Release the VideoCapture object and close all windows
cap.release()
cv2.destroyAllWindows()
