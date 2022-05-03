# import numpy as np
# import altair as alt
# import altair_viewer
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_style("ticks")

wage_df = pd.read_csv('data_cleaned_2021.csv').drop(columns='index').drop_duplicates()
rename_dict = {'seniority_by_title': 'seniority', 'Avg Salary(K)': "avg_salary"}
columns_to_drop = [
    "Job Title",
    "Job Description",
    "Salary Estimate",
    "Company Name",
    "Headquarters",
    "Employer provided",
    "Founded",
    "Job Location",
    "Hourly",
    "Competitors",
    "Type of ownership",
    "Lower Salary",
    "Upper Salary",
    'Age'
]
wage_df = wage_df.drop(columns=columns_to_drop).rename(columns=rename_dict)
wage_df.columns = wage_df.columns.str.lower()
skills = ['python', 'spark', 'aws', 'excel', 'sql', 'sas', 'keras', 'pytorch',
          'scikit', 'tensor', 'hadoop', 'tableau', 'bi', 'flink', 'mongo',
          'google_an']
wage_df = wage_df.assign(skill_num=lambda x: sum([x[a] for a in skills]))
wage_df.seniority.replace(['na', 'jr', 'sr'], ['Not Available', 'Junior', 'Senior'], inplace=True)
# wage_df.degree.replace()


# function to aggregate sectors and industries
def df_aggregate_by(param):
    param_agg = (wage_df.groupby(param)
                 .mean()
                 .drop(columns=['rating', 'skill_num', 'avg_salary'])
                 .reset_index()
                 )
    return param_agg.melt(id_vars=param)


industry_agg = df_aggregate_by('industry')
sector_agg = df_aggregate_by('sector')


# correlation between wage and degree for various seniority
def show_wage_degree_corr():
    sns.catplot(data=wage_df,
                x='degree',
                y='avg_salary',
                hue='seniority',
                kind='box',
                order=['na', 'M', 'P'],
                hue_order=['Junior', 'Not Available', 'Senior'])
    plt.xticks(rotation=45)
    plt.show()


# correlation between wage and skills for various seniority
def show_wage_skills_corr():
    sns.catplot(data=wage_df,
                x='skill_num',
                y='avg_salary',
                hue='seniority',
                hue_order=['Junior', 'Not Available', 'Senior'],
                kind='point',
                scale=0.9
                )
    plt.xticks(rotation=45)
    plt.show()


# set of common skills in an industry
def industry_skill(industry):
    sns.barplot(
        data=industry_agg[industry_agg.industry == industry],
        y='value',
        x='variable').set(ylabel=f'Частота использования в {industry}')
    plt.xticks(rotation=45)
    plt.show()


# set of common skills in a sector
def sector_skill(sector):
    sns.barplot(
        data=sector_agg[sector_agg.sector == sector],
        y='value',
        x='variable').set(ylabel=f'Частота использования в {sector}')
    plt.xticks(rotation=45)
    plt.show()


def skill_sector(skill):
    sns.barplot(
        data=sector_agg[sector_agg.variable == skill],
        y='value',
        x='sector').set(ylabel=f'Частота использования {skill}')
    plt.xticks(rotation=30)
    plt.show()
