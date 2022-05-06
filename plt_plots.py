import matplotlib.pyplot as plt
import numpy as np
from dataframe_tidied import wage_df, get_data_for_ranking


def plt_ranking(name, highlight, over):
    plt.rcParams.update({'font.size': 19
                         })
    data = get_data_for_ranking(name, highlight, over)
    df = data['df'].iloc[::-1]
    skill_or_sector = data['skill_or_sector']
    ### FROM:'https://python-graph-gallery.com/183-highlight-a-group-in-lollipop'
    plt.hlines(y=df[skill_or_sector], xmin=0, xmax=df.share, color=np.flip(data['color']), alpha=1, linewidth=3)
    plt.scatter(x=df.share, y=df[skill_or_sector], color=np.flip(data['color']), s=np.flip(data['sizes']), alpha=1)
    ### END FROM
    plt.xlabel(data['label'])
    plt.ylabel(skill_or_sector.capitalize())
    for i, color in enumerate(np.flip(data['color'])):
        plt.gca().get_yticklabels()[i].set_color(color)


