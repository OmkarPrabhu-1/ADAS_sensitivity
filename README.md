# ADAS_sensitivity
To establish an approach to better understand how image properties impact CV algorithm performance.
The features chose were FSIM, SSIM, Brisque, NIQE, PIQE, Contrast, PSNR, and RSME. The IQA-based technique to characterizing pictures is used to measure how well people perceive the quality of the images. Hence, this method was used to establish a relaibility metric for CV detection algorithms.
This is a skeletal code for generating various image property metrics and then deriving its influence on the CV algorithms.
Image dataset has not been uploaded due to confidentiality of the dataset.

Steps to run:
1. Images and ground truth must be stored in Image and GT folder respectively. 
2. Then cropy.py should be executed to resize the images into 416x416.
3. IQA (Image quality assessment metrics) are generated using IQA_metrics.py.
4. Bounding boxes for th Ground truth image are generated using GT_boundingbox.py.
5. Then the cars are classified using Deepstack via file deepstack_detect.py.
6. GT_boundingbox.py and deepstack_detect.py generate csv files that are necessary for NN classification.
7. Finally, a four layer nueral network (nn_classification.py) is used to obtain a relationship between the IQAs and deepstack results.
