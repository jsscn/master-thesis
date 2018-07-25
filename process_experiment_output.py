import json
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

if 'rules' in df:
    df.drop(['rules'], axis='columns', inplace=True)

    f.seek(0)

    j = json.load(f)

    # confidence_threshodls = j[0]['rules']

    rules_only = defaultdict(list)
    for run in j:
        for rules_run in run['rules']:
            threshold = round(float(rules_run['confidence-threshold']), 3)
            rules_only['duration-{}'.format(threshold)].append(rules_run['duration-s'])
            rules_only['num-confident-association-rules-{}'.format(threshold)].append(rules_run['num-confident-association-rules'])

    new_columns = pd.DataFrame(rules_only)
    
    df = pd.concat([df, new_columns], axis=1)

f.close()

(name, ext) = os.path.splitext(args.file_path)

for (episode_class, frequency_measure, window_width) in \
        itertools.product(df['episode-class'].unique(), df['frequency-measure'].unique(), df['window-width'].unique()):

    subdf = df[(df['episode-class'] == episode_class) & (df['frequency-measure'] == frequency_measure) & (df['window-width'] == window_width) & (df['status'] != 'too-many-candidates')]

    subdf.to_csv('{}-{}-{}-{}.tsv'.format(name, episode_class, frequency_measure, window_width), index=False, sep='\t')

# df.to_csv('out.dat', index=False, sep='\t')

#print(json_data)

