def convert(a):
    a = a.replace(' ', '').split('|')
    name = a[0]
    cal = list(map(int, a[1].split(';')))
    return name, [cal, cal[0] * 5 + cal[1] * 7 + cal[2] * 5]

returner = {}
a = input()
while a != 'СТОП':
    if a:
        conv = convert(a)
        returner[conv[0]] = conv[1]
    a = input()

order = list(i.split('-') for i in input().split(', '))

for i in sorted(order, key=lambda x: returner[x[0]][0][-1]):
    print('Продукт:', i[0] + ', калорийность:', int(i[1]) * returner[i[0]][1])
    



