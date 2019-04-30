import requests
import re



for tut in range(2,10):
    tut = str(tut)
    url = "https://www.cse.unsw.edu.au/~cs3411/19t1/tut/sol/wk"+tut+"sol.html"
    print(url)
    r = requests.get(url)
    
    filename = "tut"+tut+".html"
    print(filename)
    with open(filename,"wb") as code:
        code.write(r.content)
