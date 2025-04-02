import os
import pandas as pd
import matplotlib.pyplot as plt

# Paths to the heart data files
# load the file in an order of your desired display
# In my data, heart1,3,5 are infected hearts, heart2,4,6 are naive hearts
csv_files = [
    "../MSI_plots_data_TIC/masked_TIC_hearts/heart1_masked_TIC_normalized_overall.csv",
    "../MSI_plots_data_TIC/masked_TIC_hearts/heart3_masked_TIC_normalized_overall.csv",
    "../MSI_plots_data_TIC/masked_TIC_hearts/heart5_masked_TIC_normalized_overall.csv",
    "../MSI_plots_data_TIC/masked_TIC_hearts/heart2_masked_TIC_normalized_overall.csv",
    "../MSI_plots_data_TIC/masked_TIC_hearts/heart4_masked_TIC_normalized_overall.csv",
    "../MSI_plots_data_TIC/masked_TIC_hearts/heart6_masked_TIC_normalized_overall.csv",
]

# Read the feature list file
sample_file = "path/to/your/feature/list.csv"  # Replace with a valid file path
df_sample = pd.read_csv(sample_file)

# Convert the 'features' column to strings and extract as a list
features = df_sample['features'].astype(str).to_list()


# Directory to save the plots
output_dir = "path/to/yout/MSI_plots_whole_hearts"
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist



# Loop through each feature
for feature in features:
    # Gather global min and max for consistent scaling
    all_values = []
    for file_path in csv_files:
        df = pd.read_csv(file_path)
        if feature in df.columns:
            all_values.extend(df[feature].dropna().tolist())
    if not all_values:
        print(f"No values found for feature {feature}, skipping.")
        continue
    vmin = min(all_values)
    vmax = max(all_values)
    
for feature in features:
    # Prepare the grid layout for the current feature
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(10, 9))  # Adjust figure size as needed
    fig.suptitle(f"DESI_MSI Plot for mz_{feature}", fontsize=16)

    # Flatten axes for easy iteration
    axes = axes.flatten()

    # Loop through the CSV files to create subplots
    for i, file_path in enumerate(csv_files):
        # Read the current CSV file
        df = pd.read_csv(file_path)

        # Extract X, Y, and the current feature
        x_coords = df["X"]
        y_coords = df["Y"]
        feature_values = df[feature]

        # Plot the scatter plot for the current feature
        scatter = axes[i].scatter(
            x_coords, y_coords, c=feature_values, cmap='gnuplot', marker='s', s=8, alpha=0.7, vmin=vmin, vmax=vmax
        )
        
        # Set subplot title
        #axes[i].set_title(f"File {i+1}", fontsize=10)

        # Turn off x-axis and y-axis ticks and labels
        axes[i].tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)

    # Adjust layout to narrow gaps between subplots
    plt.subplots_adjust(
        left=0.1,  # Space on the left
        right=0.9,  # Space on the right
        top=0.9,  # Space at the top
        bottom=0.15,  # Space at the bottom
        hspace=0.1,  # Height spacing between subplots
        wspace=0.08   # Width spacing between subplots
    )

    # Add a colorbar at the bottom of the plot
    cbar_ax = fig.add_axes([0.15, 0.08, 0.7, 0.03])  # [left, bottom, width, height]
    cbar = fig.colorbar(scatter, cax=cbar_ax, orientation='horizontal')
    cbar.set_label(f"mz_{feature} normalized intensity", fontsize=10)

    # Save the plot with the feature name in the filename
    output_file = os.path.join(output_dir, f"mz_{feature}_scatter_plot.png")
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    print(f"Saved plot for {feature} to {output_file}")

    # Close the figure to free memory
    plt.close(fig)




