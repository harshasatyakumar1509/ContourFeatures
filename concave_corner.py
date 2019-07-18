import cv2
import matplotlib.pyplot as plt
import numpy as np

PATH = "/Users/sriharsha/Documents/Agricx/rice_defects/kStTn.jpg"


def create_tree(hierarchy):    
    ''' Creates high lever tree structure in a dictionary '''
    tree ={}
    for e, h in enumerate(hierarchy[0]):
        try:
            tree[h[3]].append(e)
        except:       
            tree[h[3]]=[e]
    return tree


def split_nodes(subtrees):
    leaf_nodes = []
    parent_nodes = []
    
    for key in subtrees:
        if key==-1:    
            leaf_nodes.extend(value for value in subtrees[key])
        else:
            parent_nodes.extend(value for value in subtrees[key])
            
    return leaf_nodes, parent_nodes


def reject_leaves(contours,subtree):
    
    leaves= list(subtree.values())[0]
    selected= []
    
    for leaf in leaves:
        if cv2.contourArea(contours[leaf])> 20:
            selected.append(leaf)
    return selected

def reject_parentnodes(subtrees, leaf_nodes_required):
    for i in leaf_nodes_required:
        if len(list(subtrees[i]))>2:
            leaf_nodes_required.remove(i)
    return leaf_nodes_required

def reject_leafnodes(subtrees, nodes_with_parents):
    #Reject the internal contours with no child (leaves) for clumping case
    
    parent_trees = []
    single_leaves = []
    #trees.append({-1:leaf_nodes_required})

    for sub_tree_nodes in nodes_with_parents:
        #print(sub_tree_nodes)
        try:
            parent_trees.append({sub_tree_nodes:subtrees[sub_tree_nodes]})
        except:
            single_leaves.append(sub_tree_nodes)
    
    return parent_trees

def draw_edges(contours,parent,indexes,b):
    cv2.drawContours(b, contours,parent, 255, cv2.FILLED)
    l=len(indexes)
    for i in indexes:
        #color= random.randint(100,240)
        #print(i,color)
      
        cv2.drawContours(b, contours,i, 0, cv2.FILLED) 
    return b


def draw_parent_contours(index,parent_nodes, contours, canvas):
    r=reject_leaves(contours,parent_nodes[index])
    canvas = draw_edges(contours,list(parent_nodes[index].keys())[0],r,canvas)
    return canvas


def concave_corner_points(image):
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY_INV)

    _, noisy_contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    noisy_contours = np.asarray(noisy_contours)

    test_canvas = np.zeros_like(thresh)

    tree_structure = create_tree(hierarchy)
    leaf_nodes, parent_nodes = split_nodes(tree_structure)
    leaf_nodes = reject_parentnodes(tree_structure, leaf_nodes)
    parent_nodes = reject_leafnodes(tree_structure, parent_nodes)

def get_corner_point(startpt, endpt, pairpoints):
    dist = []
    dist1 =[]
    dist2 = []
    #print(len(pairpoints))
    if pairpoints ==[]:
        return startpt
    if len(pairpoints)==1:
        return pairpoints[0]
    
    if len(pairpoints) >1:
        for pt in pairpoints:
            dist1.append(euclidean_distance(startpt, pt))
            dist2.append(euclidean_distance(endpt, pt))
        dist = [sum(i) for i in zip(dist1, dist2)] 
        index = dist.index(max(dist))
        #print(index)
        return(pairpoints[index]) 


def mid_corner_points(sel_contour, new_corner_points):
    start = None
    end = -1
    length = -1
    end = None
    list_of_points = []
    mid_corner_points = []

    for pt in sel_contour:

        if(tuple([pt[0][0],pt[0][1]]) in new_corner_points)==True:
            #print(tuple([pt[0][0],pt[0][1]]))
            if start == None:
                start = tuple([pt[0][0],pt[0][1]])
                length = 0
            else:
                length +=1
                list_of_points.append(tuple(pt[0]))

        elif(tuple([pt[0][0],pt[0][1]]) in new_corner_points)==False:
            if length >0:          
                length = -1
                end = tuple(prev[0])
                #print(start, end)
                list_of_points.remove(end)
                #print(list_of_points)
                mid_corner_points.append(get_corner_point(start, end, list_of_points))

                list_of_points = []
                start = None  
        prev = pt
    return(mid_corner_points)


def euclidean_distance(pt1, pt2):
    return(math.sqrt((pt2[1]-pt1[1])**2 + (pt2[0]-pt1[0])**2))

def get_continuous_point(corner_points, LP):
    new_corner_points = []
    for cpt in corner_points:
        for p in range(len(LP)):
            if euclidean_distance(cpt, [LP[p][0],LP[p][1]])<8:
                new_corner_points.append(tuple((LP[p][0],LP[p][1])))
    return new_corner_points


if __name__ == "__main__":
    img = cv2.imread(PATH)
    output = concave_corner_points(img)

