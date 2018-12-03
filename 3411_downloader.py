"""
    This is a downloader to download all the pdf files in the website 
    http://www.cse.unsw.edu.au/~cs3411/18s1/lect/ to the current directory

    Usage: python3 3411_downloader.py
"""

import requests
import re
def getHTMLText(url):
    try:
        r = requests.get(url,timeout=1000)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "Error in status"


if __name__ == "__main__":
    url = "http://www.cse.unsw.edu.au/~cs3411/18s1/lect/"
    r = requests.get(url)
    index_text = getHTMLText(url)
    with open("lecture.html","wb") as code:
        code.write(r.content)
    #print(index_text)
    file = open("lecture.html")
    while 1:
        line = file.readline()
        if not line: 
            break
        #try to match 
        matchObj = re.match(r'(.*)A HREF="(.*?).pdf"',line,re.M|re.I)
        if matchObj:
            download_filename = matchObj.group(2)+".pdf"
            download_url = "http://www.cse.unsw.edu.au/~cs3411/18s1/lect/"+matchObj.group(2)+".pdf"
            
            res = requests.get(download_url)
            with open(download_filename,"wb") as code:
                code.write(res.content)



