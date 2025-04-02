import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Paths to the heart data files
# load the file in an order of your desired display
# In my data, heart1,3,5 are infected hearts, heart2,4,6 are naive hearts
csv_files = {
    1: "../MSI_plots_data_TIC/masked_TIC_hearts/heart1_masked_TIC_normalized_overall.csv",
    2: "../MSI_plots_data_TIC/masked_TIC_hearts/heart3_masked_TIC_normalized_overall.csv",
    3: "../MSI_plots_data_TIC/masked_TIC_hearts/heart5_masked_TIC_normalized_overall.csv",
    4: "../MSI_plots_data_TIC/masked_TIC_hearts/heart2_masked_TIC_normalized_overall.csv",
    5: "../MSI_plots_data_TIC/masked_TIC_hearts/heart4_masked_TIC_normalized_overall.csv",
    6: "../MSI_plots_data_TIC/masked_TIC_hearts/heart6_masked_TIC_normalized_overall.csv"
}

# Path to region coordinates
region_file = "path/to/your/coordinates/file.csv"
df_regions = pd.read_csv(region_file)

# Read the feature list file
sample_file = "path/to/your/feature/list.csv"  # Replace with a valid file path
df_sample = pd.read_csv(sample_file)
features = df_sample['features'].astype(str).to_list()

# Directory to save the plots
output_dir = "path/to/yout/Region_Feature_infected_hearts"
os.makedirs(output_dir, exist_ok=True)

# Process each feature
for feature in features:
    print(f"Processing feature: mz_{feature}")

    # Get unique Heart-Spot combinations
    unique_regions = df_regions.groupby(["Heart_ID", "spot"]).size().reset_index().drop(columns=0)

    
    # Calculate global vmin and vmax for color consistency
    all_values = []
    for heart_id, spot_id in unique_regions.values:
        if heart_id in csv_files:
            df_heart = pd.read_csv(csv_files[heart_id])
            if feature in df_heart.columns:
                all_values.extend(df_heart[feature].dropna().tolist())
    if not all_values:
        print(f"No values found for feature {feature}, skipping.")
        continue
    vmin = min(all_values)
    vmax = max(all_values)

    # Define figure layout (each region gets a separate plot)
    
    num_regions = len(unique_regions)
    num_cols = 5
    num_rows = int(np.ceil(num_regions / num_cols))

    fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(22, 5.1 * num_rows))
    axes = axes.flatten()

    # Loop through each Heart-Spot combination and plot separately
    for i, (heart_id, spot_id) in enumerate(unique_regions.values):
        if heart_id not in csv_files:
            print(f"Warning: No data file found for Heart {heart_id}. Skipping.")
            continue

        # Load full heart data
        df_heart = pd.read_csv(csv_files[heart_id])

        # Ensure feature exists in the dataset
        if feature not in df_heart.columns:
            print(f"Feature '{feature}' not found in Heart {heart_id} dataset. Skipping.")
            continue

        # Extract region for the given heart and spot
        df_region = df_regions[(df_regions['Heart_ID'] == heart_id) & (df_regions['spot'] == spot_id)]
        x_min, x_max = df_region["X"].min(), df_region["X"].max()
        y_min, y_max = df_region["Y"].min(), df_region["Y"].max()

        # Filter points within the defined region
        df_inside = df_heart[
            (df_heart["X"] >= x_min) & (df_heart["X"] <= x_max) &
            (df_heart["Y"] >= y_min) & (df_heart["Y"] <= y_max)
        ]

        # Debugging: Check how many points were found
        print(f"Heart {heart_id}, Spot {spot_id}: {len(df_inside)} points found inside region for feature {feature}.")

        if len(df_inside) > 0:
            # Scatter plot for feature intensity
            scatter = axes[i].scatter(
                df_inside["X"], df_inside["Y"], 
                c=df_inside[feature], cmap='gnuplot', marker='s', s=250, alpha=0.8, vmin=vmin, vmax=vmax, label=f"Spot {spot_id}"
            )

            # Titles and formatting
            axes[i].set_title(f"Feature: mz_{feature}-Heart{heart_id} Spot{spot_id}", fontsize=15)

            # Turn off x and y labels
            axes[i].set_xlabel("")
            axes[i].set_ylabel("")

            # Turn off x and y ticks
            axes[i].tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)

        else:
            axes[i].set_title(f"Heart {heart_id} Spot {spot_id} (No data in region)", fontsize=10)

    # Hide unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    # Add a colorbar at the bottom
    cbar_ax = fig.add_axes([0.15, 0.08, 0.7, 0.03])  # [left, bottom, width, height]
    cbar = fig.colorbar(scatter, cax=cbar_ax, orientation='horizontal')
    cbar.set_label(f"mz_{feature} normalized intensity", fontsize=15)

    # Adjust layout
    plt.tight_layout(rect=[0, 0.1, 1, 0.95])

    # Save the figure
    output_file = os.path.join(output_dir, f"mz_{feature}_region_plot.png")
    plt.savefig(output_file, dpi=300)
    print(f"Saved region plot for mz_{feature} to {output_file}")

    # Close figure to free memory
    plt.close(fig)
