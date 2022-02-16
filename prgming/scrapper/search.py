from bs4 import BeautifulSoup
import requests

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
        print(article.partition("fail")[2])


if __name__ == "__main__":
    get_text()