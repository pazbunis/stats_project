import csv

NAME_IDX = 1
MODEL_IDX = 10
MAKE_IDX = 14

with open('autos.csv', 'r', encoding='iso-8859-1') as csvfile:
    listing_reader = csv.reader(csvfile)
    for row in listing_reader:
        # name = row[NAME_IDX]
        model = row[MODEL_IDX]
        make = row[MAKE_IDX]
        print(model, make)
#with open('make_and_model.csv', 'w') as csvfile:
#    modelwriter = csv.writer(csvfile, delimiter=',')
#    for make in make_model_names:
#        models = make_model_names[make]
#        for model in models:
#            modelwriter.writerow([make.lower(), model.lower()])