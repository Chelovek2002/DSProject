import altair as alt
import altair_viewer
import numpy as np
from dataframe_tidied import wage_df, get_data_for_ranking, get_data_for_corr


def alt_df_aggregate_by(param):
    param_agg = (wage_df.groupby(param)
                 .mean()
                 .drop(columns=['rating', 'skill_num', 'avg_salary'])
                 .reset_index()
                 )
    return param_agg.melt(id_vars=param)


# correlation between wage and degree for various seniority
def alt_show_wage_degree_corr():
    chart = alt.Chart(wage_df).mark_boxplot().encode(
        alt.X('seniority:O'),
        alt.Y('avg_salary:Q'),
        color='seniority:O', column='degree:O',
        tooltip=['company', 'revenue', 'avg_salary', 'job']
    ).interactive()
    altair_viewer.show(chart)


def alt_wage_corr(param):
    order = get_data_for_corr(param)['order']
    base = alt.Chart(wage_df).mark_circle(opacity=0.5).encode(
        alt.X(param, sort=order, axis=alt.Axis(labelAngle=-20)),
        alt.Y('avg_salary'),
        alt.Color('seniority'),
        tooltip=['company', 'company_revenue', 'avg_salary', 'job', 'company_size', 'own_type']
    )

    if param == 'rating' or param == 'skill_num':
        line = base.transform_loess(param, 'avg_salary', groupby=['seniority']).mark_line()
    else:
        key = dict(zip(order, range(len(order)))) if param != 'rating' else dict(zip(order, order))
        source = wage_df.assign(order=lambda x: x[param].map(key))
        line = alt.Chart(source).mark_line().encode(
            x=alt.X('order'),
            y=alt.Y('mean(avg_salary)'),
            color=alt.Color('seniority')
        )

    return base + line


def alt_ranking(name, highlight, over):
    data = get_data_for_ranking(name, highlight, over)
    condition_bars = alt.condition(
        alt.FieldOneOfPredicate(data['skill_or_sector'], highlight),
        alt.value('#F66B0E'),
        alt.value('#205375'))
    condition_text = (
        alt.condition(
            alt.FieldOneOfPredicate(data['skill_or_sector'], highlight),
            alt.value('#F66B0E'),
            alt.value('#EFEFEF')
        )
    )
    y = alt.Y(data['skill_or_sector'], sort='-x', axis=alt.Axis(labelColor='#EFEFEF', titleColor='#EFEFEF'))
    x = alt.X('share', axis=alt.Axis(labelColor='#EFEFEF', titleColor='#EFEFEF'))
    chart = alt.Chart(data['df']).mark_bar().encode(
        y=y, x=x, color=condition_bars,
        tooltip=[alt.Tooltip('jobs', title='Jobs in Sector/Industry')]
    ).properties(width=600)
    text = chart.mark_text(
        align='left', baseline='middle', dx=3
    ).encode(
        text='share', color=condition_text
    )
    return (chart + text).configure(background='#112B3C')
