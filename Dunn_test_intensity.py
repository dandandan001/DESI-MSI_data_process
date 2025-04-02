# This script is modified based on Zongyuan Liu's script.
# Please cite https://github.com/zyliu-OU/McCall-Lab/tree/main/03172021


import pandas
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from statannotations.Annotator import Annotator

M_F_data = pandas.read_csv("path/to/your/dataset/file.csv") 
full_mass_data = pandas.read_csv("path/to/the/features/to/plot/file.csv")
mass_list = full_mass_data.filename.to_list()

# Folder to save plots
output_folder = "path/to/your/output/Dunn_plots"
os.makedirs(output_folder, exist_ok=True)

sns.set_theme(style="white", font_scale=3.2)

# change the order here will change the order of groups display 
order = ['CT_center', 'CTL1', 'CTL2', 'CTL3', 'CTL4',
         'P_center', 'PL1', 'PL2', 'PL3', 'PL4']

mass_list_number = 1
for mass in mass_list:
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.set_title(mass)

    g1 = sns.barplot(x=M_F_data[str(mass)], y=M_F_data['group'], palette='Paired')

    annot_1 = Annotator(g1, [(('P_center','CT_center')),
                             ('PL1','CTL1'),
                             ('PL2','CTL2'),
                             ('PL3','CTL3'),
                             ('PL4','CTL4')],
                        x=M_F_data[str(mass)],
                        y=M_F_data['group'],
                        order=order,
                        orient='h')

    annot_1.configure(test='Mann-Whitney', comparisons_correction='BH', 
                      correction_format="replace", text_format='star', 
                      loc='outside', verbose=0)
    annot_1.apply_test()
    annot_1.annotate()

    ax1.set_ylabel('Groups name')
    ax1.set_xlabel('Normalized peak intensity')

    plt.savefig(os.path.join(output_folder, f"boxplot_{mass_list_number}_{mass}.png"), 
                dpi=300, bbox_inches='tight')
    plt.close(fig1)  # Close figure to prevent display

    mass_list_number += 1

