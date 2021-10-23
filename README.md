# Homography Calculation for two images

This repo is designed to compute the Homography matrix for two images with given correspondences. There are multiple ways in which we can compute correspondences between two images. 


Repo Structure:
* **normalized_homography**: Given correspondence, this code contains two methods of computing Homography. Method-1 is a standard method while, Method-2 first normalizes the points for stablility.

* **ransac**: Code for RANSAC algorithm. This code helps compute a robust Homography matrix.

* **panorama**: Code to create a panorama from multiple images. Note: for best resuts one should try to keep camera center fixed.


<p align="center">
  <img src="images/pano_left.png">
  <img src="images/pano_right.png">
  Visualization of the Image(Left) and it's corresponding wordmap
</p>

Assumptions:
1. The code assumes that point correspondence is already computed
_______
#### Notes
Major part of the code was developed as part of 16720 Intro to CV course at Carnegie Mellon University. This repo is under development.

To contact the author, feel free to write to paritosm@andrew.cmu.edu