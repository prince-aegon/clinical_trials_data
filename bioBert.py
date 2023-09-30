import torch
from transformers import AutoTokenizer, AutoModel

model_name = "dmis-lab/biobert-v1.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

text = "Determine the safety and toxicity of preoperative trastuzumab (Herceptin) and&#xD; paclitaxel followed by postoperative doxorubicin and cyclophosphamide in women with locally&#xD; advanced breast cancer with HER2 overexpression. II. Determine tumor response in these&#xD; patients treated with this regimen. III. Assess the effect of this regimen on tumor histology&#xD; and the potential molecular determinants of response in these patients dxjgbjabg kj's;atnfjk; sd jewgain;ion kowetjgokaeag e orjmgrjpokpermg ]samgplaer pertykep dporykpreyk drykkyp[5kyup[ oijtop]]grew    estyojy erokperryk ryes[k[pseym ]] sy5iput qewu8yhpiuef qthuiupewtn    Determine the safety and toxicity of preoperative trastuzumab (Herceptin) and&#xD; paclitaxel followed by postoperative doxorubicin and cyclophosphamide in women with locally&#xD; advanced breast cancer with HER2 overexpression. II. Determine tumor response in these&#xD; patients treated with this regimen. III. Assess the effect of this regimen on tumor histology&#xD; and the potential molecular determinants of response in these patients dxjgbjabg kj's;atnfjk; sd jewgain;ion kowetjgokaeag e orjmgrjpokpermg ]samgplaer pertykep dporykpreyk drykkyp[5kyup[ oijtop]]grew    estyojy erokperryk ryes[k[pseym ]] sy5iput qewu8yhpiuef qthuiupewtn"
# inputs = tokenizer(text, return_tensors="pt")
inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)

with torch.no_grad():
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state  # This contains the embeddings for all tokens in the input text

features = embeddings.mean(dim=1)  
print(features.size())