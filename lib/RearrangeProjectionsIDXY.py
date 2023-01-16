import numpy as np
import os
import config
from os.path import exists

def RearrangeProjectionsIDXY(path_to_images, path_to_projections, prj_delimiter):
    
    # Make output directory
    os.mkdir('output/MarkerPrjsCOLMAP')
    images = os.listdir('{}'.format(path_to_images))

    # Load projections for each image
    for image in images:
        prj_path = '{}/{}.txt'.format(path_to_projections, image)
        if not exists(prj_path):
            #with open('output/MarkerPrjsCOLMAP/{}.jpg.txt'.format(image[:-4]),'w') as new_file:
            #    new_file.write('1 128\n')
            #    new_file.write('0 0 0 0')
            continue
        file = np.loadtxt(prj_path, dtype = float, delimiter = prj_delimiter, usecols = (1,2), ndmin = 2)
        
        # Export projections
        new_file = open('output/MarkerPrjsCOLMAP/{}.jpg.txt'.format(image[:-4]),'w')
        new_file.write('{} 128\n'.format(file.shape[0]))
        for k in range(0, file.shape[0]):
            file[k,0] = str(float(file[k,0])*config.image_reduction_factor+config.image_translation_vector_X)
            file[k,1] = str(float(file[k,1])*config.image_reduction_factor+config.image_translation_vector_Y)
            new_file.write('{} {} {} {}\n'.format(file[k,0], file[k,1], '0.000000', '0.000000'))
            
        new_file.close()
        
    