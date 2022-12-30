from flask import Flask, request
import requests
import json

app = Flask(__name__)

@app.route('/')
def hello():
    return "ok"

@app.route('/reviews')
def reviews():
    title = request.form["title"]
    times = int(request.form["times"])
    text = ""
    stars = 0
    num = 0

    for i in range(times):
        if(i==0):
            res = requests.get(f"https://imdb-api.tprojects.workers.dev/reviews/{title}?option=date&sortOrder=desc")
            if(res.status_code==200):
                res = res.json()
                for review in res["reviews"]:
                    text += "\n"
                    text += review["content"]
                    stars += review["stars"]
                    num += 1
            else:
                continue
        else:
            res2 = requests.get("https://imdb-api.tprojects.workers.dev"+res["next_api_path"])
            if(res2.status_code==200):
                res2 = res2.json()
                for review in res2["reviews"]:
                    text += "\n"
                    text += review["content"]
                    stars += review["stars"]
                    num += 1
            else:
                continue
    return {
        "text":text,
        "stars":stars//num
    }
    

if __name__ == '__main__':
    app.run()
