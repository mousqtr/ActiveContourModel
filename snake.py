import numpy as np
import cv2
import scipy.sparse as ss
import matplotlib.pyplot as plt
import math
import sys

# Parametres ===========================================================================================================
alpha = 55
beta = 10
gamma = 0.4
t = 0
tlim = 2000
r = 100


# Lecture de limage ====================================================================================================
if len(sys.argv) != 2:
    print("Not enough argument")
    sys.exit(1)

img = cv2.imread(str(sys.argv[1]))
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   # Conversion de limage en niveaux de gris
plt.ion()
plt.figure(1)
plt.imshow(img)
plt.title("Image originale")
plt.show()


# Calcul des dimensions de limage
h = len(img)
w = len(img[0])


# Initialisation du snake ==============================================================================================
xcentre = w//2   # abscisses du centre du cercle
ycentre = h//2   # ordonnees du centre du cercle
N = 1000   # nombre de points du snake   # nombre de points
x_snake = [xcentre + r*math.cos(2*math.pi/(N - 1)*k) for k in range(N)]
y_snake = [ycentre + r*math.sin(2*math.pi/(N - 1)*k) for k in range(N)]


# Affichage de l'image avec le snake ===================================================================================
img_snake = np.copy(img)
for i in range(N):
    xi = x_snake[i]
    yi = y_snake[i]
    img_snake[int(yi)][int(xi)] = [255, 0, 0]

plt.ion()
plt.figure(2)
plt.imshow(img_snake)
plt.title("Image avec le snake")
plt.show()


# Calcul du gradient de l image ========================================================================================
sobelx = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=3)
# Calcul de la norme du gradient de l image
norme = [[math.sqrt(sobelx[i][j]**2+sobely[i][j]**2) for j in range(w)] for i in range(h)]

plt.ion()
plt.figure(3)
plt.subplot(2, 2, 1), plt.imshow(sobelx, cmap='gray'), plt.title("gradient horizontale")
plt.subplot(2, 2, 2), plt.imshow(sobely, cmap='gray'), plt.title("Gradient verticale")
plt.subplot(2, 2, 3), plt.imshow(norme, cmap='gray'), plt.title("Norme du gradient")
plt.show()

# Calculde lenergie de l image =========================================================================================
Eimage = [[norme[i][j]**2 for j in range(w)] for i in range(h)]

plt.ion()
plt.figure(4)
plt.imshow(Eimage, cmap='gray')
plt.title("Norme de l'energie de l'image")
plt.show()

# Calcul de l energie externe ==========================================================================================
Eext = 0
for i in range(N):
    xi = int(x_snake[i])
    yi = int(y_snake[i])
    Eext += Eimage[yi][xi]
#print('Energie externe = ' + str(Eext))


# Calculdu gradient de Eimage ==========================================================================================
Eimage = np.asarray(Eimage)
Eimage = Eimage/Eimage.max()
grad_Eimage_x = cv2.Sobel(Eimage, cv2.CV_64F, 1, 0, ksize=3)
grad_Eimage_y = cv2.Sobel(Eimage, cv2.CV_64F, 0, 1, ksize=3)

plt.ion()
plt.figure(5)
plt.subplot(1, 2, 1), plt.imshow(grad_Eimage_x, cmap='gray'), plt.title("gradient horizontal de l'energie de l'image")
plt.subplot(1, 2, 2), plt.imshow(grad_Eimage_y, cmap='gray'), plt.title("gradient vertical de l'energie de l'image")
plt.show()

# Calculde la matrice A ================================================================================================
D2 = ss.diags([1, 1, -2, 1, 1], [-N + 1, -1, 0, 1, N - 1], shape=(N, N)).toarray()
D4 = ss.diags([-4, 1, 1, -4, 6, -4, 1, 1, -4], [-N + 1, -N + 2, -2, -1, 0, 1, 2, N - 2, N - 1], shape=(N, N)).toarray()
D = alpha*D2 - beta*D4
Id = ss.diags([1], [0], shape=(N, N)).toarray()
A = np.linalg.inv(Id - D)


# Deplacement du snake =================================================================================================
plt.ion()
plt.figure(6)
Plotfig = plt.imshow(img)
plt.title("Image avec le snake evoluant")
while t < tlim:
    for i in range(N):
        xi = x_snake[i]
        yi = y_snake[i]
        img[int(yi)][int(xi)] = [0, 0, 223]

    for i in range(N):
        # Copie des coordonnees d un point du snake de l instant t-1
        xi = x_snake[i]
        yi = y_snake[i]
        # Utilisation de la formule du cours
        x_snake[i] = (xi + gamma*grad_Eimage_x[int(yi)][int(xi)])
        y_snake[i] = (yi + gamma*grad_Eimage_y[int(yi)][int(xi)])
    t += 1
    x_snake = np.around(np.dot(A, x_snake))
    y_snake = np.around(np.dot(A, y_snake))

    # Affichage du snake a l instant t
    for i in range(N):
        xi = x_snake[i]
        yi = y_snake[i]
        img[int(yi)][int(xi)] = [100, 167, 255]
    Plotfig.set_data(img)
    plt.show()
    plt.pause(0.0001)


# Calcul de l energie externe ==========================================================================================
Eext = 0
for i in range(N):
    xi = int(x_snake[i])
    yi = int(y_snake[i])
    Eext += Eimage[yi][xi]
print('Energie externe = ' + str(Eext))
