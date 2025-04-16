import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# === Load data ===
data_path = "/path/to/your/data.csv"
pval_path = "/path/to/your/data/pval.csv"

data_df = pd.read_csv(data_path)
pval_df = pd.read_csv(pval_path)

# === Create output folder ===
output_dir = "/path/to/output/folder/"
os.makedirs(output_dir, exist_ok=True)

# === Seaborn theme with large fonts ===
sns.set_theme(style="white", font_scale=3.2) 

# === Group comparisons for significance ===
comparison_map = {
    'center': ('P_center', 'CT_center'),
    'PL1': ('P_center', 'PL1'),
    'PL2': ('P_center', 'PL2'),
    'PL3': ('P_center', 'PL3'),
    'PL4': ('P_center', 'PL4'),
    'CTL1': ('CT_center', 'CTL1'),
    'CTL2': ('CT_center', 'CTL2'),
    'CTL3': ('CT_center', 'CTL3'),
    'CTL4': ('CT_center', 'CTL4'),
}

# === Convert p-values to stars ===
def get_significance_label(p):
    if p <= 0.001:
        return '***'
    elif p <= 0.01:
        return '**'
    elif p <= 0.05:
        return '*'
    else:
        return 'ns'

# === Outlier style ===
flierprops = dict(marker='o', markerfacecolor='none', markeredgecolor='black',
                  markersize=10, linestyle='none', linewidth=2)

# === Plot each feature ===
for _, row in pval_df.iterrows():
    feature = row['filename']
    if feature not in data_df.columns:
        continue

    fig, ax = plt.subplots(figsize=(18, 9))  # larger canvas
    ax.set_title(feature)

    sns.boxplot(
        y='group', x=feature, data=data_df,
        palette='Paired',
        showfliers=True,
        flierprops=flierprops,
        ax=ax
    )

    # Spacing for stars
    xmin, xmax = ax.get_xlim()
    h = (xmax - xmin) * 0.04
    offset = xmax + h
    comparisons_plotted = 0
    yticklabels = [t.get_text() for t in ax.get_yticklabels()]

    for col in ['PL1', 'PL2', 'PL3', 'PL4', 'CTL1', 'CTL2', 'CTL3', 'CTL4', 'center']:
        if col not in comparison_map:
            continue
        g1, g2 = comparison_map[col]
        if g1 in yticklabels and g2 in yticklabels:
            pval = row[col]
            label = get_significance_label(pval)

            y1, y2 = yticklabels.index(g1), yticklabels.index(g2)
            x = offset + comparisons_plotted * h * 2.0
            ax.plot([x, x+h, x+h, x], [y1, y1, y2, y2], lw=2, c='black')
            ax.text(x + h + 1, (y1 + y2) / 2, label, va='center', ha='left', fontsize=30)
            comparisons_plotted += 1

    ax.set_xlabel("Normalized peak intensity", labelpad=25)
    ax.set_ylabel("Groups name", labelpad=25)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/{feature}_styled_boxplot.png", dpi=300, bbox_inches='tight')
    plt.close()

