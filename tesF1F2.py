import cv2
import numpy as np
import Functions_1 as F1

BoardSize=[757,508] #unit in mm
PieceMat=[6,4] 
PuzzlePCNT=24
edgenum=2*sum(PieceMat)
PuzzleSize=[284,220] #unit in mm
avgSize=int(np.ceil(PuzzleSize[0]*PuzzleSize[1]/float(PuzzlePCNT)))
print 'avgSize '+str(avgSize)

filename = 'img.jpg'

img_ori=cv2.imread(filename)

img = cv2.cvtColor(img_ori,cv2.COLOR_BGR2GRAY)


# looking for straight lines


edges = cv2.Canny(img,100,200)
cv2.imshow('frame',edges)
k=cv2.waitKey(0) & 0xff
if k==27:
	cv2.destroyAllWindows()

area=[]
indmax=0
maxarea=0
contours = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
for h, cnt in reversed(list(enumerate(contours))):
	areah=int(np.ceil(cv2.contourArea(cnt)))
	area.append(areah)
	if areah>=max(area):
		maxarea=areah
		indmax=h
border=contours[indmax]
epsilon = 0.1*cv2.arcLength(border,True)
border = cv2.approxPolyDP(border,epsilon,True)

hull= cv2.convexHull(border,True)

print 'max at '+str(indmax)
print 'max area '+ str(maxarea)
print 'contour count'+ str(len(area))

cv2.drawContours(img,[border],0,[0,0,0],2)

cv2.imshow('frame',img)
k=cv2.waitKey(0) & 0xff
if k==27:
    cv2.destroyAllWindows()
print hull
# hull are the cordinates of the four corners

img_C=F1.Perspective_Transform(img_ori, hull )

cv2.imshow('frame',img_C)
k=cv2.waitKey(0) & 0xff
if k==27:
    cv2.destroyAllWindows()

img_C=F1.Perspective_Correction(img_ori,BoardSize)
cv2.imwrite('c.jpg',img_C)
edgesC=cv2.Canny(img_C,1,200)
cv2.imshow('frame',edgesC)
k=cv2.waitKey(0) & 0xff
if k==27:
	cv2.destroyAllWindows()
img_B = F1.Clear_Background(img_C)

img_BIN = F1.Binarise(img_B)


img_DP, piece_cnt, overlap_cnt = F1.Detect_Pieces(img_BIN, img_C, avgSize,PuzzlePCNT)
F1.showimg(img_DP)

img_DC = np.copy(img_C)

