import csv
import re



makes_and_models = dict()
all_models = set()
model_map = dict()
with open('make_and_model.csv', 'r') as csvfile:
    make_model_reader = csv.reader(csvfile)
    for row in make_model_reader:
        make = row[0].replace('-', '_')
        model_set = makes_and_models.get(make, set())
        
        model_set.add(row[1])
        no_dash = row[1].replace('-', '')
        no_underline = row[1].replace('_', '')
        no_space = row[1].replace(' ', '')
        model_set.update([row[1], no_dash, no_space, no_underline])
        
        model_map[no_dash] = row[1]
        model_map[no_underline] = row[1]
        model_map[no_space] = row[1]
        
        makes_and_models[make]  = model_set
        all_models = all_models.union(model_set)
#models = models.difference(makes)

#%%
NAME_IDX = 1
SELLER_IDX = 2
OFFER_IDX = 3
GEARBOX_IDX = 8
MODEL_IDX = 10
FUEL_IDX = 13
MAKE_IDX = 14
REPAIR_IDX = 15

c = 0

def get_model(make, name):
    global c
    # get maker's model set, or all models as fallback
    model_set = makes_and_models.get(make.lower(), all_models) 
    word_list = name.lower().split('_')
    orig_word_list = list(word_list)
    
    # add concats, such as ['9', '5'] -> ['9-5']
    for i in range(len(orig_word_list) - 1):
        word_list.append(orig_word_list[i] + '-' + orig_word_list[i+1])
        word_list.append(orig_word_list[i] + '_' + orig_word_list[i+1])
        word_list.append(orig_word_list[i] + orig_word_list[i+1])
        
    # add number models without letters, such as '316i' -> '316'
    regex = r"([0-9]{2,3})"
    orig_word_list = list(word_list)
    for word in orig_word_list:
        matches = re.finditer(regex, word)
        for matchNum, match in enumerate(matches):
            matchNum = matchNum + 1
            for groupNum in range(0, len(match.groups())):
                word_list.append(match.group(groupNum))
    
    for word in word_list:
        if word in model_set:        
            return model_map.get(word)
#    c += 1
#    print(c)
#    print(name)
    return 'unknown'

def translate(row):
    seller_dict = {'gewerblich': 'business', 'privat': 'private'}
    offer_dict = {'Angebot': 'selling', 'Gesuch': 'buying'}
    gearbox_dict= {'automatik': 'automatic', 'manuell': 'manual'}
    fuel_dict = {'andere': 'other', 'benzin': 'gasoline', 'elektro': 'electric'}
    repair_dict = {'ja': 'yes', 'nein': 'no'}
    row[SELLER_IDX] = seller_dict.get(row[SELLER_IDX], row[SELLER_IDX])
    row[OFFER_IDX] = offer_dict.get(row[OFFER_IDX], row[OFFER_IDX])
    row[GEARBOX_IDX] = gearbox_dict.get(row[GEARBOX_IDX], row[GEARBOX_IDX])
    row[FUEL_IDX] = fuel_dict.get(row[FUEL_IDX], row[FUEL_IDX])
    row[REPAIR_IDX] = repair_dict.get(row[REPAIR_IDX], row[REPAIR_IDX])
    return row

with open('../autos.csv', 'r', encoding='iso-8859-1') as csvfile_in:
    with open('../autos_enriched.csv', 'w', encoding='iso-8859-1') as csvfile_out:
        autos_reader = csv.reader(csvfile_in)
        autos_writer = csv.writer(csvfile_out)
        header = next(autos_reader)
        header.insert(MODEL_IDX, 'model_enriched')
        autos_writer.writerow(header)
        for row in autos_reader:
            row = translate(row)
            model = row[MODEL_IDX]
            if model not in all_models:
                make = row[MAKE_IDX]
                name = row[NAME_IDX]    
                model = get_model(make, name)
            row.insert(MODEL_IDX, model)
            autos_writer.writerow(row)
            