# Concave corner points

The repo contains the code for this paper
https://www.researchgate.net/publication/251980057_An_automatic_segmentation_algorithm_for_touching_rice_grains_images

#Description

Concave point essentially describes the geometry of any contour in opencv
This paper helper me to create a customized algorithm for detecting concavity of a shape

I referred to several algorithms for concavity, which mostly deals with angle of deviation and bending energy
which is very difficult to find with noisy contours.

The algorithm in the paper is very robust, particularly dealing with noisy contours.  

#Packages required

I used networkx graph for easy access of contour points
https://networkx.github.io/documentation/networkx-1.10/
