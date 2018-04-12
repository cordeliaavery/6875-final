from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://localhost:9000')

text = []

with open("sentences.txt") as f:
    for line in f:
        text.append(line)

for s in text:
    output = nlp.annotate(s, properties={
        'annotators': 'parse',
        'outputFormat': 'json'
    })
    
    print(output['sentences'][0]['parse'])
