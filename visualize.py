import sys
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.manifold import Isomap
import matplotlib.pyplot as plt

if __name__ == "__main__":
    word_stat_file = pd.read_csv(sys.argv[1])

    words_stats = word_stat_file[:10000]

    viz_pipe = make_pipeline(
            CountVectorizer(analyzer='char', ngram_range=(2,2), preprocessor= lambda s: f' {s} '),
            Isomap(n_components=2)
            )

    X = words_stats['word']
    y = words_stats['auto_translit_poss']
    projection = viz_pipe.fit_transform(X)

    plt.scatter(projection[:,0], projection[:,1], c=y, cmap='viridis',  alpha=0.2)
