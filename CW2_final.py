import numpy as np
import pandas as pd
import seaborn 

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap

from scipy.stats import gaussian_kde

# load data
data = pd.read_csv('Results_21Mar2022.csv')

# select data
data_mean_land = data[['mean_land', 'sex', 'diet_group', 'age_group']]

# label
diet_group = ['fish', 'meat50', 'meat100', 'meat', 'vegan', 'veggie']
age_group = ['20-29', '30-39', '40-49', '50-59', '60-69', '70-79'][::-1]
sex = ['female', 'male']

# set x range
x_min = min(data_mean_land['mean_land'])
x_max = max(data_mean_land['mean_land'])

# set y range
y_max = 0
for _, data_idx in data_mean_land.groupby(["age_group", "diet_group", "sex"]):

    kde = gaussian_kde(data_idx['mean_land'])
    x_range = np.linspace(min(data_mean_land['mean_land']), max(data_mean_land['mean_land']), 100)
    temp_y = kde(x_range)

    if y_max < np.max(temp_y) :
        y_max = np.max(temp_y)

# set color range
mean_land_min = 10000
mean_land_max = 0

for _, data_idx in data_mean_land.groupby(["age_group", "diet_group", "sex"]):
    if mean_land_min > np.mean(data_idx['mean_land']) :
        mean_land_min = np.mean(data_idx['mean_land'])
    
    if mean_land_max < np.mean(data_idx['mean_land']) :
        mean_land_max = np.mean(data_idx['mean_land'])

norm = plt.Normalize(vmin = mean_land_min, vmax = mean_land_max)

# using https://paletton.com/#uid=1000u0kllllaFw0g0qFqFg0w0aF to choose color for the color map
color = ["#FFAAAA", "#D46A6A", "#AA3939", '#801515', '#550000']
cmap = LinearSegmentedColormap.from_list('color_map', color)

# sub-figure
fig = plt.figure(figsize=(24, 12))
# gs = gridspec.GridSpec(len(age_group), 2 * len(diet_group) + 1, wspace = 0, hspace = 0)
gs = gridspec.GridSpec(len(age_group), 2 * len(diet_group) + 1, width_ratios = [1,1,1,1,1,1,0.3,1,1,1,1,1,1], wspace=0, hspace=0)

# plot
for sex_idx, sex_label in enumerate(sex):

    # devide sex
    sex_data_mean_land = data_mean_land[data_mean_land['sex'] == sex_label]
    x_male_start = sex_idx * (len(diet_group) + 1)

    # plot sub-figure
    for diet_idx, diet in enumerate(diet_group) :
        for age_idx, age in enumerate(age_group) :
            data_selected = sex_data_mean_land[(sex_data_mean_land['diet_group'] == diet) & (sex_data_mean_land['age_group'] == age)]

            sub_figure = fig.add_subplot(gs[age_idx, x_male_start + diet_idx]) 

            # set the black ground color as the color map
            sub_figure.set_facecolor(cmap(norm(np.mean(data_selected['mean_land']))))
            
            # plot the distribution of MCM
            # when you use MCM, it is always interesting to explore the distibution of the results of the MCM 
            # using the opposite color from the website
            # seaborn.kdeplot(data=data_selected, x='mean_land', color = '#2E4272', fill = True, linewidth = 0, alpha = 1)   
            seaborn.kdeplot(data=data_selected, x='mean_land', color = '#6378AA', fill = True, linewidth = 0, alpha = 1)

            # set all sub-figure at the same tick   
            sub_figure.set_xlim(x_min, x_max)
            sub_figure.set_ylim(0, y_max)         

            # only show one x label (the lowest x label) 
            if age_idx == len(age_group) - 1 :
                # sub_figure.set_xlabel(diet.capitalize(), fontsize=14, labelpad=6)
                sub_figure.set_xlabel(diet, fontsize=12)
            else :
                sub_figure.set_xticks([])
                sub_figure.set_xticklabels([])           

            # only show one y label (the most left y label)
            if sex_idx == 0 and diet_idx == 0 :
                # sub_figure.set_ylabel(age, fontsize = 14, rotation = 0, ha = 'right', va = 'center', labelpad = 10)
                sub_figure.set_ylabel(age, fontsize = 12)
            else :
                sub_figure.set_yticks([])
                sub_figure.set_yticklabels([])
                sub_figure.set_ylabel(None)
            
            # slightly divide each sub-figure
            for i in sub_figure.spines.values():
                i.set_visible(True)
                i.set_edgecolor('black')
                i.set_alpha(0.2)
                i.set_linewidth(1)

# label for the color map
pos_colorbar = fig.add_axes([0.93, 0.3, 0.015, 0.4])
colorbar = plt.colorbar(plt.cm.ScalarMappable(norm = norm, cmap = cmap), cax = pos_colorbar)
colorbar.set_label('Mean Land Use (m²)', fontsize=16)

# The describtion of the y label. It is the probabilty density of the distritbion of the MCM
fig.text(0.1075, 0.89, 'Density')

# The describiton of the x label. It is Mean Land Use of the distribution of the MCM
fig.text(0.90, 0.09, 'Mean Land Use (m²)')

# label for the diet group
fig.text(0.49, 0.03, 'Diet Group', fontsize=16)

# label for the age group
fig.text(0.07, 0.46, 'Age Group', rotation = 90, fontsize = 16)

# main title
fig.suptitle('Comparisons and Distributions of Mean Land Use by Sex, Diet and Age', fontsize = 20)

# sub title
fig.text(0.3, 0.9, 'Female', fontsize = 16)
fig.text(0.7, 0.9, 'Male', fontsize = 16)

# save fig
plt.savefig('CW2_figure.png')

plt.show()