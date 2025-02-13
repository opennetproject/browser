from tkinter import *
import urllib.request
from functools import partial

root = Tk()
root.geometry("800x600")
root.title("OpenNet")

window_width = 800
window_height = 575

POST_CONTENT = ""

url = StringVar()
url.set("http://opennetproject.github.io/index.wbl")

class WebImage:
    def __init__(self, url):
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))
        self.image = PhotoImage(image)

    def get(self):
        return self.image


def parselines(content, POST):
    decoded = []
    for i in content:
        i = i.strip().decode("utf-8")
        decoded.append({"element": "", "text": ""})
        i = i.replace("(POST)", POST)
        j = i.split(" ")
        decoded[len(decoded) - 1]["element"] = j.pop(0).split(">")[0].replace(">", "")
        parseindex = 0
        while parseindex < len(j):
            if "-" in j[parseindex]:
                temp = ""
                if "-\"" in j[parseindex]:
                    while j[parseindex][-1] != "\"":
                        temp += j[parseindex]
                        parseindex += 1
                    decoded[len(decoded) - 1][temp.split("-")[0]] = temp.split("-")[1].split(">")[0]
                else:
                    decoded[len(decoded) - 1][j[parseindex].split("-")[0]] = j[parseindex].split("-")[1].split(">")[0]
            elif ">" in j[parseindex]:
                break
            parseindex += 1
        try:
            decoded[len(decoded) - 1]["text"] = i.split(">", 1)[1]
        except:
            decoded[len(decoded) - 1]["text"] = ""
    print(decoded)
    return decoded

def post(url, content):
    global POST_CONTENT
    print(content)
    POST_CONTENT = content
    go(url)
    
    
def display_content(parsed_url_content, POST):
    global content, root
    y_pos = 0
    
    for widget in content.winfo_children():
        widget.destroy()

    for i in parsed_url_content:
        font_style = ("Arial", int(i.get("size", 12)))
        
        if i["element"] == "text":
            widget_b = Label(content, text=i["text"], font=font_style)
            widget_b.place(x=10, y=y_pos)

        elif i["element"] == "link":
            widget_b = Button(content, text=i["text"], font=font_style, 
                              command=partial(go, i["location"]))
            widget_b.place(x=10, y=y_pos)

        elif i["element"] == "img":
            try:
                img = WebImage(i["location"]).get()
                widget_b = Label(content, image=img)
                widget_b.image = img  
            except:
                widget_b = Label(content, text="Image not found")
            
            widget_b.place(x=10, y=y_pos)
            widget_b.config(width=int(i.get("width", widget_b.winfo_width())))

        elif i["element"] == "box":
            if i.get("type") == "search":
                widget_b = Frame(content, width=200, height=20)
                widget_b.place(x=round(window_width / 2 - 200 / 2), y=y_pos)
                box_content = StringVar()
                box_src = Entry(widget_b, textvariable=box_content)
                box_src.place(x=0, y=0)
                box_go = Button(widget_b, text="Go", command=lambda i=i: post(i["location"], box_content.get()))
                box_go.place(x=163, y=-5)

        elif i["element"] == "title":
            root.title(f"{i['text']} - OpenNet")

        root.update()

        if i.get("align") == "centre":
            widget_b.place(x=round(window_width / 2 - widget_b.winfo_width() / 2), y=y_pos)

        if i["element"] in ["text", "link"]:
            y_pos += int(i.get("size", 12)) * 2 + 10
        elif i["element"] == "br":
            y_pos += int(i.get("size", 13)) + 10
        elif i["element"] == "img":
            y_pos += widget_b.winfo_height() + 10
    
def go(go_url=None):
    global url,content, POST_CONTENT
    if not go_url:
        go_url=url.get()
    else:
        url.set(go_url)

    try:
        data = urllib.request.urlopen(url.get())
        data = data.readlines()
    except:
        data = [b"text size-18>Some error occured.", b"br>", b"text>Please try again."]
    display_content(parselines(data, POST_CONTENT), POST_CONTENT)
    root.update()

urlbar = Frame(root, width=800,height=25, bg="white")
urlentry = Entry(urlbar, textvariable=url, width=90)
urlgo = Button(urlbar, text="Go", width=5, command=go)
urlentry.place(x=0,y=3)
urlgo.place(x=730,y=0)
urlbar.pack()

favourites = Frame(root, width=800, height=25, bg="white")
homepage = Button(favourites, text="Homepage", width=11,command=lambda theurl="https://opennetproject.github.io/index.wbl": go(theurl))
homepage.place(x=0,y=0)
homepage = Button(favourites, text="SearchOpen", width=11,command=lambda theurl="https://opennetproject.github.io/search/index.wbl": go(theurl))
homepage.place(x=120,y=0)
favourites.pack()

content = Frame(root, width=800,height=550)
content.pack()

root.after(0,go)
root.mainloop()