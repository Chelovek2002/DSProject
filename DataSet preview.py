# import numpy as np
# import altair as alt
# import altair_viewer
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_style("ticks")

wage_df = pd.read_csv('data_cleaned_2021.csv')
columns_to_drop = [
    "index",
    "Job Title",
    "Job Description",
    "Salary Estimate",
    "Company Name",
    "Location",
    "Headquarters",
    "Employer provided",
    "Founded",
    "Job Location",
    "Hourly",
    "Competitors"
]
rename_dict = {"Type of ownership": "own_type",
               'seniority_by_title': 'seniority',
               "Avg Salary(K)": "avg_salary"}
wage_df = wage_df.drop(columns=columns_to_drop).rename(columns=rename_dict)

init_own = ['Company - Private',
            'Company - Public',
            'Nonprofit Organization',
            'Other Organization',
            'School / School District']
new_own = [
    'Private',
    'Public',
    'Nonprofit',
    'Other',
    'School'
]
wage_df.own_type.replace(init_own, new_own, inplace=True)
skills = ['Python', 'spark', 'aws', 'excel', 'sql', 'sas', 'keras', 'pytorch',
          'scikit', 'tensor', 'hadoop', 'tableau', 'bi', 'flink', 'mongo',
          'google_an']
companies_info = ["own_type", "Industry", "Sector", "Revenue", ]
people_info = ['job_title_sim', 'Degree', 'seniority']
salaries = ["Lower Salary", "Upper Salary", "avg_salary"]
wage_df = wage_df.assign(skill_num=lambda x: sum([x[a] for a in skills]))


# correlation between wage and degree for different seniority
def show_wage_degree_corr():
    sns.catplot(data=wage_df,
                x='Degree',
                y='avg_salary',
                hue='seniority',
                kind='box',
                order=['na', 'M', 'P'],
                hue_order=['jr', 'na', 'sr'])
    plt.xticks(rotation=45)
    plt.show()


# correlation between wage and skills for different seniority
def show_wage_skills_corr():
    sns.catplot(data=wage_df,
                x='skill_num',
                y='avg_salary',
                hue='seniority',
                hue_order=['jr', 'na', 'sr'],
                kind='point',
                scale=0.9
                )
    plt.xticks(rotation=45)
    plt.show()


industry_agg = wage_df.groupby("Industry").mean().drop(columns=['Age', 'Rating', 'skill_num'] + salaries).reset_index()
industry_agg = industry_agg.melt(id_vars='Industry')


# set of common skills in an industry
def industry_skill(industry):
    sns.barplot(
        data=industry_agg[industry_agg.Industry == industry],
        y='value',
        x='variable')
    plt.xticks(rotation=45)
    plt.show()


# industry_skill('Advertising & Marketing')


# correlation between wage and average over industry
ind_mean = wage_df.groupby('Industry').agg({'Industry': 'size', 'avg_salary': 'mean'})
ind_mean['Industry_name'] = ind_mean.index


def industry_salary():
    sns.scatterplot(data=wage_df,
                    x='Industry',
                    y='avg_salary',
                    hue='seniority')
    plt.xticks(rotation=45)
    plt.show()
industry_salary()