# -*- coding: utf-8 -*-
"""오사카_추천시스템.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1K-ZZ5pdxprTjmsqIez-ho4FBUxLdInl4
"""

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import json

def att_recommend(attraction_name = 'user', path = '', input_keyword=''):
  final_data = pd.read_csv(path)

  label = ['간사이 공항', '오사카 국제공항']
  index = []

  for i in label:
    index.append(final_data[final_data.Name == i].index[0])

  final_data_1 = final_data.drop(index, axis=0)
  final_data_1 = final_data_1.reset_index()

  df1 = pd.DataFrame(columns=range(2))
  df1.columns = ['Name', 'keyword']

  df1.Name = final_data_1.Name
  df1.keyword = final_data_1.keyword
  df1.loc[len(df1)] = ['user', input_keyword]

  count_vect = CountVectorizer(min_df=0, ngram_range=(1,2))
  matrixs = count_vect.fit_transform(df1['keyword'])

  cosine_matrix = cosine_similarity(matrixs, matrixs)

  # 관광지 title와 id를 매핑할 dictionary를 생성해줍니다.
  att2id = {}
  for i, c in enumerate(df1['Name']): att2id[i] = c

  # id와 관광지 title를 매핑할 dictionary를 생성해줍니다.
  id2att = {}
  for i, c in att2id.items(): id2att[c] = i

  idx = id2att[attraction_name]
  sim_scores = [(i, c) for i, c in enumerate(cosine_matrix[idx]) if i != idx] # 자기 자신을 제외한 관광지들의 유사도 및 인덱스를 추출
  sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse=True) # 유사도가 높은 순서대로 정렬
  sim_scores = [(att2id[i], score) for i, score in sim_scores[0:10]]

  attraction = []

  for i in range(len(sim_scores)):
    box = list(sim_scores[i])
    attraction.append(box[0])

  return attraction

