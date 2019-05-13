import requests
import json
from vote_code import vote

articleID = None
def getComments(URL):
    global articleID
    try:
        splitted =URL.split("-")
        id = splitted[1].split(".")
        articleID = id[0]
        commentURL = f"https://www.is.fi/rest/articles/{articleID}/comments?offset=0&perPage=1000"
        comments = requests.get(commentURL)
        return json.loads(comments.content)

    except Exception as e:
        print(f"Error building the link!{str(e)}")

def findCommentId(commentList,name):
    try:
        for user in commentList['list']:
            if name == user['userNickname']:
                print("Users comment found!")
                return user['id']
        print("kommenttia ei löytynyt tuolla nimimerkillä")
    except Exception as e:
        print(f"error: kommenttia ei löydy! {str(e)}")

def sendVotes(amount, commentID):
    global articleID
    try:
        body = {"voteType":"upvote"}
        headers = {'Content-type': 'application/json; charset=UTF-8'}
        for i in range(int(amount)):
            r = requests.post(f"https://www.is.fi/rest/articles/{articleID}/comments/{commentID}/votes", json=body, headers=headers)
            if r.status_code != 200:
                print("Ei toimi")
        print("all done!")
        exit()

    except Exception as e:
        print(f"Ei voi äänestää :( {str(e)}")

tapa = input("Haluatko antaa ääniä kyselylle? y/n: ")

URL = input("Anna uutisen linkki jossa on kommentti/kysely: ")
if URL == "q":
    exit()

elif tapa == "y":
    votes = vote(URL)
    votes.getVoteSite()

comments = getComments(URL)
commentName = input("Anna kommentin käyttäjänimi: ")
if commentName == "q":
    exit()
commentID = findCommentId(comments, commentName)
voteAmount = input("Anna tykkäysten määrä: ")
if voteAmount == "q":
    exit()
sendVotes(voteAmount, commentID)