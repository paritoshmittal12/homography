'''
This code was developed as part of the 16-720 (A) course
at Carnegie Mellon University.
'''

import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys
sys.path.append('../python')


from ransac import computeH_ransac


'''
This method is used to create a panorama 
that stitches the two left and right frames
We try to capture frames that are only 
separated by pure rotation
'''
def make_panaroma(pano_left,pano_right):
    # We first extract the matches from the left and right images
    
    '''
    Important: 
    Use feature extractors and descriptors (Harris + SIFT etc.) 
    to find correspondences between left and right images

    locs1: [x,y]  points in left image
    locs2: [x,y]  points in right image
    matches: index array denoting the correspondence between two images
    '''
    
    
    # Find corresponding pairs among all corner points
    t_locs1 = locs1[matches[:,0]]
    t_locs2 = locs2[matches[:,1]]
    
    t_locs1 = t_locs1[:,::-1]
    t_locs2 = t_locs2[:,::-1]
    
    # Compute the homography matrix that maps left to right
    H2to1,_ = computeH_ransac(t_locs2,t_locs1)

    rows_left, cols_left = pano_left.shape[:2]
    rows_right, cols_right = pano_right.shape[:2]

    # We find the boundary points of left image
    # We will use this to (a) calculate the final width of 
    # composite panorama, (b) to calculate the mask used 
    # for adding the images and (c) to calculate the translation
    left_points = np.array([[0,0,1],[0,rows_left,1],[cols_left,rows_left,1]\
        ,[cols_left,0,1]])

    # We project these points in the space of right image
    # If the boundary is projected in negative space then
    # we need to increase the size of final image
    # inorder to include this part of image
    left_transformed_points = np.dot(H2to1,left_points.T)
    left_transformed_points = np.int32(left_transformed_points / \
        left_transformed_points[2,:])
    left_transformed_points = left_transformed_points[:2].T
    
    # Since the images are separated by pure rotation we only account
    # for change in width and not for change in height
    w_max = np.maximum(left_transformed_points.max(axis=0)[0,0],cols_right)
    w_min = np.minimum(left_transformed_points.min(axis=0)[0,0],0)

    # When we warp the left image into the final panorama, the center
    # of left image also needs to be translated. This ensures that
    # entire left image will be part of the panorama. Because all
    # these transformations can we achieved using matrix multiplication
    # we can use T * H as the final matrix to perform this transformation
    left_translation_matrix = np.array([[1,0,-w_min],[0,1,0],[0,0,1]])
    
    pano_left_warped = cv2.warpPerspective(pano_left,np.dot(\
        left_translation_matrix,H2to1),(w_max-w_min, rows_right))
    
    # The final panorama image is initialized to 0
    composite_panorama = np.zeros((rows_right,w_max-w_min,3),np.uint8)
    # We fill the right side of the image with pixels from pano_right image
    composite_panorama[:,-w_min:-w_min+cols_right] = pano_right
    
    # We transform the boundary points to find the projected boundary
    # of the left image used for mask
    left_transformed_points = np.dot(np.dot(\
        left_translation_matrix,H2to1),left_points.T)
    left_transformed_points = np.int32(\
        left_transformed_points / left_transformed_points[2,:])
    left_transformed_points = left_transformed_points[:2].T
    
    composite_panorama = cv2.fillPoly(composite_panorama,\
        [left_transformed_points],[0,0,0])
    
    # We create the final composite image
    composite_panorama = cv2.add(pano_left_warped, composite_panorama)
    return composite_panorama


def main():
    
    pano_left = cv2.imread('./pano_left.jpeg')
    pano_left = cv2.cvtColor(pano_left,cv2.COLOR_BGR2RGB)
    pano_right = cv2.imread('./pano_right.jpeg')
    pano_right = cv2.cvtColor(pano_right,cv2.COLOR_BGR2RGB)
    panorama = make_panaroma(pano_left,pano_right,opts)
    
    cv2.imwrite('./panorama.png',cv2.cvtColor(\
        panorama,cv2.COLOR_BGR2RGB))

if __name__ == "__main__":
	main()