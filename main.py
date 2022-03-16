### PART ONE ###
from collections import defaultdict

def run_map_reduce(map_f, reduce_f, docs):
   
    pairs = flatten(list(map(map_f, docs)))
    groups = collect(pairs)
    return [reduce_f(g) for g in groups]

def word_count_map(doc):
   x = doc.split()
   y = []
   for words in x: 
     y.append((words,1))
   return y
     
def test_word_count_map():
    assert word_count_map('i am sam i am') == \
           [('i', 1), ('am', 1), ('sam', 1), ('i', 1), ('am', 1)]

def word_count_reduce(group):
  return group[0], reduce(plus, group[0], group[1])
    
def test_word_count_reduce():
    assert word_count_reduce(['i', [1,1,1]]) == ('i', 3)

def test_word_count():
    assert run_map_reduce(word_count_map, word_count_reduce, ['i am sam i am', 'sam is ham']) == \
           [('am', 2), ('ham', 1), ('i', 2), ('is', 1), ('sam', 2)]

def iterate(f, x, a):
    if len(a) == 0:
        return x
    else:
        return iterate(f, f(x, a[0]), a[1:])
    
def flatten(sequences):
    return iterate(plus, [], sequences)

def collect(pairs):
    
    result = defaultdict(list)
    for pair in sorted(pairs):
        result[pair[0]].append(pair[1])
    return list(result.items())


def plus(x, y):
    
    return x + y

def reduce(f, id_, a):
   
    if len(a) == 0:
        return id_
    elif len(a) == 1:
        return a[0]
    else:
        return f(reduce(f, id_, a[:len(a)//2]),
                 reduce(f, id_, a[len(a)//2:]))
    
    
### PART TWO ###

def sentiment_map(doc,
                  pos_terms=set(['good', 'great', 'awesome', 'sockdolager']),
                  neg_terms=set(['bad', 'terrible', 'waste', 'carbuncle', 'corrupted'])):
                    x = doc.split()
                    y = []
                    for i in x:
                      if i in pos_terms:
                        y.append(('positive',1))
                      elif i in neg_terms:
                        y.append(('negative',1))
                    return y
              
def test_sentiment_map():
    assert sentiment_map('it was a terrible waste of time') == [('negative', 1), ('negative', 1)]

    
def test_sentiment():
    docs = [
        'it was not great but not terrible',
        'thou art a boil a plague-sore or embossed carbuncle in my corrupted blood',
        'it was a sockdolager of a good time'
    ]
    result = run_map_reduce(sentiment_map, word_count_reduce, docs)
    assert result == [('negative', 3), ('positive', 3)]

