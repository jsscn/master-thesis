import json
import pandas
import argparse
import sys
import os
import itertools

parser = argparse.ArgumentParser()

parser.add_argument('file_path')

args = parser.parse_args()

f = open(args.file_path)

df = pandas.read_json(f)
f.close()

(name, ext) = os.path.splitext(args.file_path)

for (episode_class, frequency_measure, window_width) in \
        itertools.product(df['episode-class'].unique(), df['frequency-measure'].unique(), df['window-width'].unique()):
    
    df.drop(['rules'], inplace=True)
    subdf = df[(df['episode-class'] == episode_class) & (df['frequency-measure'] == frequency_measure) & (df['window-width'] == window_width) & (df['status'] != 'too-many-candidates')]

    subdf.to_csv('{}-{}-{}-{}.tsv'.format(name, episode_class, frequency_measure, window_width), index=False, sep='\t')

# df.to_csv('out.dat', index=False, sep='\t')

#print(json_data)

