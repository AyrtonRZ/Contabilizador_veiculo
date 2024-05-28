import cv2
import numpy as np
from time import sleep
from constantes import *

def pega_centro(x, y, largura, altura):
    """
    Calcula o centro de um retângulo.
    
    :param x: Coordenada x do canto superior esquerdo do retângulo
    :param y: Coordenada y do canto superior esquerdo do retângulo
    :param largura: Largura do retângulo
    :param altura: Altura do retângulo
    :return: Tupla com as coordenadas do centro do retângulo
    """
    cx = x + largura // 2
    cy = y + altura // 2
    return cx, cy

def set_info(detec, frame1):
    global carros
    for (x, y) in detec:
        if (pos_linha + offset) > y > (pos_linha - offset):
            carros += 1
            cv2.line(frame1, (25, pos_linha), (1200, pos_linha), (0, 127, 255), 3)
            detec.remove((x, y))
            print(f"Carros detectados até o momento: {carros}")

def show_info(frame1):
    text = f'Carros: {carros}'
    cv2.putText(frame1, text, (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
    cv2.imshow("Video", frame1)

def main():
    global carros, detec
    carros = 0
    detec = []

    cap = cv2.VideoCapture('video.mp4')
    subtracao = cv2.bgsegm.createBackgroundSubtractorMOG()

    while cap.isOpened():
        ret, frame1 = cap.read()
        if not ret:
            break

        tempo = float(1 / delay)
        sleep(tempo)

        grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grey, (3, 3), 5)
        img_sub = subtracao.apply(blur)
        dilat = cv2.dilate(img_sub, np.ones((5, 5), np.uint8))
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
        dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)

        contorno, _ = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.line(frame1, (25, pos_linha), (1200, pos_linha), (255, 127, 0), 3)

        for c in contorno:
            (x, y, w, h) = cv2.boundingRect(c)
            validar_contorno = (w >= largura_min) and (h >= altura_min)
            if not validar_contorno:
                continue

            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            centro = pega_centro(x, y, w, h)
            detec.append(centro)
            cv2.circle(frame1, centro, 4, (0, 0, 255), -1)

        set_info(detec, frame1)
        show_info(frame1)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
