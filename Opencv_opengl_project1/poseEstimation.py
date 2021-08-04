

import pickle
import numpy as np
import cv2 as cv
from pathlib import Path


# def draw(img, corners, imgpts):
#     corner = tuple(corners[0].ravel())
#     img = cv.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
#     img = cv.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
#     img = cv.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
#     return img

def draw(img, corners, imgpts):
    imgpts = np.int32(imgpts).reshape(-1,2)
    # draw ground floor in green
    img = cv.drawContours(img, [imgpts[:4]],-1,(0,255,0),-3)
    # draw pillars in blue color
    for i,j in zip(range(4),range(4,8)):
        img = cv.line(img, tuple(imgpts[i]), tuple(imgpts[j]),(0,0,255),3)
    # draw top layer in red color
    img = cv.drawContours(img, [imgpts[4:]],-1,(0,0,255),3)
    return img

if __name__ == '__main__':

	dataPath = Path("./chessboardPictures").resolve()

	#Load camera calibration
	with open('params.pickle', 'rb') as f1:
		data = pickle.load(f1)
		_, mtx, dist, _, _ = data


	criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
	objp = np.zeros((9*6,3), np.float32)
	objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)
	
	# axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)
	#Rectangle 1
	axis1 = np.float32([[0,0,0], [0,3,0], [3,3,0], [3,0,0], [0,0,-3],[0,3,-3],[3,3,-3],[3,0,-3] ])
	#Rectangle 2
	axis2 = np.float32([[1,1,0], [0,3,0], [2,2,0], [3,0,0], [1,1,-3],[0,3,-3],[2,2,-3],[3,0,-3] ])

	axis3 = np.float32([[1+4, 1+4, 0], [0+4, 3+4, 0], [2+4, 2+4, 0], [3+4, 0+4, 0], [1+4, 1+4, -3], [0+4, 3+4, -3], [2+4, 2+4, -3], [3+4, 0+4, -3]])

	axis = axis2
	for fname in dataPath.glob('*.jpg'):
		fname = str(fname)
		img = cv.imread(fname)
		img_orig = img.copy()
		gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
		ret, corners = cv.findChessboardCorners(gray, (9,6),None)
		
		if ret == True:
			corners2 = cv.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
			# Find the rotation and translation vectors.
			ret,rvecs, tvecs = cv.solvePnP(objp, corners2, mtx, dist)
			# project 3D points to image plane
			imgpts, jac = cv.projectPoints(axis, rvecs, tvecs, mtx, dist)

			imgpts2, jac = cv.projectPoints(axis3, rvecs, tvecs, mtx, dist)
			img = draw(img,corners2,imgpts)
			img = draw(img, corners2, imgpts2)

			final_frame = np.hstack((img_orig,img))
			cv.imshow('img', final_frame)
			k = cv.waitKey(0) & 0xFF
			if k == ord('s'):
			    cv.imwrite(fname[:6]+'.png', img)

	cv.destroyAllWindows()