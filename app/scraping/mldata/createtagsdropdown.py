f = open('app/scraping/mldata/tags.txt')
for line in f:
    line = line.replace('\n','')
    print("<option value="+line+">"+line+"</option>")