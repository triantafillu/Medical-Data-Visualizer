import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column.To determine if a person is overweight, first calculate their BMI by dividing their weight in kilograms by the square of their height in meters. If that value is > 25 then the person is overweight. Use the value 0 for NOT overweight and the value 1 for overweight.
def BMI(x):
  bmi = x['weight']/((x['height']/100)**2)
  if (bmi<25):
    return 0
  else:
    return 1

df['overweight'] = df.apply(BMI, axis=1)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholestorol' or 'gluc' is 1, the value is 0. If the value is more than 1,the value is 1.

df.loc[df['cholesterol']==1, 'cholesterol']=0
df.loc[df['cholesterol']>1, 'cholesterol']=1

df.loc[df['gluc']==1, 'gluc']=0
df.loc[df['gluc']>1, 'gluc']=1

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars='cardio', value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    # Group and reformat the data to split it by 'cardio'. Count each feature.
    df_cat = pd.DataFrame(df_cat.groupby(['cardio', 'variable', 'value'])                            ['value'].count()).rename(columns={'value': 'total'})                      .reset_index()

    # Draw the catplot with 'sns.catplot()'
    g = sns.catplot(
        x='variable',
        y='total',
        hue='value',
        col='cardio',
        data=df_cat,
        kind='bar')

    fig =g.fig
    # Save the plot
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    df_heat = df[(df['ap_lo'] <= df['ap_hi'])#diastolic pressure is higher than systolic
                 & (df['height'] >= df['height'].quantile(0.025))#height is less than the 2.5th percentile
                 & (df['height'] <= df['height'].quantile(0.975))#height is more than the 97.5th percentile
                 & (df['weight'] >= df['weight'].quantile(0.025))#weight is less than the 2.5th percentile
                 & (df['weight'] <= df['weight'].quantile(0.975))]#weight is more than the 97.5th percentile

    # Calculate the correlation matrix
    corr_matrix = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr_matrix)
    mask[np.triu_indices_from(mask)] = True

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 10))

    # Draw the heatmap with 'sns.heatmap()'
    ax = sns.heatmap(
        corr_matrix,
        linewidths=.3,
        annot=True,
        fmt='.1f',
        mask=mask,
        square=True,
        center=0,
        vmin=-0.1,
        vmax=0.25,
        cbar_kws={
            'shrink': .5,
            'format': '%.2f'
        })

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
