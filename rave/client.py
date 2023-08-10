import time

from .api.service import Service
from .api import headers
from .api.models import *
from .api.utils import generate_deviceId, nonce
from .socket import Socket
from json import dumps


class Client(Socket, Service):
    def __init__(self, proxies: dict = None):
        Service.__init__(self, proxies)
        self.token = None
        self.deviceId = generate_deviceId()

    def request_verification(self, email: str, language: str = "en"):
        params = {
            "language": language,
            "redirect_url": "https://rave.watch/mojoauth"
        }
        return self.mojo_post("/users/magiclink", {"email": email}, params)["state_id"]

    def get_mojo_status(self, state_id: str):
        return MojoStatus(self.mojo_get("/users/status", params={"state_id": state_id}))

    def soborol_login(self, email: str, mojo_id_token: str):
        data = dumps({
            "authData": {
                "mojo": {
                    "id_token": mojo_id_token,
                    "id": email
                }
            }
        })
        return SoborolUser(self.postSoboro("https://api.soborol.com/parse/users", data))

    def login(self, email, password, **kwargs):
        # TODO: login
        # headers.token = None
        # self.token = headers.token
        # return response
        raise NotImplementedError

    def authenticate(self, email: str) -> SoborolUser:
        verification_request = self.request_verification(email)
        while True:
            time.sleep(1)
            mojo_status = self.get_mojo_status(verification_request)

            if mojo_status.authenticated:
                id_token = mojo_status.oauth.id_token
                authenticated_email = mojo_status.user.email
                return self.soborol_login(authenticated_email, id_token)

    def login_token(self, token):
        headers.token = token
        self.token = headers.token
        return UserInfo(self.get("/users/self"))

    def check_username(self, username: str):
        return CheckUsername(self.post(f"/users/self/handle", {"handle": username}))

    def get_account_info(self):
        return UserInfo(self.get("/users/self"))

    def get_user_info(self, userId: str):
        return UserInfo(self.get(f"/users/{userId}"))

    def edit_profile(self, displayName: str = None, handel: str = None, displayAvatar: str = None):
        data = {}
        if displayName:
            data["displayName"] = displayName
        if handel:
            data["handel"] = handel
        if displayAvatar:
            data["displayAvatar"] = displayAvatar

        data = dumps(data)
        return self.put("/users/self", data)

    def delete_display(self, displayAvatar: bool = False, displayName: bool = False):
        data = {
            "displayName": displayName,
            "displayAvatar": displayAvatar
        }
        return self.delete("/users/self/display", data)

    def edit_push_notifications(self, friendsOnly: bool = False):
        return self.post("/users/self/notification_prefs",
                         {"friendsOnly": friendsOnly})

    def hide_location(self, hide: bool = True):
        return self.post("/users/self/location", {"hideLocation": hide})

    def hide_maturity_content(self, hide: bool = False):
        return self.post("/users/self/maturity", {"hideMature": hide})

    def set_birthday(self, date: str = None):
        return self.post("/users/self/dob", {"date": date})

    def get_avatar_upload_url(self):
        return self.post("/users/self/avatar/upload", {"mime": "image/jpeg"})

    def add_friend(self, userId: str):
        return self.post("/friendships", {"id": userId})

    def remove_friend(self, userId: str):
        return self.delete("/friendships/unfriend", {"id": userId})

    def get_friendships_requests(self):
        return UsersList(self.get("/friendships/requests", {"state": "pendingactionable"}).get("data"))

    def accept_friend(self, userId: str):
        return self.post("/friendships", {"id": userId, "state": "friends"})

    def search_users(self, search_for: str, friends: bool = True, recent: bool = False, all: bool = True):
        return UsersList(
            self.get("/users/search?q=rahaf", {"q": search_for, "friends": friends, "recents": recent, "all": all}))

    def get_friendships(self, limit: int = 24):
        return UsersList(self.get("/friendships", {"limit": limit}))

    def get_contacts(self, limit: int = 24):
        return UsersList(self.get("/contacts", {"limit": limit}))

    def get_blocked_users(self, limit: int = 24):
        return UsersList(self.get("/users/self/blocks", {"limit": limit}))

    def block(self, userId: str):
        return self.post("/users/self/blocks", {"id": userId})

    def unblock(self, userId: str):
        return self.delete(f"/users/self/blocks/{userId}")

    def create_mesh(self, video_url: str):
        return self.post("/meshes", {"url": video_url})

    def get_meshes(
            self,
            limit: int = 1,
            public: bool = False,
            local: bool = False,
            invited: bool = False,
            lang: str = "en"
    ):
        params = {
            "deviceId": self.deviceId,
            "public": public,
            "local": local,
            "invited": invited,
            "limit": limit, "lang": lang
        }
        return MeshesList(self.get("/meshes/self", params))

    def get_mesh_info(self, meshId: str):
        return MeshInfo(self.get(f"/meshes/{meshId}"))

    def invite_to_mesh(self, meshId: str, usersId: list):
        data = {"deviceId": self.deviceId, "ids": usersId}
        return self.post(f"/meshes/{meshId}/invites", data)

    def leave_mesh(self, meshId: str):
        return self.delete(f"/meshes/{meshId}/devices/{self.deviceId}/leave")

    def like_mesh_video(self, meshId: str, video_url):
        data = {"opinion": "LIKE", "url": video_url, "videoInstanceId": nonce()}
        return self.put(f"/meshes/{meshId}/likeskip", data)

    def dislike_mesh_video(self, meshId: str, video_url):
        data = {"opinion": "LIKE", "url": video_url, "videoInstanceId": nonce()}
        return self.delete(f"/meshes/{meshId}/likeskip", data)

    # TODO: def get_mesh_videos_queue(self, meshId: str):

    def edit_mesh(self, meshId: str, voipMode: str = "ALL", isFriend: bool = False, isLocal: bool = False,
                  isPublic: bool = True, lat: float = 0.0, lng: float = 0.0, radius: float = 0.0):
        data = {
            "isFriend": isFriend,
            "isLocal": isLocal,
            "isPublic": isPublic,
            "lat": lat,
            "lng": lng,
            "playMode": "VOTE",
            "radius": radius,
            "voipMode": voipMode  # ALL: Everyone can join the mice chat, OFF: No one can join the mice chat
        }
        data = dumps(data)
        return self.put(f"/meshes/{meshId}", data)

    def transfer_mesh_leader(self, meshId: str, userId: str):
        return self.post(f"/meshes/{meshId}/transferleadership", {"newLeaderId": userId})

    def kick_mesh_users(self, meshId: str, usersId: str):
        return self.post(f"/meshes/{meshId}/kick", {"deviceId": "f6d57a9af6fa46daac6964ad1c2e54ca", "ids": usersId})

    def mute_mesh_user(self, meshId: str, userId: str):
        return self.post(f"/meshes/{meshId}/mute/{userId}", {})

    def unmute_mesh_user(self, meshId: str, userId: str):
        return self.post(f"/meshes/{meshId}/unmute/{userId}", {})

    def clear_mesh_videos_queues(self, meshId: str):
        return self.delete("/users/self/queues", {"meshId": meshId})

    def connect_to_mesh(self, meshId: str):
        raise NotImplementedError
        # mesh = self.get_mesh_info(meshId)
        # roomId = mesh.id
        # port = 443
        # server = mesh.server
        # user = self.get_account_info()
        # peerId = str(user.id) + "_" + self.deviceId
        # socket_url = f"wss://{server}:{port}/?roomId={roomId}&peerId={peerId}"
        # Socket.__init__(self, socket_url, headers=headers.Headers().headers)
