"""
Get Steam group user list as id64.

Original Author: TerryDEV (2016)
https://github.com/bommels/steam-group-members
"""

import requests
from lxml import etree as et


class SteamGroup:
    """
    This Python class fetches the SteamID64's of all the Steam group members.
    """

    XML_URL = ''  # Add your custom group URL here
    XML_NEXT_PAGE = False
    XML_PAGE = 1
    REQUEST_TIMEOUT = 3.00  # in seconds

    STEAM_IDS = []

    def __init__(self):
        pass

    def get_steam_ids(self, page=XML_PAGE):
        """
        Process the response from the get function (xml in text) and save
        SteamID64 to an array.
        Uses get_steam_ids as a recursive function to fetch all the pages.
        :param page: the XML page, max is 1000 members per page.
        :return: the response XML in text format.
        """

        response = self.get(page)
        if response is None:
            return None

        try:
            root = et.fromstring(bytes(response, encoding='utf8'))
        except et.ParseError:
            members = None
            print(response)
        else:
            members = root.find('members')

        if members is None:
            return None

        for steamid in members.findall('steamID64'):
            self.STEAM_IDS.append(int(steamid.text))

        if root.findall('nextPageLink'):
            page += 1
            return self.get_steam_ids(page)

        steamids = self.STEAM_IDS
        self.STEAM_IDS = []

        return steamids

    def get(self, page):
        """
        Gets the XML GroupMembers from Steam, no API key required.
        :param page: the page, max 1000 members per page.
        :return: the response, return None is not a valid response.
        """

        url = self.XML_URL + '&p=%s' % page

        response = None
        try:
            response = requests.get(url, timeout=self.REQUEST_TIMEOUT)
            if response.status_code != 200:
                return None
        except requests.Timeout as e:
            print(e)
        except requests.RequestException as e:
            print(e)

        if response is None:
            return None

        return response.text

    def set_url(self, url):
        self.XML_URL = url + '/memberslistxml?xml=1'
