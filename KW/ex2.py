words = input().split()
up_words = []
for word in words:
    for char in word:

        if char in 'ЙЦУКЕНГШЩЗХЪЁФЫВАПРОЛДЖЭЯЧСМИТЬБЮ':
            up_words.append(word.lower())
            break

print(sorted(up_words))
