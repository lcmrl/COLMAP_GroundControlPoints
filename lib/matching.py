import numpy as np
import os
import config
from os.path import exists

def Matching(path_to_images, path_to_projections, prj_delimiter):
    images = os.listdir('{}'.format(path_to_images))
    projections = os.listdir('{}'.format(path_to_projections))
    file_matches = open('output/matches.txt', 'w')
    raw_matches = []
    all_matches = {}
    control = True
    
    # Match images using the ID in the projection files
    for image1_count in range(0, len(images)-1):
        if not exists('{}/{}.txt'.format(path_to_projections, images[image1_count])):
            continue
        image1_kps = np.loadtxt('{}/{}.txt'.format(path_to_projections, images[image1_count]), delimiter = prj_delimiter, usecols = (0,1,2), ndmin = 2, dtype=str)
    
        for image2_count in range(image1_count+1, len(images)):
            if not exists('{}/{}.txt'.format(path_to_projections, images[image2_count])):
                continue
            image2_kps = np.loadtxt('{}/{}.txt'.format(path_to_projections, images[image2_count]), delimiter = prj_delimiter, usecols = (0,1,2), ndmin = 2, dtype=str)
            
            # Initialize a new matches_matrix to store possible matches on current image couple
            matches_matrix = np.array(['{}.jpg'.format(images[image1_count][:-4]), '{}.jpg'.format(images[image2_count][:-4])])
            if config.INFO == False:
                print('Matching images: ', images[image1_count], images[image2_count], end='\r')
            elif config.INFO == True:
                print('Matching images: ', images[image1_count], images[image2_count])
            
            # Check if valid matches exist
            for k in range(0, image1_kps.shape[0]):
                for j in range(0, image2_kps.shape[0]):
                    if image1_kps[k, 0] == image2_kps[j, 0]:
                        other_match = np.array([k, j])
                        matches_matrix = np.vstack((matches_matrix, other_match))
                        all_matches[(images[image1_count][:-4], images[image2_count][:-4])] = matches_matrix[1:,:]
            
            raw_matches.append(matches_matrix)
            if config.INFO == True:
                print(matches_matrix)
        
        # Export matches to file
        for item in raw_matches:     
            for i in range(0, item.shape[0]):
                try:
                    file_matches.write("%s %s\n" % (item[i, 0], item[i, 1]))
                    control = True
                except:
                    #print("An exception occurred")
                    control = False
            if control == True: file_matches.write('\n')
        
        raw_matches = []
        
    file_matches.close()       
    return all_matches
    