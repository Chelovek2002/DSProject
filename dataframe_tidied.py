import pandas as pd
import numpy as np


def get_dataframe():
    df = pd.read_csv('data_cleaned_2021.csv').drop(columns='index').drop_duplicates()
    rename_dict = {'seniority_by_title': 'seniority',
                   'Avg Salary(K)': "avg_salary",
                   'company_txt': 'company',
                   'job_title_sim': 'job',
                   'Revenue': 'company_revenue',
                   "Type of ownership":'own_type'}
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
        "Lower Salary",
        "Upper Salary",
        'Age'
    ]
    df = df.drop(columns=columns_to_drop).rename(columns=rename_dict)
    df.columns = df.columns.str.lower()
    df.seniority.replace(['na', 'jr', 'sr'], ['Other', 'Other', 'Senior'], inplace=True)
    df.degree.replace(['na', 'M', 'P'], ['Not Available', 'Master', 'PhD'], inplace=True)
    df.company_revenue.replace(revenue_list, new_revenue_list, inplace=True)
    df = df.assign(skill_num=lambda x: sum([x[a] for a in skills]))
    df = df[(df.sector != '-1') * (df.industry != '-1') * (df['size'] != 'unknown') * (df.rating >= 0)]
    return df


def df_aggregate_by(param):
    def f(x):
        def get_several_lined_string(series):
            lst = []
            for i in range(0, len(series), 5):
                lst.append(', '.join(series[i:8 + i]))
            return ',\n'.join(lst)

        companies_txt = get_several_lined_string(x.company.unique())
        jobs_txt = get_several_lined_string(x.job.unique())
        ### FROM: https://stackoverflow.com/questions/17841149/pandas-groupby-how-to-get-a-union-of-strings
        dct = {skill: round(x[skill].mean(), 3) for skill in skills}
        dct['companies'] = companies_txt
        dct['jobs'] = jobs_txt
        ### ENF FROM
        return pd.Series(dct)

    param_agg = (wage_df.groupby(param)
                 .apply(f)
                 .reset_index()
                 )
    return param_agg.melt(id_vars=[param, 'companies', 'jobs'])


def get_data_for_ranking(name, highlight, over):
    agg_dict = {'industry': industry_agg, 'sector': sector_agg, 'skill': sector_agg}
    agg = agg_dict[over]
    if over == 'skill':
        skill_or_sector = 'sector'
        label = f'Частота использования {name.capitalize()}'
    else:
        skill_or_sector = 'skill'
        label = f'Частота использования в {name}'
    df = agg[agg[over] == name].sort_values(by='share', ascending=False)
    highlight_total = (np.array([df[skill_or_sector] ==
                                 hl for hl in highlight]).sum(axis=0)
                       if highlight != []
                       else np.ones(df[skill_or_sector].shape))
    color = np.where(highlight_total, '#F66B0E', '#205375')
    sizes = np.where(highlight_total, 200, 100)
    ranking_dict = {'df': df,
                    'skill_or_sector': skill_or_sector,
                    'label': label, 'color': color, 'sizes': sizes}
    return ranking_dict


def get_data_for_corr(param):
    x1, y1, x2, y2 = 0, 0, 0, 0
    order = list()
    x_label = ''
    if param == 'skill_num':
        x1, y1, x2, y2 = 1.1, 127, 0.2, 88.5
        order = list(range(11))
        x_label = 'Number of skills from the list'
    elif param == 'company_revenue':
        x1, y1, x2, y2 = 1.1, 170, 0.2, 120
        order = new_revenue_list
        x_label = 'Company Revenue'
    elif param == 'company_size':
        x1, y1, x2, y2 = 0.3, 150, 0.2, 105
        order = new_size_list[:-1]
        x_label = 'Company Size'
    elif param == 'rating':
        x1, y1, x2, y2 = 4.8, 50, 2.35, 112
        order = sorted(wage_df.rating.unique())
        x_label = 'Company Rating'
    return {'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2, 'order': order, 'x_label': x_label}


skills = ['python', 'spark', 'aws', 'excel', 'sql', 'sas', 'keras',
          'pytorch', 'scikit', 'tensor', 'hadoop', 'tableau',
          'bi', 'flink', 'mongo', 'google_an']
revenue_list = [
    'Less than $1 million (USD)', '$1 to $5 million (USD)',
    '$5 to $10 million (USD)', '$10 to $25 million (USD)',
    '$25 to $50 million (USD)', '$50 to $100 million (USD)', '$100 to $500 million (USD)',
    '$500 million to $1 billion (USD)', '$1 to $2 billion (USD)',
    '$2 to $5 billion (USD)', '$5 to $10 billion (USD)',
    '$10+ billion (USD)', 'Unknown / Non-Applicable']
new_revenue_list = ['NA', '<$1M', '$1M-$5M', '$5M-$10M', '$10M-$25M', '$25M-$50M', '$50M-$100M',
                    '$100M-$500M', '$500M-$1B', '$1B-$2B', '$2B-$5B', '$5-$10B', '$10B+']
size_list = ['1 - 50 ', '51 - 200 ', '201 - 500 ', '501 - 1000 ', '1001 - 5000 ', '5001 - 10000 ', '10000+ ']
new_size_list = ['1-50', '51-200', '201-500', '501-1000', '1001-5000', '5001-10000', '10000+']
wage_df = get_dataframe().rename(columns={'size': 'company_size'}).replace(size_list, new_size_list)
industry_agg = df_aggregate_by('industry').rename(columns={'variable': 'skill', 'value': 'share'})
sector_agg = df_aggregate_by('sector').rename(columns={'variable': 'skill', 'value': 'share'})