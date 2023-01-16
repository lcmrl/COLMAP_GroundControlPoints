### TARGET TRIANGULATION
### 3DOM - FBK - TRENTO - ITALY
# Main
# Please, change the input directories with yours in the config.py file.

print('\nTARGET TRIANGULATION')

# Importing libraries
print('\nImporting libraries ...')
import cv2
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import os
import shutil
import subprocess

# Importing other scripts
print('Importing other scripts ...\n')
import config
from lib import RearrangeProjectionsIDXY
from lib import matching
from lib import checks
from lib import database
from lib import read_existing_db
from lib import ExportColmapCameras

# Define the class to store the triangulated targets in COLMAP as objects
class target3D:
    def __init__(self, t3D_id, x, y, z, r, g, b, error, track):
        self.t3D_id = t3D_id
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.g = g
        self.b = b
        self.error = error
        self.track = track

##################################################################################
# MAIN STARTS HERE
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
else:
    shutil.rmtree(output_dir)           
    os.makedirs(output_dir)

# Print input directories
print("N of images: \t\t\t{}".format(len(os.listdir(config.image_folder))))
print("Image folder: \t\t\t{}".format(config.image_folder))
print("Projections folder: \t\t{}".format(config.projection_folder))
print("Sparse model: \t\t\t{}".format(config.sparse_model_path))
print("Projection reduction factor: \t{}".format(config.image_reduction_factor))
print("Projection delimiter: \t\t'{}'".format(config.projection_delimiter))
print("Show more info: \t\t{}".format(config.INFO)) 
print("DEBUG_bool: \t\t\t{}".format(config.DEBUG)) 
print("DEBUG_level: \t\t\t{}\n".format(config.DEBUG_level))   

# Manually check if inserted directories are correct
userIO = input("Would you continue? y/n\n")
print('\n')
if userIO != "y":
    quit()

# CHECKS ON INPUT DATA
print("Checks on input data ...")
checks.checks(config.image_folder, config.projection_folder, config.projection_delimiter)
if config.DEBUG == True and config.DEBUG_level == 0:
    quit()

# CONVERT TARGET PROJECTIONS IN COLMAP FORMAT
print("\nConverting target projections in COLMAP format ...")
RearrangeProjectionsIDXY.RearrangeProjectionsIDXY(config.image_folder, config.projection_folder, config.projection_delimiter)
if config.DEBUG == True and config.DEBUG_level == 1:
    quit()

# TARGETS MATCHING
print("\nTargets matching ...")
all_matches = matching.Matching(config.image_folder, config.projection_folder, config.projection_delimiter)
if config.DEBUG == True and config.DEBUG_level == 2:
    quit()

# AUTOMATICALLY IMPORT THE TARGETS IN COLMAP
print("\nTargets triangulation ...")
# Rearrange the sparse model output
original_cameras = "{}/cameras.txt".format(config.sparse_model_path)
original_images = "{}/images.txt".format(config.sparse_model_path)
os.mkdir("output/temp")
final_cameras = "output/temp/cameras.txt"
final_images = "output/temp/images.txt"
final_points3D = "output/temp/points3D.txt"

# Copy the camera file cameras.txt and create an empty txt file to store in future the triangulated coordiantes
shutil.copyfile('{}'.format(original_cameras), '{}'.format(final_cameras))
new_file = open('{}'.format(final_points3D), 'w')
new_file.close()

# Copy the camera orientation parameters leaving empty the row for the keypoint projections
images_param_and_ori = [] # It will contain IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME for each image
#new_file = open('{}'.format(final_images), 'w')
with open('{}'.format(original_images), 'r') as lines:
    lines = lines.readlines()[4:]
    for c,line in enumerate(lines):
        if c%2 == 0:
            #new_file.write(line)
            line = line.strip()
            img_params = line.split(" ", 9)
            images_param_and_ori.append(img_params)
        #else:
            #new_file.write("\n")
#new_file.close()

# Import camera models
cameras = []
with open(final_cameras, "r") as camera_models:
    lines = camera_models.readlines()[3:]
    for line in lines:
        line = line.strip()
        cameras.append(line.split(" ", 4))

# Initialize a new database
image_list = []
new_file = open('{}'.format(final_images), 'w')
for counter, i in enumerate(images_param_and_ori):
    IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME = i
    image_list.append(NAME)
    NEW_IMAGE_ID = counter + 1
    i = NEW_IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME
    new_file.write("{} {} {} {} {} {} {} {} {} {}\n\n".format(NEW_IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME))
new_file.close()


image_dict, matches_cont = database.newDB(cameras, image_list, all_matches, config.projection_delimiter, images_param_and_ori, config.image_file_extension)
if config.DEBUG == True and config.DEBUG_level == 3:
    quit()

## EXPERIMENTAL
##images_param_and_ori = []
#reverse_image_dict = {v: k for k, v in image_dict.items()}
#new_file = open('{}'.format(final_images), 'w')
#for i in images_param_and_ori:
#    IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME = i
#    if 
#        
#with open('{}'.format(original_images), 'r') as lines:
#    lines = lines.readlines()[4:]
#    for c,line in enumerate(lines):
#        if c%2 == 0:
#            new_file.write(line)
#            line = line.strip()
#            img_params = line.split(" ", 9)
#            #images_param_and_ori.append(img_params)
#        else:
#            new_file.write("\n")
#new_file.close()

# Initialize a new project.ini
current_directory = os.getcwd()
with open("lib/project.ini", "w") as ini_file:
    ini_file.write(
f"""log_to_stderr=false
random_seed=0
log_level=2
database_path=output/db.db
image_path={config.image_folder}
input_path=output/temp
output_path=output/bin_outs""")
    ini_file.write("\n")

with open("lib/project.ini", "a") as ini_file:                    
    with open("lib/template.ini","r") as ini_options:
        ini_file.write(ini_options.read())

# Target triangulation
os.mkdir("output/bin_outs")
print("***************")
print(r"{}/COLMAP.bat".format(config.COLMAP_EXE_PATH))
print(r"{}/lib/project.ini".format(current_directory))
print("***************")
subprocess.run([r"{}/COLMAP.bat".format(config.COLMAP_EXE_PATH), "point_triangulator", "--project_path", r"{}/lib/project.ini".format(current_directory)])
if config.DEBUG == True and config.DEBUG_level == 4:
    quit()

# Export ply file and convert the binary output in a txt output
os.mkdir("output/txt_outs")

# bin to ply format
subprocess.run(["{}/COLMAP.bat".format(config.COLMAP_EXE_PATH), "model_converter", "--input_path", "{}/output/bin_outs".format(current_directory), "--output_path", "{}/output/targets.ply".format(current_directory), "--output_type", "PLY"])

# bin to txt format
subprocess.run(["{}/COLMAP.bat".format(config.COLMAP_EXE_PATH), "model_converter", "--input_path", "{}/output/bin_outs".format(current_directory), "--output_path", "{}/output/txt_outs".format(current_directory), "--output_type", "TXT"])

# Store as object the triangulated targets
os.mkdir("output/CloudCompare")
shutil.copyfile('{}'.format(config.ground_truth_path), '{}/output/CloudCompare/GroundTruth.txt'.format(current_directory))
points3D_file = "output/txt_outs/points3D.txt"

with open(points3D_file, "r") as p3D_file:
    lines = p3D_file.readlines()[3:]
    points3D = [target3D(
                                        t3D_id = None,
                                        x = None,
                                        y = None,
                                        z = None,
                                        r = None,
                                        g = None,
                                        b = None,
                                        error = None,
                                        track = None )for i in range(len(lines))]
    
    for count, line in enumerate(lines):
        line = line.strip()
        POINT3D_ID, X, Y, Z, R, G, B, ERROR, TRACK = line.split(" ", 8)
        points3D[count] = target3D(
                                        t3D_id = None,
                                        x = float(X),
                                        y = float(Y),
                                        z = float(Z),
                                        r = int(R),
                                        g = int(G),
                                        b = int(B),
                                        error = float(ERROR),
                                        track = TRACK
                                    )

# Export targets with ID in COLMAP coordinates
target_COLMAP_XYZ_file = open("output/CloudCompare/colmap.txt", "w")

total_tracks = 0
reproj_error = []
for target in points3D:
    img_id, target_id, trash = target.track.split(" ", 2)
    img_id, target_id = int(img_id), int(target_id)
    
    image_dict_mirrored = {v: k for k, v in image_dict.items()}
    image_name = image_dict_mirrored[img_id]
    
    
    with open("{}/{}.txt".format(config.projection_folder, image_name)) as proj_file:
        lines = proj_file.readlines()
        line = lines[target_id]
        line = line.strip()
        target_name, trash = line.split(config.projection_delimiter, 1)
        #target.t3D_id = int(target_name)
        target.t3D_id = target_name
        target_COLMAP_XYZ_file.write("{},{},{},{}\n".format(target.t3D_id, target.x, target.y, target.z))
    
    tracks = target.track.split(" ")
    total_tracks += len(tracks)/2
    
    reproj_error.append(target.error)

target_COLMAP_XYZ_file.close()


# Align the two clouds (cloud from COLMAP to ground_truth)
output_file = open("output/outs.txt", "w")
subprocess.run(["{}/Align.exe".format(config.AlignCC_PATH), "{}/output/CloudCompare/colmap.txt".format(current_directory), "{}".format(config.ground_truth_path), ">", "{}/output/CloudCompare/out.txt"], stdout=output_file)
output_file.close()

# Check if all tarhets and projections are used
with open("output/outs.txt", "a") as output_file:
    output_file.write("\n- SUMMARY -\n")
    output_file.write("Nummber of targets: {}\n".format(len(points3D)))
    output_file.write("Number of total projections: {}\n".format(total_tracks))
    output_file.write("Mean Reprojection Error: {} pix\n".format(np.mean(reproj_error)))
    output_file.write("Standard Deviation: {} pix\n".format(np.std(reproj_error)))
    output_file.write("N of TOTAL matches: {}".format(matches_cont))

# Print results
print("\n\n")
with open("output/outs.txt", "r") as output_file:
    lines = output_file.readlines()
    for line in lines:
        line = line.strip()
        print(line)

# Export cameras
external_cameras_path = "output/txt_outs/images.txt"
camera_ori = ExportColmapCameras.ExportCameras(external_cameras_path)
out_file = open("output/cameras_extr.txt", 'w')
for element in camera_ori:
    out_file.write(element)
    out_file.write('\n')
out_file.close()

### END
print('\nEND')

if config.DEBUG == True and config.DEBUG_level == 5:
    quit()