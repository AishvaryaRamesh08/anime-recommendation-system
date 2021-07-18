import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
import numpy


df = pd.read_csv('animes_cleaned.csv')

df['genre'] = df['genre'].apply(lambda x: x[1:-1])
df['genre'] = df['genre'].str.replace(' ', '')
features_df = df["genre"].str.get_dummies(sep=",")
features_df['episodes'] = df['episodes']
features_df['members'] = df['members']

features_df['score'] = df['score']
min_max_scaler = MinMaxScaler()
features_df = min_max_scaler.fit_transform(features_df)

nbrs = NearestNeighbors(n_neighbors=15, algorithm='ball_tree').fit(features_df)
distances, indices = nbrs.kneighbors(features_df)

df = pd.DataFrame(indices)
df.to_csv('indices.csv', index=False)
