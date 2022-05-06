from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap, factor_mark
from dataframe_tidied import wage_df, industry_agg, sector_agg, skills
from bokeh.palettes import Spectral5


def bokeh_wage_correlation():
    seniority = sorted(wage_df.seniority.unique())
    markers = ['hex', 'circle_x', 'triangle']

    p = figure(title="Salary", background_fill_color="#fafafa")
    p.yaxis.axis_label = 'Average Salary'
    p.xaxis.axis_label = 'Number of skills fom the list'

    p.scatter("skill_num", "avg_salary", source=wage_df,
              legend_group="seniority", fill_alpha=0.2, size=12,
              marker=factor_mark('seniority', markers, seniority),
              color=factor_cmap('seniority', 'Category10_3', seniority))
    seniority_avg = list()
    for seniority_type in ['Not Available', 'Senior']:
        individual_avg = list()
        for s_num in range(11):
            condition = (wage_df.skill_num == s_num) * (wage_df.seniority == seniority_type)
            individual_avg.append(wage_df[condition].avg_salary.mean())
        seniority_avg.append(individual_avg)
    for lst in seniority_avg:
        p.line(x=list(range(11)), y=lst, color="red", line_width=2)
    p.legend.location = "top_left"
    p.legend.title = "Salary"

    show(p)


def bokeh_ranking(name, highlight, over):
    agg_dict = {'industry': industry_agg, 'sector': sector_agg, 'skill': sector_agg}
    agg = agg_dict[over]
    skill_or_sector = 'sector' if over == 'skill' else 'skill'
    data = agg[agg[over] == name].sort_values(by='share', ascending=False)

    p = figure(x_range=data[skill_or_sector], plot_width=800, plot_height=250, y_range=(0, 1), title=name)
    p.vbar(x=skill_or_sector, top='share', width=0.9, source=data)

    p.xaxis.major_label_orientation = 0.3
    p.xgrid.grid_line_color = None
    p.x_range.range_padding = 0.1
    show(p)


bokeh_ranking(wage_df.loc[3, 'sector'], 'python', 'sector')