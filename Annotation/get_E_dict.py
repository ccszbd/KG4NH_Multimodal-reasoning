import csv
import json
import os


def convert_csv_to_json(csv_file, json_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    with open(json_file, 'w') as file:
        json.dump(rows, file, indent=4)

def get_disease_e_dict(entity_file,category_file):
    E, E_dict = [], {}
    with open(entity_file, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for item in rows:
            E.append(item['e'])
    with open(category_file, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for e in E:
            e_parent, e_child = [], []
            for item in rows:
                if e.split('//')[1].split('/')[0] == 'www.ihtsdo.org':
                    if e == item['disease']:
                        e_parent.append(item['diseasetree'])
                    elif e == item['diseasetree']:
                        e_child.append(item['disease'])
                    E_dict[e] = ({"C":[['DI'],e_parent,e_child]})
            for p in e_parent:
                for item in rows:
                    if p == item['disease'] and item['diseasetree'] not in e_parent:
                        e_parent.append(item['diseasetree'])
            for c in e_child:
                for item in rows:
                    if c == item['diseasetree'] and item['disease'] not in e_child:
                        e_child.append(item['disease'])
            print(e)
    with open('disease_E_dict.json','w') as file:
        json.dump(E_dict, file, indent=4)


def get_compound_e_dict(entity_file, category_file):
    E, E_dict = [], {}
    with open(entity_file, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for item in rows:
            E.append(item['e'])
    with open(category_file, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for e in E:
            e_parent, e_child = [], []
            for item in rows:
                if e.split('//')[1].split('/')[0] == 'www.kegg.jp':
                    if e == item['Compound']:
                        e_parent.append(item['Compoundclass'])
                    E_dict[e] = ({"C": [['Nu'], e_parent, e_child]})
            print(e)
    with open('compound_E_dict.json','w') as file:
        json.dump(E_dict, file, indent=4)

def get_microbe_e_dict(entity_file, category_file):
    E, E_dict = [], {}
    with open(entity_file, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for item in rows:
            E.append(item['e'])
    with open(category_file, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for e in E:
            e_parent, e_child = [], []
            for item in rows:
                if e.split('//')[1].split('/')[0] == 'nlp_microbe.ccnu.edu.cn':
                    if e == item['bacteria']:
                        e_parent.append(item['bacteriaclass'])
                        e_parent.append(item['bacteriatree1'])
                        e_parent.append(item['bacteriatree2'])
                        e_parent.append(item['bacteriatree3'])
                        e_parent.append(item['bacteriatree4'])
                        e_parent.append(item['bacteriatree5'])
                    E_dict[e] = ({"C": [['Mi'], e_parent, e_child]})
            print(e)
    with open('microbe_E_dict.json','w') as file:
        json.dump(E_dict, file, indent=4)


def get_e_json():
    p = 'E_dict.json'
    if os.path.exists(p):
        with open(p) as file:
            E_dict = json.load(file)
        print(len(E_dict.keys()))
        print('>>  E_dict already exists !')
    else:
        name_list = ['compound','disease','microbe']
        E_dict = {}
        for k in range(3):
            with open(name_list[k] + '_E_dict' + '.json') as file:
                tmp = json.load(file)
            E_dict.update(tmp)
        with open(p, 'w') as file:
            json.dump(E_dict, file)
        print('>>  Generate E_dict Done !')

if __name__ == '__main__':
    entity_file = '../dataset/entity.csv'
    disease_category_file = 'disease_snomed.csv'
    compound_category_file = 'compound_kegg.csv'
    microbe_category_file = 'microbe_ncbi.csv'
    get_e_json()
    # get_disease_e_dict(entity_file, disease_category_file)
    # get_compound_e_dict(entity_file, compound_category_file)
    # get_microbe_e_dict(entity_file, microbe_category_file)
