import cv2
import numpy as np

# Espacios iniciales definidos manualmente
espacio1 = [75, 215, 136, 128]
espacio2 = [40, 43, 88, 52]
espacio3 = [36, 346, 170, 189]
espacio4 = [194, 346, 158, 188]
espacio5 = [210, 214, 127, 129]
espacio6 = [199, 42, 87, 55]
espacio7 = [338, 328, 108, 208]
espacio8 = [357, 47, 84, 49]

# Lista de espacios iniciales
espacios = [espacio1, espacio2, espacio3, espacio4, espacio5, espacio6, espacio7,espacio8]

video = cv2.VideoCapture('video1.mp4')

# Lista para guardar las coordenadas marcadas por el usuario
puntos_marcados = []
espacios_personalizados = []  # Lista para guardar los espacios personalizados

# Función para manejar los clics del mouse y marcar las coordenadas
def marcar_punto(event, x, y, flags, param):
    global puntos_marcados, espacios_personalizados

    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Coordenadas marcadas: ({x}, {y})")
        puntos_marcados.append((x, y))
        # Dibuja un círculo en las coordenadas marcadas
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)

        # Cuando se marcan 4 puntos, se define un rectángulo y se guarda como nuevo espacio
        if len(puntos_marcados) == 4:
            x_min = min(puntos_marcados[0][0], puntos_marcados[1][0], puntos_marcados[2][0], puntos_marcados[3][0])
            y_min = min(puntos_marcados[0][1], puntos_marcados[1][1], puntos_marcados[2][1], puntos_marcados[3][1])
            x_max = max(puntos_marcados[0][0], puntos_marcados[1][0], puntos_marcados[2][0], puntos_marcados[3][0])
            y_max = max(puntos_marcados[0][1], puntos_marcados[1][1], puntos_marcados[2][1], puntos_marcados[3][1])
            nuevo_espacio = [x_min, y_min, x_max - x_min, y_max - y_min]
            espacios_personalizados.append(nuevo_espacio)
            print(f"Nuevo espacio marcado: {nuevo_espacio}")
            puntos_marcados = []  # Limpiar los puntos después de crear el espacio

# Asigna la función de callback para el mouse
cv2.namedWindow('video')
cv2.setMouseCallback('video', marcar_punto)

while True:
    check, img = video.read()

    if not check:
        break

    # Redimensionar el frame
    img = cv2.resize(img, (450, 800))

    # Conversión a escala de grises
    imgCinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Escala de Grises', imgCinza)

    # Aplicación de umbral adaptativo y desenfoque
    imgTh = cv2.adaptiveThreshold(imgCinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgBlur = cv2.medianBlur(imgTh, 5)
    cv2.imshow('Umbral Adaptativo y Desenfoque', imgBlur)

    # Dilatación de la imagen para resaltar características
    kernel = np.ones((3, 3), np.int8)
    imgDil = cv2.dilate(imgBlur, kernel)
    cv2.imshow('Dilatación', imgDil)

    cant_espacios_libres = 0

    # Analizar los espacios marcados automáticamente (predefinidos)
    for x, y, w, h in espacios + espacios_personalizados:  # Incluir los espacios personalizados
        recorte = imgDil[y:y + h, x:x + w]
        qtPxBlanco = cv2.countNonZero(recorte)
        cv2.putText(img, str(qtPxBlanco), (x, y + h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        if qtPxBlanco > 3000:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
        else:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cant_espacios_libres += 1

    # Mostrar los puntos marcados dinámicamente
    for punto in puntos_marcados:
        cv2.circle(img, punto, 5, (0, 255, 255), -1)

    # Mostrar la cantidad de espacios libres (más pequeño y en la parte inferior)
    height, width = img.shape[:2]
    text = f'Libres: {cant_espacios_libres}/{len(espacios)}'

    # Calcular el tamaño del texto para ajustar el rectángulo al contenido
    (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)

    # Ajustar el rectángulo al tamaño del texto
    cv2.rectangle(img, (10, height - 60), (10 + text_width + 20, height - 10), (255, 0, 0),
                  -1)  # Ajustar tamaño del rectángulo
    cv2.putText(img, text, (20, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Mostrar el video redimensionado
    cv2.imshow('video', img)

    if cv2.waitKey(10) & 0xFF == 27:  # Presiona ESC para salir
        break

video.release()
cv2.destroyAllWindows()