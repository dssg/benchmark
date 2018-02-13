# coding: utf-8

import matplotlib
matplotlib.use('Agg')

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.dates as md

import seaborn as sns
sns.set_style("white")
sns.set_context("paper")
sns.set_style("ticks")

from functools import reduce

from datetime import datetime
from dateutil.relativedelta import relativedelta

import triage.component.timechop as timechop
from triage.util.conf import convert_str_to_relativedelta


FIG_SIZE = (32,16)

def show_timechop(chopper, show_as_of_times=True, show_boundaries=True, file_name=None):

    plt.close('all')

    chops = chopper.chop_time()

    chops.reverse()

    fig, ax = plt.subplots(len(chops), sharex=True, sharey=True, figsize=FIG_SIZE)


    for idx, chop in enumerate(chops):
        train_as_of_times = chop['train_matrix']['as_of_times']
        test_as_of_times = chop['test_matrices'][0]['as_of_times']

        max_training_history = chop['train_matrix']['max_training_history']
        test_label_timespan = chop['test_matrices'][0]['test_label_timespan']
        training_label_timespan = chop['train_matrix']['training_label_timespan']

        color_rgb = np.random.random(3)

        if(show_as_of_times):
            # Train matrix (as_of_times)
            ax[idx].hlines(
              [x for x in range(len(train_as_of_times))],
              [x.date() for x in train_as_of_times],
              [x.date() + convert_str_to_relativedelta(training_label_timespan) for x in train_as_of_times],
              linewidth=3, color=color_rgb,label=f"train_{idx}"
            )

            # Test matrix
            ax[idx].hlines(
              [x for x in range(len(test_as_of_times))],
              [x.date() for x in test_as_of_times],
              [x.date() + convert_str_to_relativedelta(test_label_timespan) for x in test_as_of_times],
              linewidth=3, color=color_rgb,
              label=f"test_{idx}"
            )


        if(show_boundaries):
            # Limits: train
            ax[idx].axvspan(chop['train_matrix']['first_as_of_time'],
                            chop['train_matrix']['last_as_of_time'],
                            color=color_rgb,
                            alpha=0.3
            )


            ax[idx].axvline(chop['train_matrix']['matrix_info_end_time'], color='k', linestyle='--')


            # Limits: test
            ax[idx].axvspan(chop['test_matrices'][0]['first_as_of_time'],
                            chop['test_matrices'][0]['last_as_of_time'],
                            color=color_rgb,
                            alpha=0.3
            )

            ax[idx].axvline(chop['feature_start_time'], color='k', linestyle='--', alpha=0.2)
            ax[idx].axvline(chop['feature_end_time'], color='k', linestyle='--',  alpha=0.2)
            ax[idx].axvline(chop['label_start_time'] ,color='k', linestyle='--', alpha=0.2)
            ax[idx].axvline(chop['label_end_time'] ,color='k', linestyle='--',  alpha=0.2)

            ax[idx].axvline(chop['test_matrices'][0]['matrix_info_end_time'],color='k', linestyle='--')

        ax[idx].yaxis.set_major_locator(plt.NullLocator())
        ax[idx].yaxis.set_label_position("right")
        ax[idx].set_ylabel(f"Block {idx}", rotation='horizontal', labelpad=30)

        ax[idx].xaxis.set_major_formatter(md.DateFormatter('%Y'))
        ax[idx].xaxis.set_major_locator(md.YearLocator())
        ax[idx].xaxis.set_minor_locator(md.MonthLocator())

#        fig.autofmt_xdate()

    ax[0].set_title('Timechop: Temporal cross-validation blocks')
    fig.subplots_adjust(hspace=0)
    plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)

    if file_name is not None:
        fig.savefig(file_name)

    plt.show()


def show_features_queries(st):

    for sql_list in st.get_selects().values():
        for sql in sql_list:
            print(str(sql))

    print(str(st.get_create()))
