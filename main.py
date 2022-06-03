"""
Simple lister for Steam groups. No API keys.
"""

__version__ = '0.0.1'
__author__ = 'rez_spb'
__date__ = '2022-06-03'

import SteamGroup
import SteamUserInfo

steam_group_url = "https://steamcommunity.com/groups/last-day"  # TODO: param
avatars = False  # TODO: config/param
users = []

steam_group = SteamGroup.SteamGroup()
steam_group.set_url(steam_group_url)
group_users = steam_group.get_steam_ids()

for n, user in enumerate(group_users, start=1):
    si = SteamUserInfo.SteamUserInfo()
    si.parse_id64(str(user))
    name = si.username
    custom_url = si.custom_url
    line = f"{n:02d}. {si.id64}: {name}"
    if custom_url:
        line = line + f" ({custom_url})"
    if avatars:
        line = line + f" | {si.avatar}"
    users.append(line)

for u in users:
    print(u)
