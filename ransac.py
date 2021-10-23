'''
This code was developed as part of the 16-720 (A) course
at Carnegie Mellon University.
'''
import numpy as np
from normalized_homography import *


'''
We calculate the eucledian distance between
true and projected points to identify inliers
'''
def calculate_distance(points1,points2,h):

    points2 = np.array([points2[0],points2[1],1]).T

    est1 = np.dot(h,points2).T
    est1 /= (est1[2]+eps)

    error = np.sqrt((est1[0]-points1[0])**2 + (est1[1]-points1[1])**2)
    return error

'''
This method runs the RANSAC algorithm to find 
best homography matrix that is robust towards
outliers
'''
def computeH_ransac(locs1, locs2):
    
    # Compute the best fitting homography given 
    # a list of matching points

    # the number of iterations to run RANSAC for
    max_iters = 

    # the tolerance value for considering a point to be an inlier
    inlier_tol = 
    best_H2to1 = None 
    best_inliers = np.zeros(len(locs1))
    max_inliers = -1

    for run in range(0,max_iters):
        curr_inliers = 0
        inliers = np.zeros(len(locs1))
        random_points = np.random.randint(0,len(locs1),4)
        t_locs1 = locs1[random_points]
        t_locs2 = locs2[random_points]
        cand_H = computeH_norm(t_locs1,t_locs2)
        #check for inliers
        for i in range(len(locs1)):
            error = calculate_distance(locs1[i],locs2[i],cand_H)
            if error <= inlier_tol:
                inliers[i] = 1
                curr_inliers += 1
        if curr_inliers > max_inliers:
            best_H2to1 = cand_H
            max_inliers = curr_inliers
            best_inliers = inliers
    return best_H2to1, best_inliers
