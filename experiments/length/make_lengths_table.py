import json
import pandas as pd
import itertools
import code

files = [open('tolstoy-lengths-{}.json'.format(i)) for i in range(1, 11)]
jsons = [json.load(f) for f in files]
for f in files: f.seek(0)
dfs = [pd.read_json(f) for f in files]
for f in files: f.close()

frequency_measures = dfs[0]['frequency-measure'].unique()
episode_classes = dfs[0]['episode-class'].unique()

for episode_class, frequency_measure in itertools.product(episode_classes, frequency_measures):
    smallest_common_threshold = max(df[(df['episode-class'] == episode_class) & (df['frequency-measure'] == frequency_measure) & (df['status'] == 'success')].min()['frequency-threshold'] for df in dfs)

    df = pd.DataFrame([df[(df['episode-class'] == episode_class) & (df['frequency-measure'] == frequency_measure) & (df['frequency-threshold'] == smallest_common_threshold)].iloc[0] for df in dfs])
    portions = pd.DataFrame({'portion': [i / 10 for i in range(1, 11)]})
    df.reset_index(inplace=True)
    df = pd.concat([portions, df], axis=1)
    df.drop(['num-frequent-episodes-of-size', 'num-candidates-of-size'], inplace=True, axis='columns')

    df.to_csv('tolstoy-lengths-{}-{}.dat'.format(episode_class, frequency_measure), index=False, sep='\t')
