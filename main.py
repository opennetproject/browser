from tkinter import *
import urllib.request

root = Tk()
root.geometry("800x600")
root.title("OpenNet")

window_width = 800
window_height = 575

url = StringVar()
url.set("http://opennetproject.github.io/index.wbl")

class WebImage:
    def __init__(self, url):
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))
        self.image = ImageTk.PhotoImage(image)

    def get(self):
        return self.image


def parselines(content):
    decoded = []
    for i in content:
        i = i.strip().decode("utf-8")
        decoded.append({"element": "", "text": ""})
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

def display_content(parsed_url_content):
    global content, root
    y_pos=0
    for widget in content.winfo_children():
        widget.destroy()
    for i in parsed_url_content:
        if i["element"] == "text":
            try: font_style = ("Arial", int(i["size"]))
            except: font_style = ("Arial")
            widget_b = Label(content, text=i["text"], font=font_style)
            widget_b.place(x=10,y=y_pos)
        elif i["element"] == "link":
            try: font_style = ("Arial", int(i["size"]))
            except: font_style = ("Arial")
            widget_b = Button(content, text=i["text"], font=font_style, command=lambda go_url=i["location"]: go(go_url))
            widget_b.place(x=10,y=y_pos)
        elif i["element"] == "img":
            try:
                img = WebImage(i["location"]).get()
                widget_b = Label(content, image=img)
            except:
                widget_b = Label(content, text="Image not found")
            widget_b.place(x=10,y=y_pos)
            try:
                widget_b.config(width=int(i["width"]))
            except:
                pass
        elif i["element"] == "title":
            root.title(f"{i['text']} - OpenNet")
        root.update()
        try:
            if i["align"]:
                if i["align"] == "centre":
                    widget_b.place(x=round(window_width / 2 - widget_b.winfo_width() / 2), y=y_pos)
        except:
            pass

        if i["element"] == "text":
            try: y_pos += int(i["size"]) * 2
            except: y_pos += 14 * 2
            y_pos + 10
        elif i["element"] == "link":
            try: y_pos += int(i["size"]) * 2
            except: y_pos += 13 * 2
            y_pos += 10
        elif i["element"] == "br":
            try: y_pos += int(i["size"]) * 2
            except: y_pos += 13
            y_pos += 10
        elif i["element"] == "img":
            y_pos += widget_b.winfo_width()
            y_pos += 10
    
def go(go_url=None):
    global url,content
    if not go_url:
        go_url=url.get()
    else:
        url.set(go_url)

    try:
        data = urllib.request.urlopen(url.get())
        data = data.readlines()
    except:
        data = [b"text size-18>Some error occured.", b"br>", b"text>Please try again."]
    display_content(parselines(data))
    root.update()

urlbar = Frame(root, width=800,height=25, bg="white")
urlentry = Entry(urlbar, textvariable=url, width=120)
urlgo = Button(urlbar, text="Go", width=10,command=go)
urlentry.place(x=0,y=3)
urlgo.place(x=720,y=0)
urlbar.pack()

favourites = Frame(root, width=800, height=25, bg="white")
homepage = Button(favourites, text="Homepage", width=15,command=lambda theurl="https://opennetproject.github.io/index.wbl": go(theurl))
homepage.place(x=0,y=0)
homepage = Button(favourites, text="SearchOpen", width=15,command=lambda theurl="https://opennetproject.github.io/search/index.wbl": go(theurl))
homepage.place(x=120,y=0)
favourites.pack()

content = Frame(root, width=800,height=550)
content.pack()

root.after(0,go)
root.mainloop()