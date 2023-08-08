import math,re
import mediapipe as mp


def translate(cam,results,text_encode = list):
    MPHands = mp.solutions.hands
    LmHArray = []
    left = False
    right = False
    if results.multi_hand_landmarks:
        for hlms in results.multi_hand_landmarks:
            handindex = results.multi_hand_landmarks.index(hlms)
            handlabel = results.multi_handedness[handindex].classification[0].label
            if handlabel == "Left":
                left = True
                px, py = int(hlms.landmark[MPHands.HandLandmark.INDEX_FINGER_TIP].x * cam.shape[1]), int(hlms.landmark[MPHands.HandLandmark.INDEX_FINGER_TIP].y * cam.shape[0])
            elif handlabel == "Right":
                right = True
                xl0, yl0 = int(hlms.landmark[MPHands.HandLandmark.WRIST].x * cam.shape[1]), int(hlms.landmark[MPHands.HandLandmark.WRIST].y * cam.shape[0])
                xl1, yl1 = int(hlms.landmark[MPHands.HandLandmark.THUMB_CMC].x * cam.shape[1]), int(hlms.landmark[MPHands.HandLandmark.THUMB_CMC].y * cam.shape[0])
                xl2, yl2 = int(hlms.landmark[MPHands.HandLandmark.THUMB_MCP].x * cam.shape[1]), int(hlms.landmark[MPHands.HandLandmark.THUMB_MCP].y * cam.shape[0])
                xl3, yl3 = int(hlms.landmark[MPHands.HandLandmark.THUMB_IP].x * cam.shape[1]), int(hlms.landmark[MPHands.HandLandmark.THUMB_IP].y * cam.shape[0])
                xl4, yl4 = int(hlms.landmark[MPHands.HandLandmark.THUMB_TIP].x * cam.shape[1]), int(hlms.landmark[MPHands.HandLandmark.THUMB_TIP].y * cam.shape[0])
                xl5, yl5 = int(hlms.landmark[MPHands.HandLandmark.INDEX_FINGER_MCP].x * cam.shape[1]), int(hlms.landmark[MPHands.HandLandmark.INDEX_FINGER_MCP].y * cam.shape[0])
                xl6, yl6 = int(hlms.landmark[MPHands.HandLandmark.INDEX_FINGER_PIP].x * cam.shape[1]), int(hlms.landmark[MPHands.HandLandmark.INDEX_FINGER_PIP].y * cam.shape[0])
                xl7, yl7 = int(hlms.landmark[MPHands.HandLandmark.INDEX_FINGER_DIP].x * cam.shape[1]), int(hlms.landmark[MPHands.HandLandmark.INDEX_FINGER_DIP].y * cam.shape[0])
                xl8, yl8 = int(hlms.landmark[MPHands.HandLandmark.INDEX_FINGER_TIP].x * cam.shape[1]), int(hlms.landmark[MPHands.HandLandmark.INDEX_FINGER_TIP].y * cam.shape[0])
                xl9, yl9 = int(hlms.landmark[MPHands.HandLandmark.MIDDLE_FINGER_MCP].x * cam.shape[1]), int(hlms.landmark[MPHands.HandLandmark.MIDDLE_FINGER_MCP].y * cam.shape[0])
                xl10, yl10 = int(hlms.landmark[MPHands.HandLandmark.MIDDLE_FINGER_PIP].x * cam.shape[1]), int(hlms.landmark[MPHands.HandLandmark.MIDDLE_FINGER_PIP].y * cam.shape[0])
                xl11, yl11 = int(hlms.landmark[MPHands.HandLandmark.MIDDLE_FINGER_DIP].x * cam.shape[1]), int(hlms.landmark[MPHands.HandLandmark.MIDDLE_FINGER_DIP].y * cam.shape[0])
                xl12, yl12 = int(hlms.landmark[MPHands.HandLandmark.MIDDLE_FINGER_TIP].x * cam.shape[1]), int(hlms.landmark[MPHands.HandLandmark.MIDDLE_FINGER_TIP].y * cam.shape[0])
                xl13, yl13 = int(hlms.landmark[MPHands.HandLandmark.RING_FINGER_MCP].x * cam.shape[1]), int(hlms.landmark[MPHands.HandLandmark.RING_FINGER_MCP].y * cam.shape[0])
                xl14, yl14 = int(hlms.landmark[MPHands.HandLandmark.RING_FINGER_PIP].x * cam.shape[1]), int(hlms.landmark[MPHands.HandLandmark.RING_FINGER_PIP].y * cam.shape[0])
                xl15, yl15 = int(hlms.landmark[MPHands.HandLandmark.RING_FINGER_DIP].x * cam.shape[1]), int(hlms.landmark[MPHands.HandLandmark.RING_FINGER_DIP].y * cam.shape[0])
                xl16, yl16 = int(hlms.landmark[MPHands.HandLandmark.RING_FINGER_TIP].x * cam.shape[1]), int(hlms.landmark[MPHands.HandLandmark.RING_FINGER_TIP].y * cam.shape[0])
                xl17, yl17 = int(hlms.landmark[MPHands.HandLandmark.PINKY_MCP].x * cam.shape[1]), int(hlms.landmark[MPHands.HandLandmark.PINKY_MCP].y * cam.shape[0])
                xl18, yl18 = int(hlms.landmark[MPHands.HandLandmark.PINKY_PIP].x * cam.shape[1]), int(hlms.landmark[MPHands.HandLandmark.PINKY_PIP].y * cam.shape[0])
                xl19, yl19 = int(hlms.landmark[MPHands.HandLandmark.PINKY_DIP].x * cam.shape[1]), int(hlms.landmark[MPHands.HandLandmark.PINKY_DIP].y * cam.shape[0])
                xl20, yl20 = int(hlms.landmark[MPHands.HandLandmark.PINKY_TIP].x * cam.shape[1]), int(hlms.landmark[MPHands.HandLandmark.PINKY_TIP].y * cam.shape[0])
                xc,yc= (xl9+xl0)//2 , (yl9+yl0)//2
                xmin = min([landmark.x for landmark in hlms.landmark])
                ymin = min([landmark.y for landmark in hlms.landmark])
                xmax = max([landmark.x for landmark in hlms.landmark])
                ymax = max([landmark.y for landmark in hlms.landmark])
                xmin, ymin, xmax, ymax = int(xmin * cam.shape[1])-20, int(ymin * cam.shape[0])-20, int(xmax * cam.shape[1])+20, int(ymax * cam.shape[0])+20
        for id, lm in enumerate(hlms.landmark):
            h,w,c = cam.shape
            Cx,Cy = int(lm.x*w), int(lm.y*h)
            LmHArray.append([id,Cx,Cy])

    if len(LmHArray) != 0:
        x20,y20 = LmHArray[20][1],LmHArray[20][2]
        x19,y19 = LmHArray[19][1],LmHArray[19][2]
        x18,y18 = LmHArray[18][1],LmHArray[18][2]
        x17,y17 = LmHArray[17][1],LmHArray[17][2]
        x16,y16 = LmHArray[16][1],LmHArray[16][2]
        x14,y14 = LmHArray[14][1],LmHArray[14][2]
        x13,y13 = LmHArray[13][1],LmHArray[13][2]
        x12,y12 = LmHArray[12][1],LmHArray[12][2]
        x11,y11 = LmHArray[11][1],LmHArray[11][2]
        x10,y10 = LmHArray[10][1],LmHArray[10][2]
        x9,y9 = LmHArray[9][1],LmHArray[9][2]
        x8,y8 = LmHArray[8][1],LmHArray[8][2]
        x7,y7 = LmHArray[7][1],LmHArray[7][2]
        x4,y4 = LmHArray[4][1],LmHArray[4][2]
        x6,y6 = LmHArray[6][1],LmHArray[6][2]
        x5,y5 = LmHArray[5][1],LmHArray[5][2]
        x3,y3 = LmHArray[3][1],LmHArray[3][2]
        x1,y1 = LmHArray[1][1],LmHArray[1][2]
        x0,y0 = LmHArray[0][1],LmHArray[0][2]
        L5_8 = math.hypot(x5-x8,y5-y8)
        L13_16 = math.hypot(x13-x16,y13-y16)
        L10_11 = math.hypot(x10-x11,y10-y11)
        L4_12 = math.hypot(x4-x12,y4-y12)
        L4_10 = math.hypot(x4-x10,y4-y10)
        L9_10 = math.hypot(x10-x9,y10-y9)
        L8_12 = math.hypot(x8-x12,y8-y12)
        L7_11 = math.hypot(x7-x11,y7-y11)
        L4_6 = math.hypot(x4-x6,y4-y6)
        L4_3 = math.hypot(x4-x3,y4-y3)
        L4_8 = math.hypot(x4-x8,y4-y8)
        L0_8 = math.hypot(x0-x8,y0-y8)
        L5_9 = math.hypot(x5-x9,y5-y9)
        L4_14 = math.hypot(x4-x14,y4-y14)
        L11_12 = math.hypot(x11-x12,y11-y12)
        L12_16 = math.hypot(x12-x16,y12-y16)
        L4_16 = math.hypot(x4-x16,y4-y16)
        L17_20 = math.hypot(x17-x20,y17-y20)
        L17_18 = math.hypot(x17-x18,y17-y18)
        L18_19 = math.hypot(x18-x19,y18-y19)
        L19_20 = math.hypot(x19-x20,y19-y20)
        if left == True and right == True:
            Lp_l0 = math.hypot(xl0-px,yl0-py)
            Lp_l1 = math.hypot(xl1-px,yl1-py)
            Lp_l2 = math.hypot(xl2-px,yl2-py)
            Lp_l3 = math.hypot(xl3-px,yl3-py)
            Lp_l4 = math.hypot(xl4-px,yl4-py)
            Lp_l5 = math.hypot(xl5-px,yl5-py)
            Lp_l6 = math.hypot(xl6-px,yl6-py)
            Lp_l7 = math.hypot(xl7-px,yl7-py)
            Lp_l8 = math.hypot(xl8-px,yl8-py)
            Lp_l9 = math.hypot(xl9-px,yl9-py)
            Lp_l10 = math.hypot(xl10-px,yl10-py)
            Lp_l11 = math.hypot(xl11-px,yl11-py)
            Lp_l12 = math.hypot(xl12-px,yl12-py)
            Lp_l13 = math.hypot(xl13-px,yl13-py)
            Lp_l14 = math.hypot(xl14-px,yl14-py)
            Lp_l15 = math.hypot(xl15-px,yl15-py)
            Lp_l16 = math.hypot(xl16-px,yl16-py)
            Lp_l17 = math.hypot(xl17-px,yl17-py)
            Lp_l18 = math.hypot(xl18-px,yl18-py)
            Lp_l19 = math.hypot(xl19-px,yl19-py)
            Lp_l20 = math.hypot(xl20-px,yl20-py)
            Lp_c = math.hypot(px-xc,py-yc)
            if xmin < px < xmax and ymin < py < ymax:
                if yl8 < yl7 < yl6 < yl5 and yl12 < yl11 < yl10 < yl9 and yl16 < yl15 < yl14 < yl13 and yl20 < yl19 < yl18 < yl17 and xl4 < xl3 :
                    if yc < py and Lp_l1 > Lp_l0 and Lp_l2 > Lp_l0 and Lp_l3 > Lp_l0 and Lp_c > Lp_l0 and Lp_l4 > Lp_l0 and Lp_l5 > Lp_l0 and Lp_l6 > Lp_l0 and Lp_l7 > Lp_l0 and Lp_l9 > Lp_l0 and Lp_l8 > Lp_l0:
                        text_encode.append('a')
                    elif xc > px and Lp_l0 > Lp_l2 and Lp_l4 > Lp_l2 and Lp_c > Lp_l2 and Lp_l5 > Lp_l2 and Lp_l6 > Lp_l2 and Lp_l7 > Lp_l2 and Lp_l8 > Lp_l2 and Lp_l9 > Lp_l2 and Lp_l10 > Lp_l2 and Lp_l11 > Lp_l2 and Lp_l12 > Lp_l2 and Lp_l14 > Lp_l2 and Lp_l13 > Lp_l2 and Lp_l16 > Lp_l2 and Lp_l15 > Lp_l2 and Lp_l18 > Lp_l2 and Lp_l19 > Lp_l2 and Lp_l17 > Lp_l2 and Lp_l6 > Lp_l2 and Lp_l3 > Lp_l2:
                        text_encode.append('b')
                    elif xc > px and Lp_l2 > Lp_l4 and Lp_l1 > Lp_l4 and Lp_l0 > Lp_l4 and Lp_l5 > Lp_l4 and Lp_l6 > Lp_l4 and Lp_l7 > Lp_l4 and Lp_l8 > Lp_l4 and Lp_l9 > Lp_l4 and Lp_l10 > Lp_l4 and Lp_l11 > Lp_l4 and Lp_l12 > Lp_l4 and Lp_l13 > Lp_l4 and Lp_l14 > Lp_l4 and Lp_l15 > Lp_l4 and Lp_l16 > Lp_l4 and Lp_l17 > Lp_l4 and Lp_l18 > Lp_l4 and Lp_l19 > Lp_l4 and Lp_l20 > Lp_l4:
                        text_encode.append('c')
                    elif Lp_l0 > Lp_c and Lp_l1 > Lp_c and Lp_l2 > Lp_c and Lp_l3 > Lp_c and Lp_l4 > Lp_c and Lp_l5 > Lp_c and Lp_l6 > Lp_c and Lp_l7 > Lp_c and Lp_l8 > Lp_c and Lp_l9 > Lp_c and Lp_l10 > Lp_c and Lp_l11 > Lp_c and Lp_l12 > Lp_c and Lp_l13 > Lp_c and Lp_l14 > Lp_c and Lp_l15 > Lp_c and Lp_l16 > Lp_c and Lp_l17 > Lp_c and Lp_l18 > Lp_c and Lp_l19 > Lp_c and Lp_l20 > Lp_c:
                        text_encode.append('e')
                    elif Lp_l0 > Lp_l5 and Lp_l8 > Lp_l5 and Lp_l9 > Lp_l5 and Lp_l1 > Lp_l5 and Lp_l2 > Lp_l5 and Lp_l3 > Lp_l5 and Lp_l4 > Lp_l5 and Lp_l7 > Lp_l5 and Lp_c > Lp_l5 and Lp_l10 > Lp_l5 and Lp_l11 > Lp_l5 and Lp_l12 > Lp_l5 and Lp_l13 > Lp_l5 and Lp_l14 > Lp_l5 and Lp_l15 > Lp_l5 and Lp_l16 > Lp_l5 and Lp_l17 > Lp_l5 and Lp_l18 > Lp_l5 and Lp_l19 > Lp_l5 and Lp_l20 > Lp_l5 and Lp_c > Lp_l5:
                        text_encode.append('f')
                    elif Lp_l0 > Lp_l8 and Lp_l1 > Lp_l8 and Lp_l2 > Lp_l8 and Lp_l3 > Lp_l8 and Lp_l4 > Lp_l8 and Lp_l5 > Lp_l8 and Lp_l6 > Lp_l8 and Lp_l9 > Lp_l8 and Lp_l10 > Lp_l8 and Lp_l11 > Lp_l8 and Lp_l12 > Lp_l8 and Lp_l13 > Lp_l8 and Lp_l14 > Lp_l8 and Lp_l15 > Lp_l8 and Lp_l16 > Lp_l8 and Lp_l17 > Lp_l8 and Lp_l18 > Lp_l8 and Lp_l19 > Lp_l8 and Lp_l20 > Lp_l8:
                        text_encode.append('g')
                    elif Lp_l0 > Lp_l9 and Lp_l1 > Lp_l9 and Lp_l2 > Lp_l9 and Lp_l3 > Lp_l9 and Lp_l4 > Lp_l9 and Lp_l5 > Lp_l9 and Lp_l6 > Lp_l9 and Lp_l7 > Lp_l9 and Lp_l8 > Lp_l9 and Lp_l11 > Lp_l9 and Lp_l12 > Lp_l9 and Lp_l13 > Lp_l9 and Lp_l14 > Lp_l9 and Lp_l15 > Lp_l9 and Lp_l16 > Lp_l9 and Lp_l17 > Lp_l9 and Lp_l18 > Lp_l9 and Lp_l19 > Lp_l9 and Lp_l20 > Lp_l9 and Lp_c > Lp_l9:
                        text_encode.append('i')
                    elif Lp_l0 > Lp_l12  and Lp_l1 > Lp_l12 and Lp_l2 > Lp_l12 and Lp_l3 > Lp_l12 and Lp_l4 > Lp_l12 and Lp_l5 > Lp_l12 and Lp_l6 > Lp_l12 and Lp_l7 > Lp_l12 and Lp_l8 > Lp_l12 and Lp_l9 > Lp_l12 and Lp_l10 > Lp_l12 and Lp_l13 > Lp_l12 and Lp_l14 > Lp_l12 and Lp_l15 > Lp_l12 and Lp_l16 > Lp_l12 and Lp_l17 > Lp_l12 and Lp_l18 > Lp_l12 and Lp_l19 > Lp_l12 and Lp_l20 > Lp_l12:
                        text_encode.append('j')
                    elif Lp_l0 > Lp_l13 and Lp_l1 > Lp_l13 and Lp_l2 > Lp_l13 and Lp_l3 > Lp_l13 and Lp_l4 > Lp_l13 and Lp_l5 > Lp_l13 and Lp_l6 > Lp_l13 and Lp_l7 > Lp_l13 and Lp_l8 > Lp_l13 and Lp_l9 > Lp_l13 and Lp_l10 > Lp_l13 and Lp_l11 > Lp_l13 and Lp_l12 > Lp_l13 and Lp_l15 > Lp_l13 and Lp_l16 > Lp_l13 and Lp_l17 > Lp_l13 and Lp_l18 > Lp_l13 and Lp_l19 > Lp_l13 and Lp_l20 > Lp_l13 and Lp_c > Lp_l13:
                        text_encode.append('l')
                    elif Lp_l0 > Lp_l16 and Lp_l1 > Lp_l16 and Lp_l2 > Lp_l16 and Lp_l3 > Lp_l16 and Lp_l4 > Lp_l16 and Lp_l5 > Lp_l16 and Lp_l6 > Lp_l16 and Lp_l7 > Lp_l16 and Lp_l8 > Lp_l16 and Lp_l9 > Lp_l16 and Lp_l10 > Lp_l16 and Lp_l11 > Lp_l16 and Lp_l12 > Lp_l16 and Lp_l13 > Lp_l16 and Lp_l14 > Lp_l16 and Lp_l17 > Lp_l16 and Lp_l18 > Lp_l16 and Lp_l19 > Lp_l16 and Lp_l20 > Lp_l16:
                        text_encode.append('m')
                    elif Lp_l0 > Lp_l17 and Lp_l1 > Lp_l17 and Lp_l2 > Lp_l17 and Lp_l3 > Lp_l17 and Lp_l4 > Lp_l17 and Lp_l5 > Lp_l17 and Lp_l6 > Lp_l17 and Lp_l7 > Lp_l17 and Lp_l8 > Lp_l17 and Lp_l9 > Lp_l17 and Lp_l10 > Lp_l17 and Lp_l11 > Lp_l17 and Lp_l12 > Lp_l17 and Lp_l13 > Lp_l17 and Lp_l14 > Lp_l17 and Lp_l15 > Lp_l17 and Lp_l16 > Lp_l17 and Lp_l19 > Lp_l17 and Lp_l20 > Lp_l17 and Lp_c > Lp_l17:
                        text_encode.append('o')
                    elif Lp_l0 > Lp_l20 and Lp_l1 > Lp_l20 and Lp_l2 > Lp_l20 and Lp_l3 > Lp_l20 and Lp_l4 > Lp_l20 and Lp_l5 > Lp_l20 and Lp_l6 > Lp_l20 and Lp_l7 > Lp_l20 and Lp_l8 > Lp_l20 and Lp_l9 > Lp_l20 and Lp_l10 > Lp_l20 and Lp_l11 > Lp_l20 and Lp_l12 > Lp_l20 and Lp_l13 > Lp_l20 and Lp_l14 > Lp_l20 and Lp_l15 > Lp_l20 and Lp_l16 > Lp_l20 and Lp_l17 > Lp_l20 and Lp_l18 > Lp_l20 and Lp_c > Lp_l20:
                        text_encode.append('p')   
                else:
                    text_encode.append('Y')
        if left == True and right == False:
            if LmHArray[0][2] > LmHArray[5][2] and LmHArray[17][2] < LmHArray[20][2] and LmHArray[13][2] < LmHArray[16][2] and LmHArray[7][2] < LmHArray[5][2] and LmHArray[6][2] < LmHArray[14][2] and LmHArray[7][2] < LmHArray[20][2] and LmHArray[7][2] < LmHArray[16][2] and LmHArray[7][2] < LmHArray[12][2] and LmHArray[8][2] < LmHArray[4][2] and LmHArray[8][2] < LmHArray[20][2] and LmHArray[8][2] < LmHArray[16][2] and LmHArray[8][2] < LmHArray[12][2] and LmHArray[8][2] < LmHArray[7][2] and LmHArray[7][2] < LmHArray[6][2] and LmHArray[6][2] < LmHArray[5][2]:
                if L4_6 > L4_12 and LmHArray[4][1] < LmHArray[3][1] and LmHArray[9][2] < LmHArray[12][2] and LmHArray[4][2] < LmHArray[12][2]:
                    text_encode.append('1')
                elif L4_6 < L4_12 and LmHArray[4][2] < LmHArray[5][2]  and LmHArray[0][2] > LmHArray[5][2] and LmHArray[8][1] < LmHArray[7][1] and LmHArray[7][1] < LmHArray[6][1] and LmHArray[6][1] < LmHArray[5][1] and LmHArray[10][1] < LmHArray[11][1] and LmHArray[14][1] < LmHArray[15][1] and LmHArray[18][1] < LmHArray[19][1] and LmHArray[10][2] < LmHArray[14][2] and LmHArray[14][2] < LmHArray[18][2] and LmHArray[4][2] < LmHArray[10][2]:
                    text_encode.append('s')
                elif LmHArray[4][1] > LmHArray[3][1] and LmHArray[9][2] < LmHArray[12][2]:
                    text_encode.append('K')
                elif LmHArray[9][2] > LmHArray[12][2] and LmHArray[11][2] < LmHArray[12][2] and LmHArray[4][2] < LmHArray[3][2] and LmHArray[4][2] < LmHArray[14][2]:
                    text_encode.append('I')
            elif LmHArray[0][2] > LmHArray[5][2] and LmHArray[19][2] < LmHArray[20][2] and LmHArray[8][2] < LmHArray[7][2] and LmHArray[7][2] < LmHArray[6][2] and LmHArray[6][2] < LmHArray[5][2] and LmHArray[12][2] < LmHArray[11][2] and LmHArray[11][2] < LmHArray[10][2] and LmHArray[10][2] < LmHArray[9][2] and LmHArray[16][2] < LmHArray[15][2] and LmHArray[15][2] < LmHArray[14][2] and LmHArray[14][2] < LmHArray[13][2] :
                if LmHArray[19][2] > LmHArray[4][2]:
                    text_encode.append('H')
            elif L12_16 < L4_12 and LmHArray[17][1] < LmHArray[20][1] and LmHArray[0][1] < LmHArray[1][1] < LmHArray[2][1] < LmHArray[3][1] and LmHArray[0][1] < LmHArray[4][1] and LmHArray[0][2] > LmHArray[5][2] and LmHArray[5][2] < LmHArray[4][2] and LmHArray[18][1] < LmHArray[20][1] and LmHArray[14][1] < LmHArray[16][1] and LmHArray[10][1] < LmHArray[12][1] and LmHArray[6][2] < LmHArray[5][2] and LmHArray[10][2] < LmHArray[9][2] and LmHArray[14][2] < LmHArray[13][2] and LmHArray[18][2] < LmHArray[17][2] and LmHArray[3][1] < LmHArray[4][1]:
                text_encode.append('P')
            elif LmHArray[4][2] < LmHArray[5][2] and LmHArray[8][2] < LmHArray[7][2] < LmHArray[6][2] < LmHArray[5][2] and LmHArray[12][2] < LmHArray[11][2] < LmHArray[10][2] < LmHArray[9][2] and LmHArray[16][2] < LmHArray[15][2] < LmHArray[14][2] < LmHArray[13][2] and LmHArray[20][2] < LmHArray[19][2] < LmHArray[18][2] < LmHArray[17][2] and LmHArray[4][2] < LmHArray[3][2] < LmHArray[2][2] < LmHArray[1][2]:
                text_encode.append('5')
            elif LmHArray[0][2] > LmHArray[5][2] and L4_14 < L4_10 and LmHArray[4][1] < LmHArray[5][1] and LmHArray[4][1] < LmHArray[3][1] and LmHArray[14][2] < LmHArray[18][2] and LmHArray[17][2] < LmHArray[20][2] and LmHArray[13][2] < LmHArray[16][2] and LmHArray[12][2] < LmHArray[9][2] and LmHArray[6][2] < LmHArray[14][2] and LmHArray[7][2] < LmHArray[20][2] and LmHArray[7][2] < LmHArray[16][2] and LmHArray[12][2] < LmHArray[7][2] and LmHArray[8][2] < LmHArray[4][2] and LmHArray[8][2] < LmHArray[20][2] and LmHArray[8][2] < LmHArray[16][2] and LmHArray[12][2] < LmHArray[8][2] and LmHArray[8][2] < LmHArray[7][2] and LmHArray[7][2] < LmHArray[6][2] and LmHArray[6][2] < LmHArray[5][2] and LmHArray[12][2] < LmHArray[11][2] and LmHArray[11][2] < LmHArray[10][2]:  
                if L8_12 > L5_9 :
                    text_encode.append('2')
                else:
                    text_encode.append('G')
            elif LmHArray[3][1] < LmHArray[4][1] and LmHArray[20][2] < LmHArray[19][2] < LmHArray[18][2] < LmHArray[17][2] and LmHArray[4][2] < LmHArray[3][2] < LmHArray[2][2] and LmHArray[6][2] < LmHArray[8][2] and LmHArray[10][2] < LmHArray[12][2] and LmHArray[14][2] < LmHArray[16][2] :
                text_encode.append('M')
            elif LmHArray[0][2] > LmHArray[5][2] and L4_14 > L4_10 and LmHArray[12][2] < LmHArray[11][2] and LmHArray[11][2] < LmHArray[10][2] and LmHArray[10][2] < LmHArray[9][2] and LmHArray[8][2] < LmHArray[7][2] and LmHArray[7][2] < LmHArray[6][2] and LmHArray[6][2] < LmHArray[5][2] and LmHArray[17][2] < LmHArray[20][2] and LmHArray[13][2] < LmHArray[16][2]:
                if LmHArray[4][1] < LmHArray[6][1] and (LmHArray[10][2] < LmHArray[4][2] < LmHArray[9][2] or LmHArray[10][2] < LmHArray[4][2]):
                    text_encode.append('A')
                elif L4_6 > L4_3 and LmHArray[20][2] > LmHArray[17][2] and LmHArray[16][2] > LmHArray[13][2] and LmHArray[4][2]<LmHArray[3][2] and LmHArray[4][2]<LmHArray[5][2] and LmHArray[4][1]>LmHArray[5][1]:
                    text_encode.append('3')
            elif LmHArray[0][2] > LmHArray[5][2] and LmHArray[20][1] < LmHArray[16][1] and LmHArray[16][1] < LmHArray[12][1] and LmHArray[12][1] < LmHArray[8][1] and LmHArray[19][2] < LmHArray[20][2] and LmHArray[15][2] < LmHArray[16][2] and LmHArray[11][2] < LmHArray[12][2] and LmHArray[7][2] < LmHArray[8][2] and LmHArray[8][2] < LmHArray[3][2]:
                if LmHArray[12][2] < LmHArray[4][2] and abs(x4-x3) > abs(y4-y3):
                    if LmHArray[8][2] > LmHArray[11][2] and LmHArray[14][2] < LmHArray[15][2] and LmHArray[10][2] < LmHArray[11][2]:
                        text_encode.append('R')
                    elif LmHArray[8][2] < LmHArray[11][2]:
                        text_encode.append('u')
                elif LmHArray[12][1] < LmHArray[4][1] and abs(y4-y3) > abs(x4-x3):
                    text_encode.append('S')
            elif LmHArray[0][2] > LmHArray[5][2] and LmHArray[12][2] < LmHArray[8][2] and LmHArray[8][2] < LmHArray[6][2] and LmHArray[8][2] < LmHArray[5][2] and LmHArray[12][2] < LmHArray[10][2] and LmHArray[12][2] < LmHArray[9][2] and LmHArray[16][2] < LmHArray[14][2] and LmHArray[20][2] < LmHArray[18][2] and LmHArray[5][2] < LmHArray[3][2]:
                if LmHArray[4][1] < LmHArray[3][1]:
                    if L12_16 > L11_12 and LmHArray[4][1] < LmHArray[3][1]:
                        text_encode.append('4')
                    elif L12_16 < L11_12 and LmHArray[4][1] < LmHArray[3][1]:
                        text_encode.append('F')
            elif LmHArray[0][2] > LmHArray[5][2] and LmHArray[12][2] < LmHArray[8][2] and LmHArray[8][2] < LmHArray[6][2] and LmHArray[8][2] < LmHArray[5][2] and LmHArray[12][2] < LmHArray[10][2] and LmHArray[12][2] < LmHArray[9][2] and LmHArray[16][2] < LmHArray[14][2] and LmHArray[20][2] < LmHArray[18][2] : 
                if LmHArray[3][1] < LmHArray[4][1] and LmHArray[4][2] < LmHArray[5][2]:
                    text_encode.append('5')
            elif LmHArray[0][2] > LmHArray[5][2] and LmHArray[19][2] > LmHArray[14][2] and LmHArray[18][2] < LmHArray[19][2] and LmHArray[14][2] < LmHArray[15][2] and LmHArray[10][2] < LmHArray[11][2] and LmHArray[6][2] < LmHArray[7][2]:
                if LmHArray[18][1] < LmHArray[4][1] and LmHArray[6][1] < LmHArray[4][1] and LmHArray[4][2] < LmHArray[3][2] and LmHArray[4][2] < LmHArray[7][2]:
                    text_encode.append('Q')
                elif LmHArray[4][1] < LmHArray[6][1] and (LmHArray[10][1] < LmHArray[4][1]) and LmHArray[4][2] < LmHArray[12][2] and LmHArray[4][2] < LmHArray[14][2] and LmHArray[4][2] < LmHArray[18][2]:
                    text_encode.append('B')
                elif LmHArray[4][1] < LmHArray[10][1] and LmHArray[14][1] < LmHArray[4][1] and LmHArray[4][2] < LmHArray[14][2] and LmHArray[4][2] and LmHArray[12][2] > LmHArray[14][2]:
                    text_encode.append('O')
                elif LmHArray[14][2] < LmHArray[4][2] and LmHArray[4][2] < LmHArray[18][2] and LmHArray[4][1] < LmHArray[14][1]:
                    text_encode.append('N')
                elif LmHArray[4][1] < LmHArray[3][1] and LmHArray[10][2] < LmHArray[4][2] and LmHArray[6][2] < LmHArray[4][2] and LmHArray[4][2] > LmHArray[18][2] and LmHArray[4][2] < LmHArray[8][2] and LmHArray[4][2] < LmHArray[12][2] and LmHArray[4][2] < LmHArray[16][2]:
                    text_encode.append('C')
            elif LmHArray[0][2] < LmHArray[8][2] and LmHArray[0][2] < LmHArray[12][2] and LmHArray[0][2] < LmHArray[16][2]:
                text_encode.append('D')
            elif L8_12 < L11_12:
                if not LmHArray[20][2] < LmHArray[16][2]:
                    if LmHArray[8][1] < LmHArray[7][1] < LmHArray[6][1] < LmHArray[5][1] and LmHArray[12][1] < LmHArray[11][1] < LmHArray[10][1] < LmHArray[9][1]:
                        text_encode.append('E')
                    elif LmHArray[8][1] > LmHArray[7][1] > LmHArray[6][1] > LmHArray[5][1] and LmHArray[12][1] > LmHArray[11][1] > LmHArray[10][1] > LmHArray[9][1]:
                        text_encode.append('E')
            elif LmHArray[0][2] > LmHArray[5][2] and LmHArray[12][2] < LmHArray[11][2] and LmHArray[11][2] < LmHArray[10][2] and LmHArray[10][2] < LmHArray[9][2] and LmHArray[16][2] < LmHArray[15][2] and LmHArray[15][2] < LmHArray[14][2] and LmHArray[14][2] < LmHArray[13][2] and LmHArray[20][2] < LmHArray[19][2] and LmHArray[19][2] < LmHArray[18][2] and LmHArray[18][2] < LmHArray[17][2] and LmHArray[6][2] < LmHArray[8][2] and LmHArray[6][2] < LmHArray[4][2] and LmHArray[6][2] < LmHArray[3][2]:
                text_encode.append('J')
            elif LmHArray[5][2] < LmHArray[0][2] and LmHArray[14][2] < LmHArray[16][2] and LmHArray[10][2] < LmHArray[12][2] and LmHArray[6][2] < LmHArray[8][2] and LmHArray[18][1] < LmHArray[9][1]:
                if LmHArray[20][2] < LmHArray[19][2] < LmHArray[18][2] < LmHArray[17][2] and LmHArray[4][1] < LmHArray[3][1] and (L19_20+L18_19) > L17_18 :
                    text_encode.append('T')
                elif (L19_20+L18_19) < L17_18 :
                    text_encode.append('U')
            elif LmHArray[0][2] > LmHArray[5][2] and LmHArray[20][2] < LmHArray[19][2] and LmHArray[19][2] < LmHArray[18][2] and LmHArray[18][2] < LmHArray[17][2] and LmHArray[9][1] < LmHArray[18][1] and LmHArray[20][2] < LmHArray[16][2] and LmHArray[20][2] < LmHArray[12][2] and LmHArray[20][2] < LmHArray[8][2] and LmHArray[20][2] < LmHArray[4][2]:
                text_encode.append('L')

def decode(text_encode):
    code = []
    translate_text = ''
    for i in range(0,len(text_encode)):
        if i != len(text_encode)-1:
            if text_encode[i] != text_encode[i+1]:
                if text_encode[i] != text_encode[i-1]:
                    continue
                else:
                    code.append(text_encode[i])
            else:
                continue
        else:
            if text_encode[i] == text_encode[i-1]:
                code.append(text_encode[i])
            else:
                continue
    count = len(code)
    str = ""
    for i in range(0,count):
        str = str + code[i]
    str = str  + 'z'
    if count == 0:
        translate_text = 'None'
        return translate_text
    else:
        for i in range(count):
            if str[i] == 'A': 
                if str[i+1] == '1':
                    get_char = 'ข'
                    translate_text = translate_text + get_char
                    i += 1
                elif str[i+1] == '2':
                    get_char = 'ค'
                    translate_text = translate_text + get_char 
                    i += 1
                elif str[i+1] == '3':
                    get_char = 'ฆ'
                    translate_text = translate_text + get_char
                    i += 1
                else:
                    get_char = 'ก'
                    translate_text = translate_text + get_char 
            elif str[i] == 'B':
                if str[i+1] == '1':
                    get_char = 'ถ'
                    translate_text = translate_text + get_char  
                    i += 1
                elif str[i+1] == '2':
                    get_char = 'ฐ'
                    translate_text = translate_text + get_char 
                    i += 1
                elif str[i+1] == '3':
                    get_char = 'ฒ'
                    translate_text = translate_text + get_char 
                    i += 1
                elif str[i+1] == '4':
                    get_char = 'ฑ'
                    translate_text = translate_text + get_char 
                    i += 1
                elif str[i+1] == '5':
                    get_char = 'ฏ'
                    translate_text = translate_text + get_char 
                    i += 1
                elif str[i+1] == 'E':
                    if str[i+2] == '1':
                        get_char = 'ธ'
                        translate_text = translate_text + get_char 
                        i += 2
                    else:
                        get_char = 'ท'
                        translate_text = translate_text + get_char 
                        i += 1
                else:
                    get_char = 'ต'
                    translate_text = translate_text + get_char 
            elif str[i] == 'C':
                if str[i+1] == '1':
                    get_char = 'ศ'
                    translate_text = translate_text + get_char 
                    i += 1
                elif str[i+1] == '2':
                    get_char = 'ษ'
                    translate_text = translate_text + get_char  
                    i += 1
                elif str[i+1] == 'D':
                    get_char = 'ซ'
                    translate_text = translate_text + get_char   
                    i += 1
                else:
                    get_char = 'ส'
                    translate_text = translate_text + get_char
            elif str[i] == 'D':
                if str[i+1] == '1':
                    get_char = 'ป'
                    translate_text = translate_text + get_char 
                    i += 1
                elif str[i+1] == '2':
                    get_char = 'ผ'
                    translate_text = translate_text + get_char  
                    i += 1
                elif str[i+1] == '3':
                    get_char = 'ภ'
                    translate_text = translate_text + get_char  
                    i += 1
                elif str[i-1] == 'C':
                    i += 2
                    continue
                else:
                    get_char = 'พ'
                    translate_text = translate_text + get_char  
            elif str[i] == 'E':
                if str[i+1] == '1':
                    if str[i-1] == 'B':
                        i += 2
                        continue
                    elif str[i-1] == 'P':
                        i += 2
                        continue
                    else:
                        get_char = 'ฮ'
                        translate_text = translate_text + get_char   
                        i += 1
                elif str[i-1] == 'P':
                    i += 2
                    continue
                elif str[i-1] == 'B':
                    i += 2
                    continue
                else:
                    get_char = 'ห'
                    translate_text = translate_text + get_char
            elif str[i] == 'F':
                get_char = 'บ'
                translate_text = translate_text + get_char
            elif str[i] == 'G':
                get_char = 'ร'
                translate_text = translate_text + get_char
            elif str[i] == 'H':
                get_char = 'ว'
                translate_text = translate_text + get_char 
            elif str[i] == 'I':
                if str[i+1] == '1':
                    get_char = 'ฎ'
                    translate_text = translate_text + get_char  
                    i += 1
                else:
                    get_char = 'ด'
                    translate_text = translate_text + get_char 
            elif str[i] == 'J':
                if str[i+1] == '1':
                    get_char = 'ฝ'
                    translate_text = translate_text + get_char  
                    i += 1
                else:
                    get_char = 'ฟ'
                    translate_text = translate_text + get_char   
            elif str[i] == 'K':
                if str[i+1] == '1':
                    get_char = "ฬ"
                    translate_text = translate_text + get_char
                    i += 1
                else:
                    get_char = "ล"
                    translate_text = translate_text + get_char
            elif str[i] == 'T':
                if str[i+1] == 'L':
                    get_char = "จ"
                    translate_text = translate_text + get_char
                    i += 1
                else:
                    get_char = "ไ"
                    translate_text = translate_text + get_char
            elif str[i] == 'M':
                if str[i+1] == '1':
                    get_char = "ญ"
                    translate_text = translate_text + get_char
                    i += 1
                else:
                    get_char = "ย"
                    translate_text = translate_text + get_char
            elif str[i] == 'N':
                get_char = "ม"
                translate_text = translate_text + get_char
            elif str[i] == 'O':
                if str[i+1] == '1':
                    get_char = "ณ"
                    translate_text = translate_text + get_char
                    i += 1
                elif str[i+1] == 's':
                    get_char = "ง"
                    translate_text = translate_text + get_char
                    i += 1
                else:
                    get_char = "น"
                    translate_text = translate_text + get_char
            elif str[i] == 'P':
                if str[i+1] == 'E':
                    if str[i+2] == '1':
                        get_char = "ช"
                        translate_text = translate_text + get_char
                        i += 2
                    elif str[i+2] == '2':
                        get_char = "ฌ"
                        translate_text = translate_text + get_char
                        i += 2
                    else:
                        get_char = "ฉ"
                        translate_text = translate_text + get_char
            elif str[i] == 'Q':
                get_char = "อ"
                translate_text = translate_text + get_char
            elif str[i] == '1':
                get_char = "1"
                translate_text = translate_text + get_char
            elif str[i] == '2':
                get_char = "2"
                translate_text = translate_text + get_char
            elif str[i] == '3':
                get_char = "3"
                translate_text = translate_text + get_char
            elif str[i] == '4':
                get_char = "4"
                translate_text = translate_text + get_char
            elif str[i] == '5':
                get_char = "5"
                translate_text = translate_text + get_char
            elif str[i] == '6':
                get_char = "6"
                translate_text = translate_text + get_char
            elif str[i] == '7':
                get_char = "7"
                translate_text = translate_text + get_char
            elif str[i] == '8':
                get_char = "8"
                translate_text = translate_text + get_char
            elif str[i] == '9':
                get_char = "9"
                translate_text = translate_text + get_char
            elif str[i] == 'X':
                get_char = "10"
                translate_text = translate_text + get_char
            elif str[i] == 'c':
                if str[i+1] == 'Y':
                    get_char = "ๆ"
                    translate_text = translate_text + get_char
                    i += 1
                else:
                    get_char = "ำ"
                    translate_text = translate_text + get_char
                    i += 1
            elif str[i] == 'g':
                if str[i+1] == 'Y':
                    get_char = "่"
                    translate_text = translate_text + get_char
                    i += 1
                else:
                    get_char = "ะ"
                    translate_text = translate_text + get_char
                    i += 1
            elif str[i] == 'j':
                if str[i+1] == 'Y':
                    get_char = "้"
                    translate_text = translate_text + get_char
                    i += 1
                else:
                    get_char = "ุ"
                    translate_text = translate_text + get_char
                    i += 1
            elif str[i] == 'm':
                if str[i+1] == 'Y':
                    get_char = "๊"
                    translate_text = translate_text + get_char
                    i += 1
                else:
                    get_char = "เ"
                    translate_text = translate_text + get_char
                    i += 1
            elif str[i] == 'p':
                if str[i+1] == 'Y':
                    get_char = "๋"
                    translate_text = translate_text + get_char
                    i += 1
                else:
                    get_char = "์"
                    translate_text = translate_text + get_char
                    i += 1
            elif str[i] == 'b':
                    get_char = "็"
                    translate_text = translate_text + get_char
                    i += 1
            elif str[i] == 'f':
                    get_char = "า"
                    translate_text = translate_text + get_char
                    i += 1
            elif str[i] == 'i':
                    get_char = "ู"
                    translate_text = translate_text + get_char
                    i += 1
            elif str[i] == 'l':
                    get_char = "แ"
                    translate_text = translate_text + get_char
                    i += 1
            elif str[i] == 'o':
                    get_char = "ฤ"
                    translate_text = translate_text + get_char
                    i += 1
            elif str[i] == 'e':
                    get_char = "ั"
                    translate_text = translate_text + get_char
                    i += 1
            elif str[i] == 'a':
                    get_char = "ฯ"
                    translate_text = translate_text + get_char
                    i += 1
            elif str[i] == 'S':
                if str[i-1] == 'R':
                    i += 2
                    continue
                else:
                    get_char = "โ"
                    translate_text = translate_text + get_char
            elif str[i] == 'R':
                if str[i+1] == 'u':
                    get_char = "ิ"
                    translate_text = translate_text + get_char
                    i += 1
                elif str[i+1] == 'S':
                    get_char = "ึ"
                    translate_text = translate_text + get_char
                    i += 1
                elif str[i+1] == '2':
                    get_char = "ื"
                    translate_text = translate_text + get_char
                    i += 1
                else:
                    get_char = "ี"
                    translate_text = translate_text + get_char
            elif str[i] == 'T':
                if str[i+1] == 'L':
                    get_char = "จ"
                    translate_text = translate_text + get_char
                    i += 1
                else:
                    get_char = "ไ"
                    translate_text = translate_text + get_char
            elif str[i] == 'U':
                get_char = "ใ"
                translate_text = translate_text + get_char
            elif str[i] == 'd':
                get_char = "ๆ"
                translate_text = translate_text + get_char
            elif str[i] == 'h':
                get_char = "่"
                translate_text = translate_text + get_char
            elif str[i] == 'k':
                get_char = "้"
                translate_text = translate_text + get_char
            elif str[i] == 'n':
                get_char = "๊"
                translate_text = translate_text + get_char
            elif str[i] == 'q':
                get_char = "๋"
                translate_text = translate_text + get_char

        translate_text = re.sub(r'\d+', '', translate_text)
        return translate_text
