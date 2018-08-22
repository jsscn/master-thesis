import json
import numpy as np
import pandas as pd
import argparse
import sys
import os
import itertools
from collections import defaultdict

parser = argparse.ArgumentParser()

parser.add_argument('file_path')

args = parser.parse_args()

f = open(args.file_path)

df = pd.read_json(f)

f.seek(0)
j = json.load(f)

df.drop(['num-frequent-episodes-of-size', 'num-candidates-of-size'], axis='columns', inplace=True)

largest_episode_size = max(len(run['num-frequent-episodes-of-size']) for run in j)

columnize_frequent_episode_counts = defaultdict(list)

for run in j:
    for i in range(largest_episode_size):
        episode_counts = run['num-frequent-episodes-of-size']

        columnize_frequent_episode_counts['num-frequent-{}-episodes'.format(i + 1)].append(
                episode_counts[i] if i < len(episode_counts) else 0)

df = pd.concat([df, pd.DataFrame(columnize_frequent_episode_counts)], axis=1)

if 'rules' in df:
    df.drop(['rules'], axis='columns', inplace=True)

    # confidence_threshodls = j[0]['rules']

    rules_only = defaultdict(list)
    for run in j:
        if run['status'] == 'too-many-candidates':
            # note: if very first experiment is too many candidates, this won't work (rules_only won't have been initialized properly yet)
            for k, l in rules_only.items():
                l.append(0)
        else:
            for rules_run in run['rules']:
                threshold = round(float(rules_run['confidence-threshold']), 3)
                rules_only['duration-rules-{}'.format(threshold)].append(rules_run['duration-s'])
                rules_only['num-confident-rules-{}'.format(threshold)].append(rules_run['num-confident-rules'])

    new_columns = pd.DataFrame(rules_only)
    
    print(new_columns)
    print(df)

    df = pd.concat([df, new_columns], axis=1)

f.close()

df = df[df['status'] != 'too-many-candidates']

df['percentage-frequent-of-candidates'] = df.apply(lambda frame: frame['num-frequent-episodes'] / frame['num-candidates'], axis=1)

(name, ext) = os.path.splitext(args.file_path)

for (episode_class, frequency_measure, window_width) in \
        itertools.product(df['episode-class'].unique(), df['frequency-measure'].unique(), df['window-width'].unique()):

    subdf = df[(df['episode-class'] == episode_class) & (df['frequency-measure'] == frequency_measure) & (df['window-width'] == window_width)]

    subdf.to_csv('{}-{}-{}-{}.tsv'.format(name, episode_class, frequency_measure, window_width), index=False, sep='\t')

# df.to_csv('out.dat', index=False, sep='\t')

#print(json_data)

