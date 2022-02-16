import requests
import sys
import matplotlib.pyplot as mat
import nltk
from nltk.corpus import stopwords
import string
from bs4 import BeautifulSoup


def get_text():
    url = "https://www.cbinsights.com/research/startup-failure-post-mortem"
    result = requests.get(url).text
    doc = BeautifulSoup(result , "html.parser")
    h3 = doc.find_all(["h3"] )
    bq = doc.find_all(["blockquote"] )
    for i in range(100):
        if i > 46 and i <58:
            continue
        name = h3[i].string
        article = str()
        p = h3[i].next_sibling
        z = bq[i] if i<80 else bq[i+1]
        while p is not z:
            if not(p.string == None or p.string == '\n'):
                if p.string not in ["Product:" , "Title:" ,"Company:"] :
                    article = article + '\n' + p.string
            else:
                try:
                    # remove if have missing info
                    text = " ".join([child.string for child in p.children])
                    article = article + '\n' + text
                except:
                    pass
            p = p.next_sibling
        article = article + '\n' + bq[i].p.string
        writefile(sys.argv[1] , name , article , i)
    
def writefile(file, name , article , number):
    with open(file, "a" , encoding="utf8") as f:
        f.write(str(number))
        f.write("\n")
        f.write(name)
        f.write(article)
        f.write("\n")
        f.write("\n")

def sentiment(name , paragraphs)-> dict:
    """
    Sentiment analysis!!! by words / phrases
    """
    reason = {}
    
    for para in paragraphs:
        _reason = []
        if any(word in para for word in["pandemic" , "COVID"]):
            _reason.append("Pandemic")
            print("Pandemic")
        if any(word in para for word in ["margins" , "low profit", "no captial", "low captial" ,"revenue growth"]):
            _reason.append("margins")
            print("margins")
        if any(word in para for word in ["unable to find product-market fit","product market fit"]):
            _reason.append("buiness model")
            print("buiness model")
        if any(word in para for word in ["complex regulatory environment","violated" , "illegally", "illegal"]):
            _reason.append("regulation")
            print("regulation")
        if any(word in para for word in ["misleading marketing practices","violated"]):
            _reason.append("PR")
            print("PR")
        if any(word in para for word in ["bankrupt"]):
            _reason.append("bankrupt")
            print("bankrupt")

def readfile(file)->str():
    with open(file, "r", encoding="utf8") as f:
        return f.read()
        
class textanalysis():
    def __init__(self, article:str , stopwords , punctuation , lem) -> None:
        self.article = article 
        self.words = []
        #self.filtered = []    
        self.lemma = []
        self.stopword = stopwords
        self.punctuation = punctuation
        self.lem = lem  
        self.tokenisation() 
        self.remove_noise()
        self.plot()  

    def tokenisation(self)->None:
        #self.article = sent_tokenize(self.article , language="english")
        #for word in self.article:
        self.words = nltk.tokenize.word_tokenize(self.article)
        
    def remove_noise(self) ->None:
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



if __name__ == "__main__":
    article = readfile(sys.argv[1])
    #ps = nltk.PorterStemmer()
    lem = nltk.stem.WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))
    text = textanalysis(str(article),stop_words,set(string.punctuation) , lem)
