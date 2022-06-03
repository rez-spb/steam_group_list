"""
Get Steam user info by ID64.
"""

import requests
from lxml import etree as et


class SteamUserInfo:
    url_base = "https://steamcommunity.com/profiles/"
    url_suffix = "?xml=1"

    username = None
    avatar = None
    id64 = None
    custom_url = None

    def __init__(self):
        pass

    def parse_id64(self, id64):
        """
        Fill the instance with valid data.
        Lacks check for ratelimit etc.
        Probably should be done in init block.

        :param id64: valid SteamID64 for a user.
        :return: None
        """
        url = self.url_base + id64 + self.url_suffix
        raw_xml = None
        with requests.Session() as s:
            response = s.get(url)
            if response.ok:
                raw_xml = response.text

        root = et.fromstring(bytes(raw_xml, encoding='utf8'))

        self.id64 = id64
        self.username = root.xpath("//steamID")[0].text
        self.avatar = root.xpath("//avatarMedium")[0].text
        try:
            self.custom_url = root.xpath("//customURL")[0].text
        except IndexError:
            pass
