import csv
import urllib3
import json

http = urllib3.PoolManager()
make_model = dict()

with open('make_ids.csv', 'r') as csvfile:
    makereader = csv.reader(csvfile)
    for i, row in enumerate(makereader):
        make_id = row[0]
        make_name = row[1]
        url = 'https://www.autoscout24.com/home/makes/{0}/models?modelType=C&lang=en-GB'.format(make_id)        
        r = http.request('GET', url)
        make_model[make_name] = json.loads(r.data.decode('utf-8'))

#%%
def get_names(models_list):
    names_sets = []
    for m in models_list:
        if 'models' in m:
            names_sets.extend(m['models'])
        else:
            names_sets.append(m)
    names = []
    for s in names_sets:
        names.append(s['name'])
    return names


make_model_names = dict()
for key in make_model:
    make_model_names[key] = get_names(make_model[key])

#%%
with open('make_and_model.csv', 'w') as csvfile:
    modelwriter = csv.writer(csvfile, delimiter=',')
    for make in make_model_names:
        models = make_model_names[make]
        for model in models:
            modelwriter.writerow([make.lower(), model.lower()])