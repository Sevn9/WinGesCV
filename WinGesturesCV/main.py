import cv2
import mediapipe as mp
import pyautogui
import copy

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    hand_detector = mp.solutions.hands.Hands()
    drawing_utils = mp.solutions.drawing_utils
    # корректируем экран относительно камеры
    screen_width, screen_height = pyautogui.size()
    index_y = 0

    while True:
        _, frame = cap.read()
        # нужно чтобы правильно относительно экрана рисовать
        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = hand_detector.process(rgb_frame)
        hands = output.multi_hand_landmarks
        # Если обнаруживает руки, то рисует точки
        if hands:
            for hand in hands:
                drawing_utils.draw_landmarks(frame, hand)
                landmarks = hand.landmark
                scroll_amount = 300
                # вывод координат точки под индексом 8 (на указательном пальце)
                for id, landmarks in enumerate(landmarks):
                    x = int(landmarks.x*frame_width)
                    y = int(landmarks.y*frame_height)
                    if id == 8:
                        cv2.circle(img=frame, center=(x,y), radius=10, color=(0,255,255)) # рисуем кружок на этой точке для понимания
                        index_x = screen_width/frame_width*x
                        index_y = screen_height/frame_height*y
                        pyautogui.moveTo(index_x, index_y) # перемещаем курсор мыши по координатам точки
                    if id == 4:
                        cv2.circle(img=frame, center=(x, y), radius=10,
                                   color=(0, 255, 255))  # рисуем кружок на этой точке для понимания
                        thumb_x = screen_width / frame_width * x
                        thumb_y = screen_height / frame_height * y
                        #print(abs(index_y - thumb_y))
                        if abs(index_y - thumb_y) < 70:
                            print('Click operation')
                            pyautogui.click()
                            pyautogui.sleep(10)
                    if id == 20:
                        cv2.circle(img=frame, center=(x, y), radius=10,
                                   color=(0, 255, 255))  # рисуем кружок на этой точке для понимания
                        middle_x = screen_width / frame_width * x
                        middle_y = screen_height / frame_height * y
                       # if abs(index_y - middle_y) < 70:
                           # print('scroll operation')
                           # prev_index_y = copy.deepcopy(index_y)
                           # prev_middle_y = copy.deepcopy(middle_y)
                           # print("prev")
                           # print(prev_index_y, prev_middle_y)
                           # print("index")
                            #print(prev_index_y, prev_middle_y)
                        if thumb_y < middle_y:
                                # Опустились, прокручиваем вниз
                            pyautogui.scroll(-scroll_amount)
                            pyautogui.sleep(1)
                            print('scroll down operation')
                        if thumb_y > middle_y:
                                # Опустились, прокручиваем вверх
                            pyautogui.scroll(scroll_amount)
                            pyautogui.sleep(1)
                            print('scroll up operation')


        #print(hands)
        cv2.imshow('Virtual Mouse', frame)
        cv2.waitKey(1)

