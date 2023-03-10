# COLMAP_GroundControlPoints
Python scripts to triangulate ground control points (GCPs) in COLMAP and check their 3D position agiainst a ground truth with an Helmert transformation.

### Create a conda environment named colmap_tri
Open Anaconda prompt as administrator

```
>conda create --name colmap_tri
>conda activate colmap_tri
>conda install -c conda-forge colmap_tri
>conda install -c anaconda pandas
>conda install -c conda-forge matplotlib
```

### Usage
Set inputs and options in the config.py file. See the script for more details.
```
>conda activate colmap_tri
>python main.py
```

### Notes
*All images in ./sample_test/imgs must be registered in the sparse model
*This repository contains some scripts to extend "COLMAP 3.6 and 3.7" (https://colmap.github.io/) functionalities. If you find these scripts useful, please consider citing the paper for which these scripts were developed:

```
@Article{isprs-archives-XLVI-2-W1-2022-73-2022,
AUTHOR = {Bellavia, F. and Morelli, L. and Menna, F. and Remondino, F.},
TITLE = {IMAGE ORIENTATION WITH A HYBRID PIPELINE ROBUST TO ROTATIONS AND WIDE-BASELINES},
JOURNAL = {The International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences},
VOLUME = {XLVI-2/W1-2022},
YEAR = {2022},
PAGES = {73--80},
URL = {https://www.int-arch-photogramm-remote-sens-spatial-inf-sci.net/XLVI-2-W1-2022/73/2022/},
DOI = {10.5194/isprs-archives-XLVI-2-W1-2022-73-2022}
}