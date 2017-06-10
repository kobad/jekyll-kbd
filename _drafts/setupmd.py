import sys
from datetime import datetime

def setupmd(fname):
    date = datetime.now().strftime("%Y-%m-%d")
    line = "---"
    layout = "layout: post"
    title = "title: "
    datet = "date: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    categories = "categories: "

    t = input("title: ")
    c = input("catogory: ")

    title += t
    categories += c
    tmp = line + "\n" + layout + "\n" + title + "\n" + datet + "\n" + categories + "\n" + line + "\n"

    with open(date + "-" + fname, "wb") as f:
        f.write(tmp.encode('utf-8'))
        md = open(fname, "rb")
        f.write(md.read())
        md.close()

if __name__=="__main__":
    if len(sys.argv) >= 2:
        setupmd(sys.argv[1])



