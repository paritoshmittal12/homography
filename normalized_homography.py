'''
This code was developed as part of the 16-720 (A) course
at Carnegie Mellon University.
'''

import numpy as np

'''
This variable is an epsilon value added while 
dividing to avoid division with 0
'''
eps = 1e-6

'''
The following code is used to compute homography 
between 2 sets of corresponding point pairs
The homography matrix that is calculated is 
best in least square sense.
'''
def computeH(locs1, locs2):
    '''
    Args:
    locs1 : [x,y] corresponding points for first image
    locs2 : [x,y] corresponding points for second image
    '''

    # Compute the homography between two sets of points

    # Create the combined matrix A
    A = []
    for i in range(len(locs1)):
        ith1_row = [-locs2[i][0],-locs2[i][1],-1,0,0,0,\
        locs1[i][0]*locs2[i][0],locs1[i][0]*locs2[i][1],locs1[i][0]]
        A.append(ith1_row)
        ith2_row = [0,0,0,-locs2[i][0],-locs2[i][1],-1,\
        locs1[i][1]*locs2[i][0],locs1[i][1]*locs2[i][1],locs1[i][1]]
        A.append(ith2_row)
    
    A = np.matrix(A)
    
    # Calculate the SVD for matrix A
    u,s,v_transpose = np.linalg.svd(A)
    
    # Homogrphy corresponds to the last column of v or
    # last row (here) of v transpose 
    H_col = v_transpose[8]
    
    # Normalize so that H[2,2] = 1
    H_col = (1/(H_col.item(8)+eps)) * H_col
    
    # Resize to 3x3 matrix
    H2to1 = np.reshape(H_col,(3,3))

    return H2to1

'''
This method is used to compute normalized
homography. We translate and scale that data
such that mean is 0 and max value is 1.
Linear transformation matrices are also computed
'''
def computeH_norm(locs1, locs2):
    '''
    Args:
    locs1 : [x,y] corresponding points for first image
    locs2 : [x,y] corresponding points for second image
    '''
    
    # Compute the centroid of the points
    t_locs1_xmean,t_locs1_ymean = np.mean(locs1,axis=0)
    t_locs2_xmean,t_locs2_ymean = np.mean(locs2,axis=0)
    
    # Shift the origin of the points to the centroid
    t_locs1 = locs1 - np.array([t_locs1_xmean,t_locs1_ymean]) 
    t_locs2 = locs2 - np.array([t_locs2_xmean,t_locs2_ymean]) 
    
    # Normalize the points so that the largest distance from the
    # origin is equal to sqrt(2)
    
    t_scale1_x, t_scale1_y = np.abs(t_locs1).max(axis=0)
    t_scale2_x, t_scale2_y = np.abs(t_locs2).max(axis=0)
    
    t_scale1_x, t_scale1_y = (t_scale1_x+eps)**-1, (t_scale1_y+eps)**-1
    t_scale2_x, t_scale2_y = (t_scale2_x+eps)**-1, (t_scale2_y+eps)**-1
    
    t_locs1 = t_locs1 * np.array([t_scale1_x,t_scale1_y])
    t_locs2 = t_locs2 * np.array([t_scale2_x,t_scale2_y])
    
    
    # Similarity transform 1
    T1 = np.array([[t_scale1_x,0,-t_scale1_x*t_locs1_xmean],[0,t_scale1_y,\
        -t_scale1_y*t_locs1_ymean],[0,0,1]])
    
    # Similarity transform 2
    T2 = np.array([[t_scale2_x,0,-t_scale2_x*t_locs2_xmean],[0,t_scale2_y,\
        -t_scale2_y*t_locs2_ymean],[0,0,1]])
    
    # Compute homography
    normalized_H2to1 = computeH(t_locs1,t_locs2)
    
    # Denormalization
    H2to1 = np.dot(np.linalg.inv(T1),np.dot(normalized_H2to1,T2))
    H2to1 *= ((H2to1[2,2]+eps)**-1)

    return H2to1