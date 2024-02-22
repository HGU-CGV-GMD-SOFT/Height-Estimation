import cv2
import math
from time import time

boxes = []

xCount = 0
yCount = 0
iter = 0
count = 0
def on_mouse(event, x, y, flags, params):
    global count
    global iter
    t = time()

    if  event == cv2.EVENT_LBUTTONDOWN:
        if count%2 ==0:
            print ('Start Mouse Position: '+str(x)+', '+str(y))
            sbox = [x, y]
            boxes.append(sbox)
            count += 1
        else:
            print ('End Mouse Position: '+str(x)+', '+str(y))
            ebox = [x, y]
            boxes.append(ebox)
            count +=1
            iter += 1
   
# 소실점(Vanishing Point) 계산
def line_intersection(line1, line2):
	
		# 각 선분의 방향을 결정. 이를 위해 각 선분의 두 점을 사용하여 방향 벡터를 계산
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) 

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]
	
		# 외적 계산. 외적은 두 벡터가 이루는 사변형의 크기를 의미함. 
		# 따라서 이 크기가 0이 되면 두 벡터가 평행하거나 겹치는 경우이기에 패스.
    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('Lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

# L2 norm(직선 거리 계산)
def norm(point1, point2):

    xdiff = point1[0] - point2[0]
    ydiff = point1[1] - point2[1]

    norm = math.sqrt(xdiff*xdiff + ydiff*ydiff)
    return norm

print ("-------------------------INSTRUCTIONS----------------------------")
print ("Draw 8 line segments, holding mouse while drawing")
print ("First two for xVanish")
print ("Next two for yVanish")
print ("Next two for objects whose lengths are to be compared")
print ("First draw for the shorter object in the image plane starting from bottom")
print ("Then for the other object again starting from bottom")
print ("Finally two for zVanish")
print ("-----------------------------END---------------------------------")

count = 0
while iter < 9:
    img = cv2.imread('input3.jpg', 1)
    img = cv2.resize(img, (720, 540))
    #img = cv2.resize(img, None, fx=0.8, fy=0.8)

    cv2.namedWindow('real image')
    cv2.setMouseCallback('real image', on_mouse, 0)

    # Draw lines on the image with different colors based on the current iteration
    for i in range(iter):
        if i < 2:
            color = (0, 0, 255)  # Red for xVanish
        elif 2 <= i < 4:
            color = (0, 255, 0)  # Green for yVanish
        elif 4 <= i < 6:
            color = (255, 0, 0)  # Blue for zVanish
        else:
            color = (0, 165, 255)  # Orange for object lines
        cv2.line(img, tuple(boxes[2 * i]), tuple(boxes[2 * i + 1]), color, 2)
        if iter==8:
            iter += 1

    cv2.imshow('real image', img)

    if cv2.waitKey(33) == 27:
        cv2.destroyAllWindows()
        break


# Calculate intersections and print results

# Vx
xVanish = line_intersection([boxes[0], boxes[1]], [boxes[2], boxes[3]])
print(f'xVanish: {xVanish}')

# Vy
yVanish = line_intersection([boxes[4], boxes[5]], [boxes[6], boxes[7]])
print(f'yVanish: {yVanish}')

# Vz
zVanish = line_intersection([boxes[8], boxes[9]], [boxes[10], boxes[11]])
print(f'zVanish: {zVanish}')

# [xVanish, yVanish] -- 소실선을 의미
# boxes[12] - obj bot(b0)
# vertex - V
vertex = line_intersection([xVanish, yVanish], [boxes[12], boxes[14]])
bot = boxes[14] # ref bot(b)
ref = line_intersection([vertex, boxes[13]], [boxes[14], boxes[15]])
top = boxes[15] # ref top(r)

response1 = float(input("Please enter the height of the shorter object, enter 0 if unknown: "))
response2 = float(input("Please enter the height of the other object, enter 0 if unknown: "))

response = response1 + response2

print("Length of the unknown object is:")
# L2 norm 계산
print((norm(top, bot) / norm(ref, bot)) * (norm(zVanish, ref) / norm(zVanish, top)) * response) # = H(object의 높이)

#cv2.destroyAllWindows()