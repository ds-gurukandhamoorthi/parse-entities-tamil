import sys
import re
import pandas as pd
from collections import Counter
from nltk.tokenize import word_tokenize
from parse_entities import nb_tamil_entities



def is_eng_or_punct(word):
    return re.search(r'^[a-zA-Z0-9_<>–%*,.!:#=?’‘”“;\'&{}\[\]()/-]+$', word)

def count_words(filename):
    wordcount = Counter(word_tokenize(open(filename, 'r').read()))
    for w in wordcount:
        if is_eng_or_punct(w):
            wordcount[w] = 0
    return wordcount



if __name__ == "__main__":
    total_word_count = Counter()
    for filename in sys.argv:
        # print(filename)
        this_file_counter = count_words(filename)
        total_word_count.update(this_file_counter)
    # print(total_word_count)
    df = pd.DataFrame.from_dict(total_word_count, orient='index').reset_index().rename(columns={'index':'word', 0:'count'})
    df['entities_len'] = df['word'].map(str).apply(nb_tamil_entities)
    df['importance'] = df['count'] * df['entities_len']
    df = df.sort_values(by='importance', ascending=False)
    df.to_csv('/tmp/abcweirwuij.csv', index=False)


