import json
from api.model.models import Disease
with open("data.json","r",encoding='utf-8') as f:
    data:dict
    data = json.load(f)
    for key,value in data.items():
        disease = Disease(
            name=key,
            label=value["label"],
            concept= value["concept"],
            reason = value["reason"],
            symptom = value["symptom"],
            consequence = value["consequence"],
            type = value["type"]
        )
        print(disease)
        break

f.close()