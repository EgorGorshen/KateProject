returner = {
    "Уже были": {

    },
    "Хотим поехать": {

    }
}

WAS = "Уже были"
WILL = "Хотим поехать"
original_file = ""
with open('./travel_notes.csv', 'r') as file:
    for man in file.readlines():
        man = man[:-1].split(',')
        returner[WAS].update({sity: [] for sity in man[1].split(';')})
        returner[WILL].update({sity: [] for sity in man[2].split(';')})


with open('./travel_notes.csv', 'r') as file:
    for man in file.readlines():
        man = man.split(',')
        for sity in returner[WAS].keys():
            if sity in man[1]:
                returner[WAS][sity].append(man[0])

with open('./travel_notes.csv', 'r') as file:
    for man in file.readlines():
        man = man.split(',')
        for sity in returner[WILL].keys():
            if sity in man[2]:
                returner[WILL][sity].append(man[0])


print(returner)





