import requests, json

def checkrs(rs):
    el = requests.get("https://users.roblox.com/v1/users/authenticated", cookies={".ROBLOSECURITY": rs})
    el = json.loads(el.text)
    if "errors" in el:
        return None
    else:
        return True
    
def getuser(user):
    if type(user) in [str, int, list]:
        if type(user) == list:
            user = enumerate(user)
            ids, usernames = [], []
            for el in user:
                if type(el[1]) == int:
                    ids.append(el)
                elif type(el[1]) == str:
                    usernames.append(el)
            newids, newusernames = [], []
            if ids:
                el = requests.post("https://users.roblox.com/v1/users", json={"userIds": [el[1] for el in ids], "excludeBannedUsers": False})
                el = json.loads(el.text)
                if el["data"]:
                    for foo in el["data"]:
                        newids.append(foo["id"])
            if usernames:
                el = requests.post("https://users.roblox.com/v1/usernames/users", json={"usernames": [el[1] for el in usernames], "excludeBannedUsers": False})
                el = json.loads(el.text)
                if el["data"]:
                    for foo in el["data"]:
                        newusernames.append(foo["id"])
            user = sorted(newids + newusernames)
            if user == []:
                return None
            else:
                return user
        else:
            try:
                user = int(user)
            except:
                pass
            if type(user) == int:
                el = requests.post("https://users.roblox.com/v1/users", json={"userIds": [user], "excludeBannedUsers": False})
            else:
                el = requests.post("https://users.roblox.com/v1/usernames/users", json={"usernames": [user], "excludeBannedUsers": False})
            el = json.loads(el.text)
            if el["data"] == []:
                return None
            else:
                return el["data"][0]["id"]
    else:
        return None

class client():
    def __init__(self, rosec=None):
        self.user = _user(rosec)
        self.group = _group(rosec)

class _user():
    def __init__(self, rosec):
        self._rosec = rosec
    
    def check(self, user):
        user = getuser(user)
        if user:
            return True
        else:
            return False
    
    def info(self, user):
        user = getuser(user)
        if user:
            el = requests.get(f"https://users.roblox.com/v1/users/{user}")
            el = json.loads(el.text)
            foo = requests.get("https://thumbnails.roblox.com/v1/users/avatar", params={"userIds": user, "size": "720x720", "format": "png"})
            foo = json.loads(foo.text)
            bar = requests.get(f"https://friends.roblox.com/v1/users/{user}/friends/count")
            bar = json.loads(bar.text)
            ag = requests.get(f"https://friends.roblox.com/v1/users/{user}/followers/count")
            ag = json.loads(ag.text)
            qux = requests.get(f"https://friends.roblox.com/v1/users/{user}/followings/count")
            qux = json.loads(qux.text)
            info = {
                "name": el["name"],
                "nick": el["displayName"],
                "id": el["id"],
                "creation": el["created"],
                "avatar": foo["data"][0]["imageUrl"],
                "friends": bar["count"],
                "followers": ag["count"],
                "following": qux["count"]
            }
            return info
        else:
            return None
    
    def activity(self, user):
        user = getuser(user)
        if user:
            yesrs = None
            rosec = self._rosec
            if rosec:
                rscheck = checkrs(rosec)
                if rscheck:
                    yesrs = True
                    el = requests.post("https://presence.roblox.com/v1/presence/users", json={"userIds": [user]}, cookies={".ROBLOSECURITY": rosec})
                else:
                    el = requests.post("https://presence.roblox.com/v1/presence/users", json={"userIds": [user]})
            else:
                el = requests.post("https://presence.roblox.com/v1/presence/users", json={"userIds": [user]})
            el = json.loads(el.text)
            if "errors" not in el:
                el = el["userPresences"][0]
                info = {}
                if yesrs:
                    if el["lastLocation"] not in ["", "Website"]:
                        info["game"] = {
                            "name": el["lastLocation"],
                            "link": f"https://www.roblox.com/games/{el['placeId']}"
                        }
                if el["userPresenceType"] == 0:
                    activitytype = "Offline"
                elif el["userPresenceType"] == 1:
                    activitytype = "Online"
                elif el["userPresenceType"] == 2:
                    activitytype = "In-Game"
                else:
                    activitytype = "Creating"
                info["type"] = activitytype
                return info
            else:
                return el["errors"][0]["message"]
        else:
            return None

    def friends(self, user):
        user = getuser(user)
        if user:
            el = requests.get(f"https://friends.roblox.com/v1/users/{user}/friends")
            el = json.loads(el.text)
            if "errors" not in el:
                info = {}
                for foo in el["data"]:
                    info[foo["name"]] = {
                        "name": foo["name"],
                        "id": foo["id"],
                    }
                return info
            else:
                return el["errors"][0]["message"]
        else:
            return None

    def groups(self, user):
        user = getuser(user)
        if user:
            el = requests.get(f"https://groups.roblox.com/v1/users/{user}/groups/roles")
            el = json.loads(el.text)
            if "errors" not in el:
                info = {}
                for foo in el["data"]:
                    info[foo["group"]["name"]] = {
                        "id": foo["group"]["id"],
                        "role": {
                            "name": foo["role"]["name"],
                            "id": foo["role"]["id"]
                        }
                    }
                return info
            else:
                return el["errors"][0]["message"]
        else:
            return None

class _group():
    def __init__(self, rosec):
        self._rosec = rosec
    
    def info(self, id):
        el = requests.get(f"https://groups.roblox.com/v1/groups/{id}")
        el = json.loads(el.text)
        foo = requests.get("https://thumbnails.roblox.com/v1/groups/icons", params={"groupIds": id, "size": "420x420", "format": "png"})
        foo = json.loads(foo.text)
        if "errors" not in el:
            info = {
                "name": el["name"],
                "id": el["id"],
                "description": el["description"],
                "members": el["memberCount"],
                "private": el["publicEntryAllowed"],
                "owner": {
                    "name": el["owner"]["username"],
                    "id": el["owner"]["userId"]
                },
                "avatar": foo["data"][0]["imageUrl"]
            }
            return info
        else:
            return el["errors"][0]["message"]
    
    def roles(self, id):
        el = requests.get(f"https://groups.roblox.com/v1/groups/{id}/roles")
        el = json.loads(el.text)
        if "errors" not in el:
            all = {}
            for foo in el["roles"]:
                all[foo["name"]] = {
                    "id": foo["id"],
                    "rank": foo["rank"],
                    "holders": foo["memberCount"]
                }
            return all
        else:
            return el["errors"][0]["message"]
    
    def shout(self, id, shout):
        rosec = self._rosec
        if rosec:
            rscheck = checkrs(rosec)
            if rscheck:
                el = requests.patch(f"https://groups.roblox.com/v1/groups/{id}/status", cookies={".ROBLOSECURITY": rosec}, json={"message": shout})
                el = requests.patch(f"https://groups.roblox.com/v1/groups/{id}/status", cookies={".ROBLOSECURITY": rosec}, json={"message": shout}, headers={"x-csrf-token": el.headers["x-csrf-token"]})
                el = json.loads(el.text)
                if "errors" in el:
                    return el["errors"][0]["message"]
                else:
                    return "Shouted"
            else:
                return "Your roblosecurity is invalid"
        else:
            return "You don't have a connected roblosecurity"
    
    def accept(self, groupid, user):
        rosec = self._rosec
        if rosec:
            rscheck = checkrs(rosec)
            if rscheck:
                isint = True
                try:
                    user = int(user)
                except:
                    isint = None
                if not isint:
                    user = getuser(user)
                    if not user:
                        return "Invalid user"
                el = requests.post(f"https://groups.roblox.com/v1/groups/{groupid}/join-requests/users/{user}", cookies={".ROBLOSECURITY": rosec})
                el = requests.post(f"https://groups.roblox.com/v1/groups/{groupid}/join-requests/users/{user}", cookies={".ROBLOSECURITY": rosec}, headers={"x-csrf-token": el.headers["x-csrf-token"]})
                el = json.loads(el.text)
                if "errors" in el:
                    return el["errors"][0]["message"]
                else:
                    return "Accepted"
            else:
                return "Your roblosecurity is invalid"
        else:
            return "You don't have a connected roblosecurity"

    def acceptall(self, groupid):
        rosec = self._rosec
        if rosec:
            rscheck = checkrs(rosec)
            if rscheck:
                alluserids = []
                el = requests.get(f"https://groups.roblox.com/v1/groups/{groupid}/join-requests", params={"limit": 100}, cookies={".ROBLOSECURITY": rosec})
                el = json.loads(el.text)
                while len(el["data"]) == 100:
                    for foo in el["data"]:
                        alluserids.append(foo["requester"]["userId"])
                    el = requests.get(f"https://groups.roblox.com/v1/groups/{groupid}/join-requests", params={"limit": 100, "cursor": el["nextPageCursor"]}, cookies={".ROBLOSECURITY": rosec})
                for foo in el["data"]:
                    if foo["requester"]["userId"] not in alluserids:
                        alluserids.append(foo["requester"]["userId"])
                errors = []
                for el in alluserids:
                    foo = requests.post(f"https://groups.roblox.com/v1/groups/{groupId}/join-requests/users/{el}", cookies={".ROBLOSECURITY": rosec})
                    foo = requests.post(f"https://groups.roblox.com/v1/groups/{groupId}/join-requests/users/{el}", cookies={".ROBLOSECURITY": rosec}, headers={"x-csrf-token": el.headers["x-csrf-token"]})
                    if "errors" in foo:
                        errors.append(foo["errors"]["message"])
                if len(errors) > 0:
                    message = {}
                    message["tried"] = "Tried to accept all, but got the following errors"
                    for el in errors:
                        if el not in message:
                            message[el] = errors.count(el)
                    return message
                else:
                    return "All accepted"
            else:
                return "Your roblosecurity is invalid"
        else:
            return "You don't have a connected roblosecurity"

    def declineall(self, groupid):
        rosec = self._rosec
        if rosec:
            rscheck = checkrs(rosec)
            if rscheck:
                alluserids = []
                el = requests.get(f"https://groups.roblox.com/v1/groups/{groupid}/join-requests", params={"limit": 100}, cookies={".ROBLOSECURITY": rosec})
                el = json.loads(el.text)
                while len(el["data"]) == 100:
                    for foo in el["data"]:
                        alluserids.append(foo["requester"]["userId"])
                    el = requests.get(f"https://groups.roblox.com/v1/groups/{groupid}/join-requests", params={"limit": 100, "cursor": el["nextPageCursor"]}, cookies={".ROBLOSECURITY": rosec})
                for foo in el["data"]:
                    if foo["requester"]["userId"] not in alluserids:
                        alluserids.append(foo["requester"]["userId"])
                errors = []
                for el in alluserids:
                    foo = requests.delete(f"https://groups.roblox.com/v1/groups/{groupId}/join-requests/users/{el}", cookies={".ROBLOSECURITY": rosec})
                    foo = requests.delete(f"https://groups.roblox.com/v1/groups/{groupId}/join-requests/users/{el}", cookies={".ROBLOSECURITY": rosec}, headers={"x-csrf-token": el.headers["x-csrf-token"]})
                    if "errors" in foo:
                        errors.append(foo["errors"]["message"])
                if len(errors) > 0:
                    message = {}
                    message["tried"] = "Tried to decline all, but got the following errors"
                    for el in errors:
                        if el not in message:
                            message[el] = errors.count(el)
                    return message
                else:
                    return "All accepted"
            else:
                return "Your roblosecurity is invalid"
        else:
            return "You don't have a connected roblosecurity"
    
    def rank(self, groupid, user, rank):
        rosec = self._rosec
        if rosec:
            rscheck = checkrs(rosec)
            if rscheck:
                isint = True
                try:
                    user = int(user)
                except:
                    isint = None
                if not isint:
                    user = getuser(user)
                    if not user:
                        return "Invalid user"
                el = requests.get(f"https://users.roblox.com/v1/users/{user}")
                el = json.loads(el.text)
                if "errors" not in el:
                    try:
                        rank = int(rank)
                        isint = True
                    except:
                        isint = None
                    if isint:
                        if rank <= 255:
                            el = requests.get(f"https://groups.roblox.com/v1/groups/{groupid}/roles")
                            el = json.loads(el.text)
                            if rank in [foo["rank"] for foo in el["roles"]]:
                                for bar in el["roles"]:
                                    if bar["rank"] == rank:
                                        rank = bar["id"]
                                el = requests.patch(f"https://groups.roblox.com/v1/groups/{groupid}/users/{user}", data={"roleId": rank}, cookies={".ROBLOSECURITY": rosec})
                                el = requests.patch(f"https://groups.roblox.com/v1/groups/{groupid}/users/{user}", data={"roleId": rank}, cookies={".ROBLOSECURITY": rosec}, headers={"x-csrf-token": el.headers["x-csrf-token"]})
                                el = json.loads(el.text)
                                if "errors" in el:
                                    return el["errors"][0]["message"]
                                else:
                                    return "Ranked"
                            else:
                                return "A rank with that id doesn't exist in that group"
                        else:
                            el = requests.get("https://groups.roblox.com/v1/roles", params={"ids": rank})
                            el = json.loads(el.text)
                            if "errors" in el:
                                return el["errors"][0]["message"]
                            else:
                                if el["data"][0]["groupId"] == groupid:
                                    el = requests.patch(f"https://groups.roblox.com/v1/groups/{groupid}/users/{user}", data={"roleId": rank}, cookies={".ROBLOSECURITY": rosec})
                                    el = requests.patch(f"https://groups.roblox.com/v1/groups/{groupid}/users/{user}", data={"roleId": rank}, cookies={".ROBLOSECURITY": rosec}, headers={"x-csrf-token": el.headers["x-csrf-token"]})
                                    el = json.loads(el.text)
                                    if "errors" in el:
                                        return el["errors"][0]["message"]
                                    else:
                                        return "Ranked"
                                else:
                                    return "That rank id doesn't belong to the group id sent"
                    else:
                        el = requests.get(f"https://groups.roblox.com/v1/groups/{groupid}/roles")
                        el = json.loads(el.text)
                        if rank.lower() in [foo["name"].lower() for foo in el["roles"]]:
                            for foo in el["roles"]:
                                if foo["name"] == rank:
                                    rank = foo["id"]
                            el = requests.patch(f"https://groups.roblox.com/v1/groups/{groupid}/users/{user}", data={"roleId": rank}, cookies={".ROBLOSECURITY": rosec})
                            el = requests.patch(f"https://groups.roblox.com/v1/groups/{groupid}/users/{user}", data={"roleId": rank}, cookies={".ROBLOSECURITY": rosec}, headers={"x-csrf-token": el.headers["x-csrf-token"]})
                            el = json.loads(el.text)
                            if "errors" in el:
                                return el["errors"][0]["message"]
                            else:
                                return "Ranked"
                        else:
                            return "That rank doesn't exist in that group"
                else:
                    return "An account with that id doesn't exist"
            else:
                return "Your roblosecurity is invalid"
        else:
            return "You don't have a connected roblosecurity"
    
    def exile(self, groupid, user):
        rosec = self._rosec
        if rosec:
            rscheck = checkrs(rosec)
            if rscheck:
                isint = True
                try:
                    user = int(user)
                except:
                    isint = None
                if not isint:
                    user = getuser(user)
                    if not user:
                        return "Invalid user"
                el = requests.delete(f"https://groups.roblox.com/v1/groups/{groupid}/users/{user}", cookies={".ROBLOSECURITY": rosec})
                el = requests.delete(f"https://groups.roblox.com/v1/groups/{groupid}/users/{user}", cookies={".ROBLOSECURITY": rosec}, headers={"x-csrf-token": el.headers["x-csrf-token"]})
                el = json.loads(el.text)
                if "errors" in el:
                    return el["errors"][0]["message"]
                else:
                    return "Exiled"
            else:
                return "Your roblosecurity is invalid"
        else:
            return "You don't have a connected roblosecurity"