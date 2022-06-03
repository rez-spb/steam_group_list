"""
Simple lister for Steam groups. No API keys.
"""

__version__ = '0.0.2'
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
    print("""
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
        <meta http-equiv="content-type" content="application/xml; charset=utf-8" />
        <title>Steam Group User List</title>
    </head>
    <body>
        <h1>Steam Group User List</h1>
        <table>
            <tr><th>#</th><th>avatar</th><th>name</th><th>id64</th></tr>
""", file=fd)

    for n, u_obj in enumerate(users, start=1):
        print("<tr>", file=fd)
        print(f"<td>{n:02d}</td>", file=fd)  # #
        print(f"<td><img src='{u_obj.avatar}' /></td>", file=fd)  # avatar
        print(f"<td>{u_obj.username}", file=fd)  # name
        if u_obj.custom_url:
            print(f" ({u_obj.custom_url})", file=fd)
        print("</td>", file=fd)
        print(f"<td>{u_obj.id64}</td>", file=fd)  # id64
        print("</tr>", file=fd)

    print(
        """
        </table>
    </body>
</html>""", file=fd)


for user in group_users:
    si = SteamUserInfo.SteamUserInfo()
    si.parse_id64(str(user))
    users.append(si)

printer_console(users)

with open('out.html', 'w') as of:
    printer_html(users, of)
