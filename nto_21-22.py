from cv2 import cv2
from math import atan2, cos, sin, sqrt, pi, atan
import numpy as np


def drawAxis(img, p_, q_, color, scale):
    p = list(p_)
    q = list(q_)
    ## [visualization1]
    angle = atan2(p[1] - q[1], p[0] - q[0])  # angle in radians
    hypotenuse = sqrt((p[1] - q[1]) * (p[1] - q[1]) + (p[0] - q[0]) * (p[0] - q[0]))
    # Here we lengthen the arrow by a factor of scale
    q[0] = p[0] - scale * hypotenuse * cos(angle)
    q[1] = p[1] - scale * hypotenuse * sin(angle)
    cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)
    # create the arrow hooks
    p[0] = q[0] + 9 * cos(angle + pi / 4)
    p[1] = q[1] + 9 * sin(angle + pi / 4)
    cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)
    p[0] = q[0] + 9 * cos(angle - pi / 4)
    p[1] = q[1] + 9 * sin(angle - pi / 4)
    cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), color, 3, cv2.LINE_AA)


## [visualization1]
def getOrientation(pts, img):
    ## [pca]
    # Construct a buffer used by the pca analysis
    sz = len(pts)
    data_pts = np.empty((sz, 2), dtype=np.float64)
    for i in range(data_pts.shape[0]):
        data_pts[i, 0] = pts[i, 0, 0]
    data_pts[i, 1] = pts[i, 0, 1]
    # Perform PCA analysis
    mean = np.empty((0))
    mean, eigenvectors, eigenvalues = cv2.PCACompute2(data_pts, mean)
    # Store the center of the object
    cntr = (int(mean[0, 0]), int(mean[0, 1]))
    ## [pca]
    ## [visualization]
    # 119
    # Draw the principal components
    cv2.circle(img, cntr, 3, (255, 0, 255), 2)
    p1 = (
        cntr[0] + 0.02 * eigenvectors[0, 0] * eigenvalues[0, 0],
        cntr[1] + 0.02 * eigenvectors[0, 1] * eigenvalues[0, 0])
    p2 = (
        cntr[0] - 0.02 * eigenvectors[1, 0] * eigenvalues[1, 0],
        cntr[1] - 0.02 * eigenvectors[1, 1] * eigenvalues[1, 0])
    drawAxis(img, cntr, p1, (255, 255, 0), 1)
    drawAxis(img, cntr, p2, (0, 0, 255), 5)
    angle = atan2(eigenvectors[0, 1], eigenvectors[0, 0])  # orientation in radians
    ## [visualization]
    # Label with the rotation angle
    label = " Rotation Angle: " + str(-int(np.rad2deg(angle)) - 90) + " degrees"
    textbox = cv2.rectangle(img, (cntr[0], cntr[1] - 25), (cntr[0] + 250, cntr[1] + 10), (255, 255, 255), -1)
    cv2.putText(img, label, (cntr[0], cntr[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    return angle, cntr


# Load the image
# color definition
red_lower = np.array([0, 200, 160], dtype="uint8")
red_upper = np.array([20, 255, 255], dtype="uint8")
red_lower_v = np.array([235, 120, 150], dtype="uint8")
red_upper_v = np.array([255, 255, 255], dtype="uint8")
# Main cycle
img = cv2.imread('source.png')
# Normalize image brightness
cv2.normalize(img, img, 0, 255, cv2.NORM_MINMAX)
# Blur the image to reduce noise
blur = cv2.medianBlur(img, 5)
# Convert BGR to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# Find color masks
red3_mask = cv2.inRange(hsv, red_lower, red_upper)
red2_mask = cv2.inRange(hsv, red_lower_v, red_upper_v)
# white_mask = cv2.inRange(hsv, white_lower, white_upper)
full_mask = red2_mask + red3_mask
# full_mask = white_mask
# cv2.imwrite("deb.png", full_mask)
# Find counters
contours, hierarchy = cv2.findContours(full_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
# img = full_mask
# for i, c in enumerate(contours):
comb = contours[0].copy()
for i in range(1, len(contours)):
    comb = np.concatenate((comb, contours[i]))
# print(comb)
c = comb
i = 0
# Calculate the area of each contour
area = cv2.contourArea(c)
# Ignore contours that are too small or too large
# 120
# if area < 220 or 100000 < area:
# continue
# Draw each contour only for visualisation purposes
cv2.drawContours(img, contours, i, (0, 200, 0), 2)
# Find the orientation of each shape
alpha, cntr = getOrientation(c, img)
alpha = -alpha - pi / 2.0
lx = 5.8
ly = 3.4
x0 = 527.40
z0 = 467.70
xuav = 520.80
zuav = 473.72
h = 41
psi = 29.99 * pi / 180
lxx = sqrt(lx ** 2 + 1) + sqrt(0.5 ** 2 + 0.5 ** 2)
# print(0.5*1.4)
# alpha = alpha + atan2(1, lx)
cx = []
cy = []
for el in c:
    cx.append(el[0][0])
    cy.append(el[0][1])
# print(cx)
dpx = max(cx) - min(cx)
dpy = max(cy) - min(cy)  # vertical
print("Object rotation angle: {:.2f}".format(alpha * 180 / pi))
dx = abs(lxx * cos(alpha))  # vertical
dz = abs(lxx * sin(alpha))
print("pixel {}, meters {}".format(dpx, dz))
print("pixel {}, meters {}".format(dpy, dx))
height, width, channels = img.shape
pixel_height = dx / dpy
pixel_width = dz / dpx
print("Pixel height: {}, width: {}".format(pixel_height, pixel_width))
center_dx = cntr[0] - width / 2  # right
center_dy = height / 2 - cntr[1]  # up
print("Center shift hor: {}, ver: {}".format(center_dx, center_dy))
vect = [center_dy * pixel_height, center_dx * pixel_width]
print("Displacement in body frame X: {:.2f}, Z: {:.2f}".format(vect[0], vect[1]))
v2 = [1, 0]
# psi = 45 * pi / 180
v2[0] = vect[0] * cos(psi) - vect[1] * sin(psi)
v2[1] = +vect[0] * sin(psi) + vect[1] * cos(psi)
print("Actual displacement X: {:.2f}, Z: {:.2f}".format(v2[0], v2[1]))
print("Solution X: {:.2f}, Z: {:.2f}".format(xuav + v2[0], zuav + v2[1]))
print("Solutuion error: {:.2f} (X: {:.2f}, Z: {:.2f})".format(sqrt((xuav + v2[0] - x0) ** 2 + (zuav + v2[1] - z0) ** 2),
                                                              xuav + v2[0] - x0, zuav + v2[1] - z0))
cv2.imshow('Output Image', img)
cv2.imwrite("sol_2.png", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
