class Error:
    def __init__(self, data):
        self.json = data
        self.data = data if type(data) == dict else {}
        self.code = self.data.get("code")
        self.message = self.data.get("message")


class UserInfo:
    def __init__(self, data):
        self.json = data
        self.data = data.get("data", data)
        self.avatar = self.data.get("avatar")
        self.avatars = self.data.get("avatars")
        self.country = self.data.get("country")
        self.displayName = self.data.get("displayName")
        self.handel = self.data.get("handel")
        self.hideLocation = self.data.get("hideLocation")
        self.id = self.data.get("id")
        self.lat = self.data.get("lat")
        self.lng = self.data.get("lng")
        self.name = self.data.get("name")
        self.socialAvatar = self.data.get("socialAvatar")


class UsersList:
    def __init__(self, data):
        self.json = data
        self.data = data.get("data", data) if type(data) is dict else data
        self.users = []
        for user in self.data if self.data else []:
            self.users.append(UserInfo(user))


class MeshInfo:
    def __init__(self, data):
        self.json = data
        self.data = self.json.get("data", self.json) if "data" in self.json else self.json
        self.channel = self.data.get("channel")
        self.createdAt = self.data.get("createdAt")
        self.currentState = self.data.get("currentState")
        self.explicit = self.data.get("explicit")
        self.id = self.data.get("id")
        self.isFriend = self.data.get("isFriend")
        self.isLocal = self.data.get("isLocal")
        self.isPublic = self.data.get("isPublic")
        self.kickMode = self.data.get("kickMode")
        self.maturity = self.data.get("maturity")
        self.mediaUrl = self.data.get("mediaUrl")
        self.originator = self.data.get("originator")
        self.playMode = self.data.get("playMode")
        self.position = self.data.get("position")
        self.server = self.data.get("server")
        self.thumbnails = self.data.get("thumbnails")
        self.time = self.data.get("time")
        self.users = UsersList(self.data.get("users")).users
        self.videoAuthor = self.data.get("videoAuthor")
        self.videoDuration = self.data.get("videoDuration")
        self.videoProvider = self.data.get("videoProvider")
        self.videoPublishedAt = self.data.get("videoPublishedAt")
        self.videoThumbnail = self.data.get("videoThumbnail")
        self.videoTitle = self.data.get("videoTitle")
        self.videoUrl = self.data.get("videoUrl")
        self.vikiPass = self.data.get("vikiPass")
        self.voipMode = self.data.get("voipMode")


class MeshesList:
    def __init__(self, data):
        self.json = data
        self.data = data.get("data", data) if type(data) is dict else data
        self.meshes = []
        self.users = []
        for mesh in self.data:
            self.meshes.append(MeshInfo(mesh.get("mesh")))
            self.users.append(UsersList(mesh.get("users")))


class MojoOAuth:
    def __init__(self, data):
        self.json = data
        self.access_token = self.json.get("access_token")
        self.id_token = self.json.get("id_token")
        self.refresh_token = self.json.get("refresh_token")
        self.expires_in = self.json.get("expires_in")
        self.token_type = self.json.get("token_type")


class MojoUser:
    def __init__(self, data):
        self.json = data
        self.created_at = self.json.get("created_at")
        self.updated_at = self.json.get("updated_at")
        self.issuer = self.json.get("issuer")
        self.user_id = self.json.get("user_id")
        self.identifier = self.json.get("identifier")
        self.email = self.json.get("email")


class MojoStatus:
    def __init__(self, data):
        self.json = data
        self.authenticated = self.json.get("authenticated")
        self.oauth = MojoOAuth(self.json.get("oauth", {}))
        self.user = MojoUser(self.json.get("user", {}))


class SoborolUser:
    def __init__(self, data):
        self.json = data.json()
        self.token = self.json.get("sessionToken")


class CheckUsername:
    def __init__(self, data):
        self.json = data
        self.data = self.json.get("data", {}) if type(self.json) == dict else {}
        self.isValid = self.data.get("isValid")
        self.suggestedHandles = self.data.get("suggestedHandles")
        self.error = Error(self.data.get("error"))
