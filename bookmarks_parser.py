import argparse
import sys
import re


parser = argparse.ArgumentParser(description='Parse a HTML bookmark file.')

group_folders_displaying = parser.add_mutually_exclusive_group()
group_folders_matching = parser.add_mutually_exclusive_group()

parser.add_argument('bookmarks_file', metavar='<bookmarks file>',
    help='the path of the bookmark file')
parser.add_argument('-folders', '--list-folders', action='store_true', default=False,
    help='list the folders (default)')
parser.add_argument('-links', '--list-links', action='store_true', default=False,
    help='list the links (default)')
parser.add_argument('-hr', '--list-hr', action='store_true', default=False,
    help='list the hr elements (default)')
parser.add_argument('-r', '--list-results', action='store_true', default=False,
    help='list the results numbers')
parser.add_argument('-i', '--list-index', action='store_true', default=False,
    help='list the index numbers')
parser.add_argument('-e', '--extended-parsing', action='store_true', default=False,
    help='alternative display easily manipulable for developers')
parser.add_argument('-j', '--json', action='store_true', default=False,
    help='output in JSON format')
group_folders_displaying.add_argument('--folders-name', action='store_true', default=False,
    help='display the folders name (default)')
group_folders_displaying.add_argument('--folders-path', action='store_true', default=False,
    help='display the folders path')
group_folders_matching.add_argument('--folders-case_sensitive', metavar='<folder name>', default=False,
    help='list all folders matching <folder name> with case sensitive.')
group_folders_matching.add_argument('--folders-case_insensitive', metavar='<folder name>', default=False,
    help='list all folders matching <folder name> with case insensitive.')
group_folders_matching.add_argument('--folders-all-case_sensitive', metavar='<folder name>', default=False,
    help='list all content from folders matching <folder name> with case sensitive.')
group_folders_matching.add_argument('--folders-all-case_insensitive', metavar='<folder name>', default=False,
    help='list all content from folders matching <folder name> with case insensitive.')
parser.add_argument('--depth', metavar='<depth>', default=False,
    help='list the choosen depth only')
parser.add_argument('--spacing-style', metavar='<character>', default=False,
    help='Change the spacing style <character>. Valid characters are: [ ]/[,]/[-]/[_]  (default: [ ])')
parser.add_argument('--quoting-style', metavar='<character>', default=False,
    help='Change the quoting style <character>. Valid characters are: ["]/[\'].  (default: ["])')

args = parser.parse_args()

if not (args.list_folders or args.list_links or args.list_hr):
    args.list_folders = True
    args.list_links = True
    args.list_hr = True
if not args.depth == False:
    args.depth = int(args.depth)
SPACING_STYLE = args.spacing_style
if not SPACING_STYLE in [' ', ",", "-", "_"]:
    SPACING_STYLE = ' '
QUOTING_STYLE = args.quoting_style
if not QUOTING_STYLE in ['"', "'", ""]:
    QUOTING_STYLE = '"'

HTML_FOLDER_RE = re.compile(r'<DT><H3 [^>]*>(?P<name>[^<]*)</H3>', re.IGNORECASE)
HTML_LINK_RE = re.compile(r'<DT><A HREF="(?P<link>https?:[^"]+)"[^>]*>(?P<name>[^<]*)</A>', re.IGNORECASE)

sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")

depth = previous_depth = results = index = 0
link = name = ""
list_path = []
path = []
depth_scan = html_open_dl_p = html_closed_dl_p = previous_line_open_dl_p = False
regexes = r'(?P<html_open_dl_p><DL><p>)', r'(?P<html_hr><HR>)', r'(?P<html_folder><DT><H3 [^>]*>[^<]*</H3>)', r'(?P<html_link><DT><A HREF="https?:[^"]+"[^>]*>[^<]*</A>)', r'(?P<html_closed_dl_p></DL><p>)'
combinedRegex = re.compile('|'.join(regexes), re.IGNORECASE)


def quote(item):
    return f"{QUOTING_STYLE}{item}{QUOTING_STYLE}"


result_list = []

for line in open(args.bookmarks_file, "r", encoding="utf-8"):
    if html_open_dl_p:
        previous_line_open_dl_p = html_open_dl_p
    else:
        previous_line_open_dl_p = False
    for html_open_dl_p, html_hr, html_folder, html_link, html_closed_dl_p in combinedRegex.findall(line):

        if html_closed_dl_p:
            if previous_line_open_dl_p:
                list_path = list_path[:-1]
            continue
        elif html_open_dl_p:
            continue

        if args.list_index:
            index += 1

        if html_hr:
            name = "--------------------"
        elif html_folder:
            match = re.search(HTML_FOLDER_RE, html_folder)
            assert match
            name = match["name"]
        elif html_link:
            match = re.search(HTML_LINK_RE, html_link)
            assert match
            link, name = match.group("link", "name")

        previous_depth = depth
        depth = ((len(line) - len(line.lstrip(" "))) // 4) - 1

        if (html_hr or html_folder or html_link):
            if args.folders_path:
                if depth < previous_depth:
                    list_path = list_path[:-(previous_depth - depth)]
                if html_folder:
                    list_path.append(name.replace("\\", "\\\\").replace("/", "\\/") + "/")
                    if args.extended_parsing:
                        path = "".join(list_path[:-1])[:-1]
                else:
                    path = "".join(list_path)[:-1]

        if args.depth is not False:
            if not depth == args.depth:
                continue

        if args.folders_case_sensitive or args.folders_case_insensitive:
            if not html_folder:
                continue
            if (args.folders_case_sensitive and name != args.folders_case_sensitive) or (args.folders_case_insensitive and name.lower() != args.folders_case_insensitive.lower()):
                continue

        if args.folders_all_case_sensitive or args.folders_all_case_insensitive:
            if depth_scan is False:
                if html_folder and ((args.folders_all_case_insensitive and name.lower() == args.folders_all_case_insensitive.lower()) or
                                    (not args.folders_all_case_insensitive and name == args.folders_all_case_sensitive)):
                    depth_scan = depth
                else:
                    continue
            elif depth <= depth_scan:
                depth_scan = False
                continue

        if html_hr and not args.list_hr:
            continue
        elif html_folder and not args.list_folders:
            continue
        elif html_link and not args.list_links:
            continue
        elif not (html_hr or html_folder or html_link):
            continue

        results += 1

        if html_hr:
            item = "HR"
        elif html_folder:
            item = "FOLDER"
        elif html_link:
            item = "LINK"
        elif args.folders_path:
            item = "PATH"

        items = [item, depth]

        if args.list_results:
            items.append(results)
        if args.list_index:
            items.append(index)
        if args.folders_path:
            items.append(path)
        if html_link:
            items.append(link)
        items.append(name)

        if args.json:
            result_list.append(items)
            continue

        quoted = list(map(quote, items))

        if args.extended_parsing:
            print(f"{SPACING_STYLE}".join(quoted))
        else:
            prefix = "-" * depth if html_folder else " " * (depth + 1)
            print(f"{prefix}- {SPACING_STYLE.join(quoted[2:])}")


if args.json and result_list:
    import json

    json.dump(result_list, sys.stdout)
