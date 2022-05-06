import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from dataframe_tidied import wage_df, get_data_for_ranking, get_data_for_corr


def sns_show_wage_degree_corr():
    sns.catplot(data=wage_df,
                x='degree',
                y='avg_salary',
                hue='seniority',
                kind='box',
                hue_order=['Junior', 'Not Available', 'Senior']
                ).set(xlabel='Degree', ylabel='Average Salary')
    plt.show()


# correlation between wage and skills for various seniority
def sns_show_wage_skills_corr():
    sns.catplot(data=wage_df,
                x='skill_num',
                y='avg_salary',
                hue='seniority',
                hue_order=['Junior', 'Not Available', 'Senior'],
                kind='point',
                scale=0.9
                ).set(xlabel='Number of skills from the list', ylabel='Average Salary')
    plt.show()


def sns_ranking(name, highlight, over):
    highlight = highlight if highlight else []
    data = get_data_for_ranking(name, highlight, over)
    sns.set_theme(context='notebook', style='dark')
    sns.set(rc={'axes.facecolor': '#112B3C', 'figure.facecolor': '#112B3C'})
    sns.barplot(data=data['df'], x='share', y=data['skill_or_sector'], palette=data['color'],
                linewidth=0).set(xlabel=data['label'], ylabel=data['skill_or_sector'].capitalize())
    for i, color in enumerate(data['color']):
        plt.gca().get_yticklabels()[i].set_color(color)


# sns_show_wage_skills_corr()
# # sns_show_wage_degree_corr()
# sns_ranking(wage_df.loc[1, 'sector'], ['python', 'sql'], 'sector')
#
# plt.show()


def customize_axis(ax):
    ax.xaxis.label.set_color('#EFEFEF')
    ax.yaxis.label.set_color('#EFEFEF')
    ax.tick_params(axis='x', colors='#EFEFEF')
    ax.grid(visible=True, axis='x', color='#205375')
    ax.grid(visible=False, axis='y')


def sns_wage_corr(param):
    dct = get_data_for_corr(param)
    sns.set_theme(context='notebook', style='dark')
    sns.set(rc={'axes.facecolor': '#112B3C', 'figure.facecolor': '#112B3C'})
    sns.stripplot(
        data=wage_df, x=param, y="avg_salary", hue="seniority",
        dodge=False, order=dct['order'], alpha=0.4)
    sns.pointplot(data=wage_df,
                  x=param,
                  y='avg_salary',
                  hue='seniority',
                  order=dct['order'],
                  hue_order=['Other', 'Senior'],
                  scale=0.9
                  ).set(xlabel=dct['x_label'], ylabel='Average Salary (K)')
    plt.text(dct['x1'], dct['y1'], "Senior", horizontalalignment='left', size='medium', color='#da8251',
             weight='semibold')
    plt.text(dct['x2'], dct['y2'], "Other", horizontalalignment='left', size='medium', color='#4c72b0',
             weight='semibold')

