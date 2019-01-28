with open('domain_raw.txt') as f:
    wp_list = [line.rstrip('\n') for line in f]

print(wp_list)
ans = []


def add(temp):
    if temp not in ans:
        ans.append(temp)


for item in wp_list:
    item = item.split('.')
    if len(item) > 2:
        continue
    if len(item) == 1:
        add(item[0] + '.wikipedia.org')
        continue
    if item[1] == 'b':
        add(item[0] + '.wikibooks.org')
        continue
    if item[1] == 'd':
        add(item[0] + '.wiktionary.org')
        continue
    if item[1] == 'f':
        add(item[0] + '.wikimediafoundation.org')
        continue
    if item[1] == 'n':
        add(item[0] + '.wikinews.org')
        continue
    if item[1] == 'q':
        add(item[0] + '.wikiquote.org')
        continue
    if item[1] == 's':
        add(item[0] + '.wikisource.org')
        continue
    if item[1] == 'v':
        add(item[0] + '.wikiversity.org')
        continue
    if item[1] == 'voy':
        add(item[0] + '.wikivoyage.org')
        continue
    if item[1] == 'w':
        add(item[0] + '.mediawiki.org')
        continue
    if item[1] == 'wd':
        add(item[0] + '.wikidata.org')
        continue

with open('wp_full.txt', 'w') as f:
    for item in ans:
        f.write("%s\n" % item)

