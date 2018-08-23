import json
import pandas as pd
import itertools
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('files', nargs="+")

args = parser.parse_args()

files = [open(fname) for fname in args.files]
jsons = [json.load(f) for f in files]
for f in files: f.seek(0)
dfs = [pd.read_json(f) for f in files]
for f in files: f.close()

frequency_measures = dfs[0]['frequency-measure'].unique()
episode_classes = dfs[0]['episode-class'].unique()

for episode_class, frequency_measure in itertools.product(episode_classes, frequency_measures):
    smallest_common_threshold = max(df[(df['episode-class'] == episode_class) & (df['frequency-measure'] == frequency_measure) & (df['status'] == 'success')].min()['frequency-threshold'] for df in dfs)

    print('{} {}: {}'.format(episode_class, frequency_measure, smallest_common_threshold))
