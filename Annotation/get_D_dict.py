import csv
import json
import os

def get_decribe_dict(entity_file,category_file):
    p = 'E_dict_d.json'
    with open(entity_file, 'r') as file:
        E_dict = json.load(file)
    with open(category_file, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for key in E_dict.keys():
            entity_d = []
            for item in rows:
                nu = item['keggcom']
                di = item['disease']
                text = item['text']
                if key == nu and text not in entity_d:
                    entity_d.append(item['text'])
                elif key == di and text not in entity_d:
                    entity_d.append(item['text'])
            E_dict[key].update({"D":"".join(entity_d)})
    with open(p, 'w') as file:
        json.dump(E_dict, file)
    print('>>  Generate E_dict Done !')


if __name__ == '__main__':
    entity_file = 'E_dict.json'
    nu_di_text = 'compound_disease_text.csv'

    get_decribe_dict(entity_file,nu_di_text)