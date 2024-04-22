import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def draw_violin_sh_schemes_parts(resfile, outfilename):
    df = pd.read_csv(resfile, skiprows=1, header=None)

    df = df.loc[:,[0,5]]

    df_dict = {}
    for k, g in df.groupby([0]):
        df_dict[k[0]] = g[5].values.tolist()

    df = pd.DataFrame(df_dict)

    df.columns = ['NO-shuffle','RCW-shuffle', 'DRW-shuffle','SLW-shuffle']
    df = df[['DRW-shuffle', 'SLW-shuffle']]
    df.columns = ['DRW-shuffle','SLW-shuffle'] 
    
    labels_x = []
    labels_x.append(None)
    labels_x.append(None)
    labels_x.append(None)   
    for i in df.columns.values.tolist():
        labels_x.append(i)
        labels_x.append(None)

    csfont = {'fontname':'Times New Roman'}
    hfont = {'fontname':'Helvetica'}

    fig, axes = plt.subplots(figsize=(12, 6))
    axes.violinplot(dataset = df)
    # Scale down the x-axis by reducing the range by half
    plt.xlim(-0.5, 3)
    # axes.set_title('Comparing Shuffling Methods')
    axes.yaxis.grid(True)
    axes.set_xlabel('Shuffling Scheme', weight = 'bold', **csfont, fontsize=24)

    axes.tick_params(axis="y",direction="in")
    axes.tick_params(axis="x",direction="in")

    plt.xticks(fontsize=20, **csfont)
    plt.yticks(fontsize=20, **csfont)

    axes.grid(axis='y', linestyle='--')

    axes.set_ylabel('Part Number Access Count', weight = 'bold', **csfont, fontsize=24)
    axes.set_xticklabels(labels_x)
    
    fig.savefig(outfilename + '.eps', format='eps', bbox_inches='tight')
    fig.savefig(outfilename + '.jpeg', format='jpeg', dpi=300, bbox_inches='tight')
    fig.savefig(outfilename + '.pdf', format='pdf', bbox_inches='tight')
    fig.savefig(outfilename + '.svg', format='svg', bbox_inches='tight')


    # plt.show()

