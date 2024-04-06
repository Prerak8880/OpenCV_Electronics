import cv2
import time
import serial
from cvzone.HandTrackingModule import HandDetector  # Import the HandDetector class from your module

# Initialize the HandDetector with appropriate parameters
detector = HandDetector(maxHands=1, detectionCon=0.8)

# Open the video capture device
video = cv2.VideoCapture(0)

# Specify the correct COM port for Arduino
arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

while True:
    # Read a frame from the video capture device
    _, img = video.read()
    img = cv2.flip(img, 1)  # Flip the image horizontally

    # Use the HandDetector to find hands in the image
    hands, img = detector.findHands(img, draw=False)

    if hands:
        hand = hands[0]  # Get the first detected hand
        finger_up = detector.fingersUp(hand)
        gesture = ''.join(map(str, finger_up))  # Convert finger configuration to a string

        # Send corresponding signals to Arduino based on the detected gesture
        if gesture == '00000':
            arduino.write(b'0')  # Send '0' to Arduino
            print("0")
        elif gesture == '01000':
            arduino.write(b'1')  # Send '1' to Arduino
            print("1")
        elif gesture == '01100':
            arduino.write(b'2')  # Send '2' to Arduino
            print("2")
        elif gesture == '01110':
            arduino.write(b'3')  # Send '3' to Arduino
            print("3")
        elif gesture == '01111':
            arduino.write(b'4')  # Send '4' to Arduino
            print("4")
        elif gesture == '11111':
            arduino.write(b'5')  # Send '5' to Arduino
            print("5")

    # Display the processed image
    cv2.imshow("Video", img)

    # Check for key press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Pause for a short duration to avoid high CPU usage
    time.sleep(0.1)

# Release the video capture device and close all OpenCV windows
video.release()
cv2.destroyAllWindows()
