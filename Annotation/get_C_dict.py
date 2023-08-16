import os
import json
import random
import pickle
import pandas as pd

p = 'C_dict.data'

# if os.path.exists(p):
#     with open(p, 'rb') as file:
#         C_dict = pickle.load(file)
#     print('>>  C_dict already exists !')
# else:
    # E: whole entity name list(such as disease-011) len(E):2367
E = list(pd.read_csv('../dataset/entity.csv')['E'])
with open('E_dict.json') as file:
    E_dict = json.load(file)
c_count, C = {}, []
for e in E:
    # E_dict[e]['C']: find Categories about an entity e based on its name
    # C only has three index, but the third index may have more categories
    c1, c2, c3 = E_dict[e]["C"]
    # c_count: count each category type and its numbers len(c_count):82235
    for c in c2 + c3:
        if c not in c_count:
            c_count[c] = 1
        else:
            c_count[c] += 1
    # C: each entity has a category description, len(C):2367
    C.append([c1, c2, c3])
# this process is to filter the categories which are more than 10
# transfer the category type to sequence len(c_list) 4398 (because the filter)
c_list = \
    ['DI','Nu','Mi'] + \
    [key for key, value in c_count.items() if value >= 10]
c_dict = dict(zip(sorted(c_list), range(len(c_list))))

# the dimension of layer_c is 32
num_c = 32
C_dict = []
for c1, c2, c3 in C:
    c1 = [c_dict[c1[0]]]
    c2 = [c_dict[c] for c in c2 if c in c_dict]
    c3 = [c_dict[c] for c in c3 if c in c_dict]
    # len(c) 32
    if 1 + len(c2) >= num_c:
        c = c1 + random.sample(c2, num_c - 1)
    # random sample from c3
    elif 1 + len(c2 + c3) >= num_c:
        c = c1 + c2 + random.sample(c3, num_c - len(c2) - 1)
    else:
        c = (c1 + c2 + c3) * (num_c // (1 + len(c2 + c3)))
        c += c1 * (num_c - len(c))
    # len(C_dict):2367
    C_dict.append(sorted(c))

with open(p, 'wb') as file:
    pickle.dump(C_dict, file)
print('>>  Generate C_dict Done !')

E_index = dict(zip(E, range(len(E))))
with open('E_index.json', 'w') as file:
    json.dump(E_index, file)
print('>>  Generate E_index Done !')