This project describes 
1. how to generate better quality ion images from mass spectrometry imaging (MSI) dataset: whole region plot and regions of interests (ROI) plot. (Python code, ChatGPT was used for debugging)
Please cite: Desorption electrospray ionization–mass spectrometry imaging of metabolites and lipids in heart samples infected with Trypanosoma cruzi, Dan Chen, Guilherme MP Carrara, Laura-Isobel McCall# and Zhibo Yang#

2. Perfrom statistical analysis on pixels from ROI:
   Wilcox t-test (R code adapted from McCall lab, https://github.com/zyliu-OU/McCall-Lab/tree/main/03172021, please cite: Liu, Z., et al, 2023. Localized cardiac small molecule trajectories and persistent chemical sequelae in experimental Chagas disease. Nature Communications, 14(1), p.6769.)
   Random Forest (R code, adapted from McCall lab) and
   Boxplot using the p-val from Wilcox t-test.
   
