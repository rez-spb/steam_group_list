"""
Simple lister for Steam groups. No API keys.
"""

__version__ = '0.0.4'
__author__ = 'rez_spb'
__date__ = '2022-06-03'

import SteamGroup
import SteamUserInfo

steam_group_url = "https://steamcommunity.com/groups/last-day"  # TODO: param
avatars = False  # TODO: config/param
obfuscate_id = True  # TODO: config/param
users = []

steam_group = SteamGroup.SteamGroup()
steam_group.set_url(steam_group_url)
group_users = steam_group.get_steam_ids()
group_name = steam_group.group_name


def obfuscator(id64):
    return f"{id64[:2]}...{id64[-5:]}"


def printer_console(users):
    for n, user in enumerate(users, start=1):
        name = user.username
        custom_url = user.custom_url
        line = f"{n:02d}. {user.id64}: {name}"
        if custom_url:
            line = line + f" ({custom_url})"
        if avatars:
            line = line + f" | {user.avatar}"
        print(line)


def printer_html(users, fd):
    lines = []
    style = """
table td th {
    padding: 1px 3px;
    }
th {
    border-bottom: 3px double black;
    }
td {
    border-bottom: 1px dashed black;
    }
        """
    header = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
        <meta http-equiv="content-type" content="application/xml; charset=utf-8" />
        <title>{group_name} User List</title>
        <style type="text/css">{style}</style>
    </head>
    <body>
        <h1>{group_name} User List</h1>
        <table>
            <tr><th>#</th><th>avatar</th><th>name</th><th>id64</th></tr>
""".format(style=style, group_name=group_name)
    footer = "\n</table></body></html>"
    row_template = "<tr><td>{num:02d}</td>" \
                   "<td><img alt='{id64}' src='{avatar}' /></td>" \
                   "<td>{user}{url}</td><td>{id64}</td></tr>"
    for n, u_obj in enumerate(users, start=1):
        lines.append(row_template.format(
            num=n, avatar=u_obj.avatar, user=u_obj.username,
            url=f" ({u_obj.custom_url})" if u_obj.custom_url else '',
            id64=obfuscator(u_obj.id64) if obfuscate_id else u_obj.id64))
    print(header + '\n'.join(lines) + footer, file=fd)


for user in group_users:
    si = SteamUserInfo.SteamUserInfo()
    si.parse_id64(str(user))
    users.append(si)

printer_console(users)

with open('out.html', 'w') as of:
    printer_html(users, of)
