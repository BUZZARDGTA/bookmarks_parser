import argparse
import re
import sys

parser = argparse.ArgumentParser(description='Parse a HTML bookmark file.')

def callback_argparse__is_positive_int(value):
    try:
        int_value = int(value)
        if int_value >= 0:
            return int_value
        else:
            raise ValueError
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid positive int value: '{value}'")

group_folders_displaying = parser.add_mutually_exclusive_group()
group_folders_matching = parser.add_mutually_exclusive_group()

valid_spacing_characters = [' ', ',', '-', '_', '|']
valid_quoting_characters = ['"', "'", ""]

parser.add_argument('bookmarks_file', metavar='<bookmarks file>', type=str,
    help='the path of the bookmark file')
parser.add_argument('-folders', '--list-folders', action='store_true', default=False,
    help='list the folders (default)')
parser.add_argument('--list-folders-add_date', action='store_true', default=False,
    help='list the "ADD_DATE" attribute within \'--list-folders\'')
parser.add_argument('--list-folders-last_modified', action='store_true', default=False,
    help='list the "LAST_MODIFIED" attribute within \'--list-folders\'')
parser.add_argument('--list-folders-personal_toolbar_folder', action='store_true', default=False,
    help='list the "PERSONAL_TOOLBAR_FOLDER" attribute within \'--list-folders\'')
parser.add_argument('-links', '--list-links', action='store_true', default=False,
    help='list the links (default)')
parser.add_argument('--no-list-links-href', action='store_true', default=False,
    help='do not list the "HREF" attribute within \'--list-links\'')
parser.add_argument('--list-links-add_date', action='store_true', default=False,
    help='list the "ADD_DATE" attribute within \'--list-links\'')
parser.add_argument('--list-links-last_modified', action='store_true', default=False,
    help='list the "LAST_MODIFIED" attribute within \'--list-links\'')
parser.add_argument('--list-links-icon_uri', action='store_true', default=False,
    help='list the "ICON_URI" attribute within \'--list-links\'')
parser.add_argument('--list-links-icon', action='store_true', default=False,
    help='list the "ICON" attribute within \'--list-links\'')
parser.add_argument('--list-links-shortcuturl', action='store_true', default=False,
    help='list the "SHORTCUTURL" attribute within \'--list-links\'')
parser.add_argument('--list-links-tags', action='store_true', default=False,
    help='list the "TAGS" attribute within \'--list-links\'')
parser.add_argument('-hr', '--list-hr', action='store_true', default=False,
    help='list the hr elements (default)')
parser.add_argument('-i', '--list-index', action='store_true', default=False,
    help='list the index numbers')
parser.add_argument('-r', '--list-results', action='store_true', default=False,
    help='list the results numbers')
parser.add_argument('-e', '--extended-parsing', action='store_true', default=False,
    help='alternative display easily manipulable for developers')
parser.add_argument('-j', '--json', action='store_true', default=False,
    help='output in JSON format')
group_folders_displaying.add_argument('--folders-name', action='store_true', default=False,
    help='display the folders name (default)')
group_folders_displaying.add_argument('--folders-path', action='store_true', default=False,
    help='display the folders path')
parser.add_argument('--depth', metavar='<depth>', default=False, type=callback_argparse__is_positive_int,
    help='List all content within matching depth <depth>. It must be a positive number or zero. (default: -1)')
group_folders_matching.add_argument('--folders-case_sensitive', metavar='<folder name>', default=False, type=str,
    help='List all folders matching <folder name> with case sensitive.')
group_folders_matching.add_argument('--folders-case_insensitive', metavar='<folder name>', default=False, type=str,
    help='List all folders matching <folder name> with case insensitive.')
group_folders_matching.add_argument('--folders-all-case_sensitive', metavar='<folder name>', default=False, type=str,
    help='List all content from folders matching <folder name> with case sensitive.')
group_folders_matching.add_argument('--folders-all-case_insensitive', metavar='<folder name>', default=False, type=str,
    help='List all content from folders matching <folder name> with case insensitive.')
parser.add_argument('--export-personal_toolbar_folder', action='store_true', default=False,
    help='Exports the default bookmarks toolbar folder(s).')
parser.add_argument('--spacing-style', metavar='<character>', default=" ", choices=valid_spacing_characters, type=str,
    help=f"Change the spacing style <character>. Valid characters are: {valid_spacing_characters} (default: ' ')")
parser.add_argument('--quoting-style', metavar='<character>', default='"', choices=valid_quoting_characters, type=str,
    help=f"Change the quoting style <character>. Valid characters are: {valid_quoting_characters} (default: '\"')")

args = parser.parse_args()

if not (args.list_folders or args.list_links or args.list_hr):
    args.list_folders = True
    args.list_links = True
    args.list_hr = True

sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")

regexes = (
    r'(?P<html_open_dl_p><DL><p>)',
    r'(?P<html_hr><HR>)',
    r'(?P<html_folder><DT><H3[^>]*>(?P<folder__name>[^<]*)</H3>)',
    r'(?P<html_link><DT><A[^>]*>(?P<link__name>[^<]*)</A>)',
    r'(?P<html_closed_dl_p></DL><p>)'
)
PATTERNS_HTML = re.compile('|'.join(regexes), re.IGNORECASE)

# These patterns allow flexible extraction of attributes associated with bookmarks and help maintain the order of attributes, which can vary in the HTML structure.
PATTERN_HTML__ADD_DATE = re.compile(r'ADD_DATE="(?P<add_date>[0-9]+)"', re.IGNORECASE)
PATTERN_HTML__LAST_MODIFIED = re.compile(r'LAST_MODIFIED="(?P<last_modified>[0-9]+)"', re.IGNORECASE)
PATTERN_HTML_FOLDER__PERSONAL_TOOLBAR_FOLDER = re.compile(r'PERSONAL_TOOLBAR_FOLDER="(?P<folder__personal_toolbar_folder>true)"', re.IGNORECASE)
PATTERN_HTML_LINK__HREF = re.compile(r'HREF="(?P<link__href>[^"]+)"', re.IGNORECASE)
PATTERN_HTML_LINK__ICON_URI = re.compile(r'ICON_URI="(?P<link__icon_uri>[^"]+)"', re.IGNORECASE)
PATTERN_HTML_LINK__ICON = re.compile(r'ICON="(?P<link__icon>[^"]+)"', re.IGNORECASE)
PATTERN_HTML_LINK__SHORTCUTURL = re.compile(r'SHORTCUTURL="(?P<link__shortcuturl>[^"]+)"', re.IGNORECASE)
PATTERN_HTML_LINK__TAGS = re.compile(r'TAGS="(?P<link__tags>[^"]+)"', re.IGNORECASE)

depth = -1
previous_depth = results = index = 0
list_path = []
path = []
if args.json:
    result_list = []
depth_scan = False


def quote(item):
    return f"{args.quoting_style}{item}{args.quoting_style}"


def return_regex_match(regex: re.Pattern, content, group_match: str):
    match = regex.search(content)
    if match:
        return match[group_match]
    else:
        return ""


for line in open(args.bookmarks_file, "r", encoding="utf-8"):

    for html_open_dl_p, html_hr, html_folder, folder__name, html_link, link__name, html_closed_dl_p in PATTERNS_HTML.findall(line):
        if html_open_dl_p:
            depth += 1
            continue
        elif html_closed_dl_p:
            depth -= 1
            continue

        if args.list_index:
            index += 1


        if html_hr:
            name = "--------------------"
        elif html_folder:
            name = folder__name
            if args.list_folders_add_date:
                folder__add_date = return_regex_match(PATTERN_HTML__ADD_DATE, html_folder, "add_date")
            if args.list_folders_last_modified:
                folder__last_modified = return_regex_match(PATTERN_HTML__LAST_MODIFIED, html_folder, "last_modified")
            if args.list_folders_personal_toolbar_folder:
                folder__personal_toolbar_folder = return_regex_match(PATTERN_HTML_FOLDER__PERSONAL_TOOLBAR_FOLDER, html_folder, "folder__personal_toolbar_folder")
        elif html_link:
            name = link__name
            if not args.no_list_links_href:
                link__href = return_regex_match(PATTERN_HTML_LINK__HREF, html_link, "link__href")
            if args.list_links_add_date:
                link__add_date = return_regex_match(PATTERN_HTML__ADD_DATE, html_link, "add_date")
            if args.list_links_last_modified:
                link__last_modified = return_regex_match(PATTERN_HTML__LAST_MODIFIED, html_link, "last_modified")
            if args.list_links_icon_uri:
                link__icon_uri = return_regex_match(PATTERN_HTML_LINK__ICON_URI, html_link, "link__icon_uri")
            if args.list_links_icon:
                link__icon = return_regex_match(PATTERN_HTML_LINK__ICON, html_link, "link__icon")
            if args.list_links_shortcuturl:
                link__shortcuturl = return_regex_match(PATTERN_HTML_LINK__SHORTCUTURL, html_link, "link__shortcuturl")
            if args.list_links_tags:
                link__tags = return_regex_match(PATTERN_HTML_LINK__TAGS, html_link, "link__tags")

        if args.folders_path:
            list_path = list_path[:depth]
            if html_folder:
                list_path.append(name.replace("\\", "\\\\").replace("/", "\\/") + "/")
                path = "".join(list_path[:-1])[:-1] # Removes the folder from the PATH because it displays it as a new folder  # Removes the trailing [+ "/"] from above
            else:
                path = "".join(list_path)[:-1] # Removes the trailing [+ "/"] from above

        if args.depth is not False:
            if not depth == args.depth:
                if not (args.folders_all_case_sensitive or args.folders_all_case_insensitive):
                    continue

        if (args.folders_case_sensitive or args.folders_case_insensitive):
            if not html_folder:
                continue
            if (
                (args.folders_case_sensitive and (name != args.folders_case_sensitive)) or
                (args.folders_case_insensitive and (name.lower() != args.folders_case_insensitive.lower()))
            ):
                continue
        elif (args.folders_all_case_sensitive or args.folders_all_case_insensitive):
            if depth_scan is False:
                if not html_folder:
                    continue
                if args.depth is not False:
                    if not depth == args.depth:
                        continue
                if (
                    (args.folders_all_case_sensitive and (name == args.folders_all_case_sensitive)) or
                    (args.folders_all_case_insensitive and (name.lower() == args.folders_all_case_insensitive.lower()))
                ):
                    depth_scan = depth
                else:
                    continue
            elif depth <= depth_scan:
                depth_scan = False
                continue

        if (html_hr and not args.list_hr):
            continue
        elif (html_folder and not args.list_folders):
            continue
        elif (html_link and not args.list_links):
            continue

        if args.export_personal_toolbar_folder:
            if html_folder:
                if not folder__personal_toolbar_folder:
                    continue
            else:
                continue

        results += 1

        items = []

        if html_hr:
            items.append("HR")
        elif html_folder:
            if args.folders_path:
                items.append("PATH")
            else:
                items.append("FOLDER")
        elif html_link:
            items.append("LINK")
        else:
            assert False, "All possible items exhausted"

        items.append(depth)

        if args.list_results:
            items.append(results)
        if args.list_index:
            items.append(index)
        if args.folders_path:
            items.append(path)
        if html_link:
            if not args.no_list_links_href:
                items.append(link__href)
        items.append(name)

        if html_folder:
            if args.list_folders_add_date:
                items.append(folder__add_date)
            if args.list_folders_last_modified:
                items.append(folder__last_modified)
        elif html_link:
            if args.list_links_add_date:
                items.append(link__add_date)
            if args.list_links_last_modified:
                items.append(link__last_modified)
            if args.list_links_icon_uri:
                items.append(link__icon_uri)
            if args.list_links_icon:
                items.append(link__icon)
            if args.list_links_shortcuturl:
                items.append(link__shortcuturl)
            if args.list_links_tags:
                items.append(link__tags)

        if args.json:
            result_list.append(items)
            continue

        quoted = list(map(quote, items))

        if args.extended_parsing:
            print(args.spacing_style.join(quoted))
        else:
            prefix = "-" * depth if html_folder else " " * depth
            print(f"{prefix}- {args.spacing_style.join(quoted[2:])}")


if args.json:
    import json

    json.dump(result_list, sys.stdout)