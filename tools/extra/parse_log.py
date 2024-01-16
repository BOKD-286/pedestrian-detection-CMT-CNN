#!/usr/bin/env python

"""
Parse training log

Evolved from parse_log.sh
"""

import os
import re
import extract_seconds
import argparse
import csv
from collections import OrderedDict


def parse_log(path_to_log):
    """Parse log file
    Returns (train_dict_list, train_dict_names, test_dict_list, test_dict_names)

    train_dict_list and test_dict_list are lists of dicts that define the table
    rows

    train_dict_names and test_dict_names are ordered tuples of the column names
    for the two dict_lists
    """

    regex_iteration = re.compile('Iteration (\d+)')
    regex_train_output = re.compile('Train net output #(\d+): (\S+) = ([\.\deE+-]+)')
    regex_test_output = re.compile('Test net output #(\d+): (\S+) = ([\.\deE+-]+)')
    regex_learning_rate = re.compile('lr = ([\.\d]+)')

    # Pick out lines of interest
    iteration = -1
    learning_rate = float('NaN')
    train_dict_list = []
    test_dict_list = []
    train_row = None
    test_row = None

    logfile_year = extract_seconds.get_log_created_year(path_to_log)
    with open(path_to_log) as f:
        start_time = extract_seconds.get_start_time(f, logfile_year)

        for line in f:
            iteration_match = regex_iteration.search(line)
            if iteration_match:
                iteration = float(iteration_match.group(1))
            if iteration == -1:
                # Only start parsing for other stuff if we've found the first
                # iteration
                continue

            time = extract_seconds.extract_datetime_from_line(line,
                                                              logfile_year)
            seconds = (time - start_time).total_seconds()

            learning_rate_match = regex_learning_rate.search(line)
            if learning_rate_match:
                learning_rate = float(learning_rate_match.group(1))

            train_dict_list, train_row = parse_line_for_net_output(
                regex_train_output, train_row, train_dict_list,
                line, iteration, seconds, learning_rate
            )
            test_dict_list, test_row = parse_line_for_net_output(
                regex_test_output, test_row, test_dict_list,
                line, iteration, seconds, learning_rate
            )

    fix_initial_nan_learning_rate(train_dict_list)
    fix_initial_nan_learning_rate(test_dict_list)

    return train_dict_list, test_dict_list


def parse_line_for_net_output(regex_obj, row, row_dict_list,
                              line, iteration, seconds, learning_rate):
    """Parse a single line for training or test output

    Returns a a tuple with (row_dict_list, row)
    row: may be either a new row or an augmented version of the current row
    row_dict_list: may be either the current row_dict_list or an augmented
    version of the current row_dict_list
    """

    output_match = regex_obj.search(line)
    if output_match:
        if not row or row['NumIters'] != iteration:
            # Push the last row and start a new one
            if row:
                # If we're on a new iteration, push the last row
                # This will probably only happen for the first row; otherwise
                # the full row checking logic below will push and clear full
                # rows
                row_dict_list.append(row)

            row = OrderedDict([
                ('NumIters', iteration),
                ('Seconds', seconds),
                ('LearningRate', learnin