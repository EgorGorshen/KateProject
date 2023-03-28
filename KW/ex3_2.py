with open('travel_notes.csv', 'r') as f:
    lines = f.readlines()

data = {}

for line in lines:
    s = line.strip().split(',')
    name, cities = s[0], ','.join((s[1], s[2]))

    want_to_visit, visited = cities.split(',')
    data[name] = {
        'want_to_visit': set(want_to_visit.split(';')),
        'visited': set(visited.split(';'))
    }

first_letter = input()

selected_data = {k: v for k, v in data.items() if k.startswith(first_letter)}

want_to_visit_cities = set()
for v in selected_data.values():
    want_to_visit_cities |= v['want_to_visit']

visited_cities = set()
for v in selected_data.values():
    visited_cities |= v['visited']

not_visited_cities = want_to_visit_cities - visited_cities

want_to_visit_cities = sorted(want_to_visit_cities)
visited_cities = sorted(visited_cities)
not_visited_cities = sorted(not_visited_cities)

destination_city = max(not_visited_cities)

with open('vacation.csv', 'w') as f:
    f.write(f'Хотим побывать: {", ".join(want_to_visit_cities)}\n')
    f.write(f'Успели побывать: {", ".join(visited_cities)}\n')
    f.write(f'Никто не был в: {", ".join(not_visited_cities)}\n')
    f.write(f'В итоге едем в: {destination_city}\n')

