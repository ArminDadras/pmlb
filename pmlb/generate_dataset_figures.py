# -*- coding: utf-8 -*-

"""
PMLB was primarily developed at the University of Pennsylvania by:
    - Randal S. Olson (rso@randalolson.com)
    - William La Cava (lacava@upenn.edu)
    - Weixuan Fu (weixuanf@upenn.edu)
    - Trang Le (ttle@pennmedicine.upenn.edu)
    - and many more generous open source contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from pmlb import fetch_data
from .dataset_lists import (classification_dataset_names, 
                            regression_dataset_names)
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import operator

def plot_corr(dataset, df):
    if df.shape[0] > 1000:
        df = df.sample(n=1000, axis=0)
    max_cols = 20
    # plot most correlated features
    corrs = {col:
	np.square(np.corrcoef(df['target'],df[col])[0,1]) for col in df.columns
	    }
    corrs = {k:v for k,v in corrs.items() if not np.isnan(v)}
    sorted_corrs = sorted(corrs.items(), key=operator.itemgetter(1))[::-1]
    print('sorted_corrs:',sorted_corrs[:max_cols])
    order = [sc[0] for sc in sorted_corrs[:max_cols]]
    order.remove('target')
    order += ['target']
    df = df[order]
    # make correlation plot 
    corr = np.square(df.corr())
    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask,k=0)] = True

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    g = plt.figure()
    sns.heatmap(corr, mask=mask, cmap=cmap,  center=0,
                square=True, linewidths=.5, 
                cbar_kws={"shrink": .5,
                          'label':'Square Corr. Coef'},
                xticklabels=[k.lower() for k in df.columns],
                yticklabels=[k.lower() for k in df.columns]
                )
    plt.gca().tick_params(axis='both', which='major', labelsize=8)
    plt.title('Pairwise Correlations')
    g.tight_layout()
    return g

def plot_label(dataset, y, problem_type,ax):
    """Plot label distribution"""
    print('plotting',dataset)
    if problem_type == 'classification':
        # then do a bar plot
        classes = list(np.sort(y.unique()))
        bins = sorted([c-0.25 for c in classes]+[c+0.25 for c in classes])
        print(bins)
#         bins = [-0.25, 0.25, 0.75, 1.25]
        ax = sns.distplot(y, kde=False, 
                          bins = bins, hist_kws={'align':'mid'})
        ax.set_xticks(np.sort(y.unique()))
    elif problem_type == 'regression':
        ax = sns.distplot(y, kde=False)
    plt.title('Target Values')
    plt.ylabel('Samples')
    plt.xlabel('')
    plt.tight_layout()
    return plt.gcf()

def make_plots(dataset, y, problem_type):
    h = plt.figure() #figsize=(8,4))
#     ax = h.add_subplot(1,2,1)
    ax = h.gca()
    plot_label(dataset, df['target'], problem_type, ax)
    g = plot_corr(dataset, df)
    return h, g
    
    

if __name__ =='__main__':

    local_dir = 'datasets/'
    names = {
	'regression': regression_dataset_names,
	'classification': classification_dataset_names
    #     'regression': regression_dataset_names[:5],
    #     'classification': classification_dataset_names[:5]
    }

    for problem_type in ['classification','regression']:
        for dataset in names[problem_type]:
            df = fetch_data(dataset, local_cache_dir = local_dir)
            fig1, fig2 = make_plots(dataset, df['target'], problem_type)
            fig1.savefig(local_dir+ '/'+dataset+'/label.svg',dpi=300) 
            fig2.savefig(local_dir+ '/'+dataset+'/corr.svg',dpi=300) 
