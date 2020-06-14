import sys
import pandas as pd
import editdistance
from parse_entities import entities

def dist_word(word1, word2):
    ents1 = entities.parseString(word1)
    ents2 = entities.parseString(word2)
    return editdistance.eval(ents1, ents2)

if __name__ == "__main__":
    word_stat_file = pd.read_csv(sys.argv[1])
    words_to_distance_oneself_from = set()
    for rulesfile in sys.argv[2:]:
        words_to_distance_oneself_from.update(pd.read_csv(rulesfile, delimiter='->', header=None).iloc[:, 0])
    
    MAX_LIM = 5
    chosen_words = set()
    for word in word_stat_file['word']:
        if len(chosen_words) < MAX_LIM:
            if word in words_to_distance_oneself_from:
                continue #slight optimization to avoid parsing known words (the answer would be an editdistance of 0)
            if min(dist_word(word, w) for w in words_to_distance_oneself_from) >= 3:
                chosen_words.add(word)
                words_to_distance_oneself_from.add(word)

    for word in chosen_words:
        print(word)

    #FIXME: I've to improve the logic. If a word can be auto-transformed (composed of unambiguous unigrams), then we can add it to `words_to_distance_oneself_from`
