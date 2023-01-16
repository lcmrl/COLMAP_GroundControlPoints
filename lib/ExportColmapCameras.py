# Pyquaternion installation with Anaconda
# conda install -c krande pyquaternion
# USAGE: python ExportColmapCameras.py -i .\images.txt -o .\outs

import argparse
import numpy as np
from pyquaternion import quaternion
from scipy.spatial.transform import Rotation as R
from scipy import linalg
import matplotlib.pyplot as plt

print("Exporting cameras ...")

def ExportCameras(external_cameras_path):
    lines= []
    lines.append("IMAGE_ID X Y Z NX NY NZ FOCAL_LENGTH EULER_ROTATION_MATRIX\n")
    d = {}
    k = 0
    n_images = 0
    
    with open(external_cameras_path,'r') as file :
        for line in file:
            k = k+1
            line = line[:-1]
            try:
                first_elem, waste = line.split(' ', 1)
                if first_elem == "#":
                    print(first_elem)
                elif k%2 != 0:
                    image_id, qw, qx, qy, qz, tx, ty, tz, camera_id, name = line.split(" ", 9)
                    q = np.array([float(qw), float(qx), float(qy), float(qz)])
                    t = np.array([[float(tx)],[float(ty)],[float(tz)]])
                    q_matrix = quaternion.Quaternion(q).transformation_matrix
                    q_matrix = q_matrix[0:3,0:3]
                    camera_location = np.dot(-q_matrix.transpose(),t)
                    n_images = n_images + 1
                    camera_direction = np.dot(q_matrix.transpose(),np.array([[0],[0],[1]]))#*-1
                    lines.append('{} {} {} {} {} {} {} 50 {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(
                                                name,
                                                camera_location[0,0],
                                                camera_location[1,0],
                                                camera_location[2,0],
                                                camera_direction[0,0],
                                                camera_direction[1,0],
                                                camera_direction[2,0],
                                                q_matrix[0,0],
                                                q_matrix[0,1],
                                                q_matrix[0,2],
                                                "0",
                                                q_matrix[1,0],
                                                q_matrix[1,1],
                                                q_matrix[1,2],
                                                "0",
                                                q_matrix[2,0],
                                                q_matrix[2,1],
                                                q_matrix[2,2],
                                                "0",
                                                "0",
                                                "0",
                                                "0",
                                                "1"
                                                ))
        
            except:
                print("Empty line")
    return lines
    
def main():
    # I/O management
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--Input", help = "Input the path to COLMAP images.txt")
    parser.add_argument("-o", "--Output", help = "Output folder")
    args = parser.parse_args()

    if args.Input:
        print("Input: % s" % args.Input)
    if args.Output:
        print("Output: % s" % args.Output)
    
    external_cameras_path = args.Input
    output_dir = args.Output
    
    camera_ori = ExportCameras(external_cameras_path)
    
    out_file = open(r"{}/ssssssssssssss.txt".format(output_dir), 'w')
    for element in camera_ori:
        out_file.write(element)
        out_file.write('\n')
    out_file.close()

# DRIVER FUNCTION 
if __name__=="__main__": 
    main()