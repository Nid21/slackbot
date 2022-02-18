
import sys
from collections import Counter
import nltk
from nltk.corpus import stopwords
import string
nltk.download('omw-1.4')
def readfile(file):
    with open(file, "r", encoding="utf8") as f:
        return f.read()

class textanalysis():
    def __init__(self, article , stopwords , punctuation , lem):
        self.article = article 
        self.words = []
        #self.filtered = []    
        self.lemma = []
        self.stopword = stopwords
        self.punctuation = punctuation
        self.lem = lem  
        self.tokenisation() 
        self.remove_noise()
        #self.plot()  

    def tokenisation(self):
        #self.article = sent_tokenize(self.article , language="english")
        #for word in self.article:
        self.words = nltk.tokenize.word_tokenize(self.article)
        
    def remove_noise(self):
        self.words.pop(0)
        for w in self.words:
            if w.lower().strip() not in self.stopword and w not in self.punctuation and w.lower().strip() not in [".",",","’",":","—","”","“", "company","title", "product" ,"startup","shut"]:
                #self.filtered.append(ps.stem(w))
                self.lemma.append(self.lem.lemmatize(w.lower().strip(),"v"))
    def plot(self):
        #self.dfilter = nltk.probability.FreqDist(self.filtered)
        self.dlem = nltk.probability.FreqDist(self.lemma)
        self.dlem.plot(100 , cumulative=False)
        print(self.dlem.most_common(150))
        #mat.show()

    def ngram(self, n = 5):
        self.ngrams = Counter(nltk.ngrams(self.lemma,n))
        for ngram, freq in  self.ngrams.most_common(100):
            print(f"{freq}, {ngram}")

if __name__ == "__main__":
    article = readfile(sys.argv[1])
    with open("function_words.txt") as f:
        function_words = set(f.read().splitlines())
    #ps = nltk.PorterStemmer()
    lem = nltk.stem.WordNetLemmatizer()
    stop_words = set(stopwords.words("english")).union(function_words)
    
    text = textanalysis(str(article),stop_words,set(string.punctuation) , lem)
    # generate n gram
    text.ngram( 1)
