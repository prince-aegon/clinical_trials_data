# import torch
# from transformers import AutoTokenizer, AutoModel

# model_name = "dmis-lab/biobert-v1.1"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModel.from_pretrained(model_name)

# text = "Determine the safety and toxicity of preoperative trastuzumab (Herceptin) and&#xD; paclitaxel followed by postoperative doxorubicin and cyclophosphamide in women with locally&#xD; advanced breast cancer with HER2 overexpression. II. Determine tumor response in these&#xD; patients treated with this regimen. III. Assess the effect of this regimen on tumor histology&#xD; and the potential molecular determinants of response in these patients dxjgbjabg kj's;atnfjk; sd jewgain;ion kowetjgokaeag e orjmgrjpokpermg ]samgplaer pertykep dporykpreyk drykkyp[5kyup[ oijtop]]grew    estyojy erokperryk ryes[k[pseym ]] sy5iput qewu8yhpiuef qthuiupewtn    Determine the safety and toxicity of preoperative trastuzumab (Herceptin) and&#xD; paclitaxel followed by postoperative doxorubicin and cyclophosphamide in women with locally&#xD; advanced breast cancer with HER2 overexpression. II. Determine tumor response in these&#xD; patients treated with this regimen. III. Assess the effect of this regimen on tumor histology&#xD; and the potential molecular determinants of response in these patients dxjgbjabg kj's;atnfjk; sd jewgain;ion kowetjgokaeag e orjmgrjpokpermg ]samgplaer pertykep dporykpreyk drykkyp[5kyup[ oijtop]]grew    estyojy erokperryk ryes[k[pseym ]] sy5iput qewu8yhpiuef qthuiupewtn"
# # inputs = tokenizer(text, return_tensors="pt")
# inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)

# with torch.no_grad():
#     outputs = model(**inputs)
#     embeddings = outputs.last_hidden_state  # This contains the embeddings for all tokens in the input text

# features = embeddings.mean(dim=1)  
# print(features.size())


import torch
from transformers import AutoTokenizer, AutoModel
import pandas as pd
# Load the BioBERT tokenizer and model
# model_name = "monologg/biobert_v1.1_pubmed"
model_name = "dmis-lab/biobert-v1.1"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)


df = pd.read_csv("outputCpy.csv")


# # Define the input text
# text = "This is a sample text for vector extraction using BioBERT."

# # Tokenize and encode the text
# inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)

# # Pass the input through the model to get embeddings
# with torch.no_grad():
#     outputs = model(**inputs)

# # Extract embeddings from the output
# embeddings = outputs.last_hidden_state.mean(dim=-1)  # You can use different strategies for pooling

word_vectors = {}
new_bioBert = []

for i in range (len(df['bioBert_values'])):
    embeddings = df['bioBert_values'][i]

    tensor = torch.tensor

    tensor = torch.tensor(eval(embeddings))  

# 'embeddings' now contains the numerical vector representation of the input text
# print(embeddings.size())

    vector = tensor.view(-1)

    df['bioBert_values'][i] = vector.numpy()

# 'numpy_vector' now contains the NumPy representation of the embeddings
# print(len(vector))
# # print()
# print(vector[1].numpy())


max_list_length = max(df['bioBert_values'].apply(len))
column_names = [f'bioBert{i+1}' for i in range(max_list_length)]

df[column_names] = pd.DataFrame(df['bioBert_values'].to_list(), index=df.index)
# df.drop('glove_values', axis=1, inplace=True)


df.to_csv('outputCpy.csv')