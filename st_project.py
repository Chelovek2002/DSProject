import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
from sns_plots import sns_ranking, sns_wage_corr
from dataframe_tidied import wage_df, skills
from alt_plots import alt_ranking, alt_wage_corr
from plt_plots import plt_ranking

with st.echo(code_location='below'):
    """
    ## Start
    """


    def print_hello(name="World"):
        st.write(f"### Hello, {name}!")


    name = st.text_input("Your name", key="name", value="Anonymous")
    print_hello(name)

    """
    ## Добавим графики
    Чтобы заработали библиотеки seaborn и altair, нужно добавить в проект файл 
    `requirements.txt` с такими строчками:

        seaborn
        altair
    """

    """
    ## Немного анализа данных
    """

    selector_1 = st.selectbox("What are we ranking?",
                              ('Skills over a Sector', 'Skills over an Industries', 'Sectors over a Skill'))
    if selector_1 == 'Skills over a Sector':
        selector = st.selectbox("Sector", wage_df.sector.unique())
        highlight = st.multiselect("What skills would you like to highlight?", skills)
        over = 'sector'
    elif selector_1 == 'Skills over an Industries':
        selector = st.selectbox("Industry", wage_df.industry.unique())
        highlight = st.multiselect("What skills would you like to highlight?", skills)
        over = 'industry'
    elif selector_1 == 'Sectors over a Skill':
        selector = st.selectbox("Skill", skills)
        highlight = st.multiselect("What sector would you like to highlight?", wage_df.sector.unique())
        over = 'skill'
    ### FROM: https://discuss.streamlit.io/t/horizontal-radio-buttons/2114/8
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>',
             unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>',
             unsafe_allow_html=True)
    ### END FROM
    rank_lib = st.radio("Plotting library", ("Seaborn", "Altair", "Matplotlib"))


    def customize_axis(ax):
        ax.xaxis.label.set_color('#EFEFEF')
        ax.yaxis.label.set_color('#EFEFEF')
        ax.tick_params(axis='x', colors='#EFEFEF')
        ax.grid(visible=True, axis='x', color='#205375')
        ax.grid(visible=False, axis='y')


    if rank_lib == 'Seaborn':
        fig, ax = plt.subplots(figsize=(8, 8))
        sns_ranking(selector, highlight, over)
        customize_axis(ax)
        st.pyplot(fig, True)
    elif rank_lib == 'Altair':
        chart = alt_ranking(selector, highlight, over)
        st.altair_chart(chart.interactive())
    elif rank_lib == 'Matplotlib':
        fig, ax = plt.subplots(figsize=(8, 8))
        plt_ranking(selector, highlight, over)
        customize_axis(ax)
        st.pyplot(fig, True)
    """
    New_plot
    """

    corr = st.selectbox("Choose parameter to correlate.",
                        ('Number of skills', 'Company Revenue', 'Company Size', 'Company Rating'))
    if corr == 'Number of skills':
        parameter = 'skill_num'
    elif corr == 'Company Revenue':
        parameter = 'company_revenue'
    elif corr == 'Company Size':
        parameter = 'company_size'
    elif corr == 'Company Rating':
        parameter = 'rating'

    ### FROM: https://discuss.streamlit.io/t/horizontal-radio-buttons/2114/8
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>',
             unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>',
             unsafe_allow_html=True)
    ### END FROM
    corr_lib = st.radio("Plotting library", ("Seaborn", "Altair"))
    if corr_lib == 'Seaborn':
        fig, ax = plt.subplots(figsize=(10, 5))
        sns_wage_corr(parameter)
        customize_axis(ax)
        ax.tick_params(axis='y', colors='#EFEFEF')
        plt.xticks(rotation=30)
        ax.legend_ = None
        if parameter == 'rating':
            for label in ax.xaxis.get_ticklabels()[::2]:
                label.set_visible(False)
            plt.xticks(rotation=0)
        st.pyplot(fig, True)

    elif corr_lib == 'Altair':
        chart = alt_wage_corr(parameter)
        st.altair_chart(chart.interactive(), use_container_width=True)

    st.dataframe(wage_df)