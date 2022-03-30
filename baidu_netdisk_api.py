#! -*- coding: utf8 -*-
import json
import requests


class BaiduNetDiskAPI(object):
    """
    授权文档： https://developer.baidu.com/newwiki/dev-wiki/kai-fa-wen-dang.html?t=1557733846879
    网盘文档： https://pan.baidu.com/union/document/basic
    """
    def __init__(self, redirect_uri="http://localhost:8088/auth"):
        self.client_id = ""  # api key
        self.client_secret = ""  # secret_key
        self.redirect_uri = redirect_uri
        self.access_token_expire = 0   # Access Token的有效期，以秒为单位
        self._access_token = None
        self._refresh_token = None   # 用于刷新Access Token的Refresh Token，所有应用都会返回该参数（10年的有效期）

    @property
    def access_token(self):
        if self._access_token is None:
            raise ValueError("Please get user auth first")
        return self._access_token

    @access_token.setter
    def access_token(self, access_token):
        self._access_token = access_token

    @property
    def refresh_token(self):
        if self._refresh_token is None:
            raise ValueError("Please get user auth first")
        return self._refresh_token

    @refresh_token.setter
    def refresh_token(self, refresh_token):
        self._refresh_token = refresh_token

    def generate_user_code_url(self, force_login=0, scope="basic,netdisk"):
        api = "https://openapi.baidu.com/oauth/2.0/authorize"
        # params = "redirect_uri=oob&qrcode=1&force_login=1"
        # display:
        #     page：全屏形式的授权页面（默认），适用于web应用。
        #     popup：弹框形式的授权页面，适用于桌面软件应用和web应用。
        #     dialog：浮层形式的授权页面，只能用于站内web应用。
        #     mobile：IPhone/Android等智能移动终端上用的授权页面，适用于IPhone/Android等智能移动终端上的应用。
        #     pad：IPad/Android等平板上使用的授权页面，适用于IPad/Android等智能移动终端上的应用。
        #     tv：电视等超大显示屏使用的授权页面。
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "scope": scope,
            "redirect_uri": self.redirect_uri,
            "display": "popup",
            "qrcode": 1,  # 是否使用二维码登陆
            "force_login": force_login,  # 是否强制用户重新登陆
        }
        api_url = api + "?" + "&".join(map(lambda (k, v): "{}={}".format(k, v), params.items()))
        return api_url

    def get_access_token(self, user_code):
        api = "https://openapi.baidu.com/oauth/2.0/token"
        payload = {
            "grant_type": "authorization_code",
            "code": user_code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri
        }
        response = requests.get(api, params=payload)
        response.raise_for_status()
        result = response.json()
        self.access_token = result["access_token"]
        self.refresh_token = result["refresh_token"]
        self.access_token_expire = result["expires_in"]
        return result

    def refresh_access_token(self):
        api = "https://openapi.baidu.com/oauth/2.0/token"
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = requests.get(api, params=payload)
        response.raise_for_status()
        result = response.json()
        self.access_token = result["access_token"]
        self.refresh_token = result["refresh_token"]
        self.access_token_expire = result["expires_in"]
        return result

    def get_user_info(self):
        api = "https://pan.baidu.com/rest/2.0/xpan/nas"
        payload = {
            "method": "uinfo",
            "access_token": self.access_token,
        }
        response = requests.get(api, params=payload)
        response.raise_for_status()
        return response.json()

    def get_file_list(self, dirname="/pwdata"):
        api = "https://pan.baidu.com/rest/2.0/xpan/file"
        params = {
            "method": "list",
            "access_token": self.access_token,
            "dir": dirname,
            "folder": 0,
            "showempty": 1,
        }
        response = requests.get(api, params=params)
        response.raise_for_status()
        return response.json()

    def get_file_detail(self, fsids, path="/pwdata", has_thumb=False, has_dlink=False, has_extra=False):
        api = "https://pan.baidu.com/rest/2.0/xpan/multimedia"
        params = {
            "method": "filemetas",
            "access_token": self.access_token,
            "path": path,
            "fsids": json.dumps(fsids),
            "thumb": int(has_thumb),
            "dlink": int(has_dlink),
            "extra": int(has_extra)
        }
        response = requests.get(api, params=params)
        response.raise_for_status()
        return response.json()

    def download_file_from_dlink(self, dlink, path, chunk_size=10*1024*1024):
        response = requests.get(dlink, stream=True, params={"access_token": self.access_token}, headers={"User-Agent": "pan.baidu.com"})
        with open(path, "wb") as fp:
            for chunk in response.iter_content(chunk_size=chunk_size):
                fp.write(chunk)


def main():
    netdisk_api = BaiduNetDiskAPI()
    netdisk_api.access_token = ""
    res = netdisk_api.get_file_list()
    print(json.dumps(res, indent=2))

    res = netdisk_api.get_file_detail([1122248572614088], has_dlink=True)
    print(json.dumps(res, indent=2))

    res = netdisk_api.download_file_from_dlink("")


if __name__ == '__main__':
    main()
