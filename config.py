### TARGET TRIANGULATION
### 3DOM - FBK - TRENTO - ITALY
# Configuration file
# Please, change the input directories with yours.
# Note: Set 0.5 for the image_translation_vector_X and image_translation_vector_Y parameters, when you mark targets with OpenCV or other tools which have the reference system placed in the middle of the first pixel, while COLMAP has the reference system placed in the upper-left corner.
# GCPs LABEL MUST BE AN INTEGER!!!

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--Imgs", help = "Path to the image folder", required=True)
parser.add_argument("-e", "--ImgExtension", help = "Image extension file", required=True)
parser.add_argument("-p", "--Projections", help = "Path to image projections", required=True)
parser.add_argument("-d", "--ProjectionDelimeter", help = "Delimeter used in the projections file", required=True)
parser.add_argument("-s", "--SparseModel", help = "Path to COLMAP sparse reconstruction", required=True)
parser.add_argument("-g", "--GroundTruth", help = "Path to ground truth file", required=True)
parser.add_argument("-c", "--ColmapExe", help = "Path to the COLMAP exe", required=True)
parser.add_argument("-a", "--AlignerExe", help = "Path to aligner exe", required=True)
args = parser.parse_args()

COLMAP_EXE_PATH = args.ColmapExe
AlignCC_PATH = args.AlignerExe
image_folder = args.Imgs
projection_folder = args.Projections
sparse_model_path = args.SparseModel
ground_truth_path = args.GroundTruth
#database_path = r"./colmap_sparse/database.db"

image_file_extension = args.ImgExtension
projection_delimiter = args.ProjectionDelimeter
image_reduction_factor = 0.24                      # Ratio between the image resolution used in COLMAP and the image res targets were extracted
image_translation_vector_X = 0.5                        # X and Y value must be the same
image_translation_vector_Y = 0.5                        # X and Y value must be the same
INFO = False                                             # Get more info printed when script is running
DEBUG = False
DEBUG_level = 5                                         # 0:CHECKS
                                                        # 1:CONVERT TARGET PROJECTIONS IN COLMAP FORMAT
                                                        # 2:TARGETS MATCHING
                                                        # 3:INITIALIZE A NEW DATABASE
                                                        # 4:TARGET TRIANGULATION
                                                        # 5:FULL PIPELINE







