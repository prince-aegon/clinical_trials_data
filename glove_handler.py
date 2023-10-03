import pandas as pd
import numpy as np
df = pd.read_csv("output1.csv")

glove_model_path = "glove.6B.50d.txt\glove.6B.50d.txt"
word_vectors = {}
new_glove = []
with open(glove_model_path, encoding="utf-8") as f:
    for line in f:
        values = line.split()
        word = values[0]
        vector = np.asarray(values[1:], dtype="float32")
        word_vectors[word] = vector
for text_data in df['text']:
    input_text = text_data
    tokens = input_text.lower().split()
    text_vector = np.mean([word_vectors.get(token, np.zeros(50)) for token in tokens], axis=0)
    new_glove.append(text_vector)
df['glove_values'] = new_glove

max_list_length = max(df['glove_values'].apply(len))
column_names = [f'glove{i+1}' for i in range(max_list_length)]

df[column_names] = pd.DataFrame(df['glove_values'].to_list(), index=df.index)
# df.drop('glove_values', axis=1, inplace=True)
df.to_csv('output1.csv')