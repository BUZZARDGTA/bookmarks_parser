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
if not str(args.depth) == "False":
    args.depth = int(args.depth)
SPACING_STYLE = args.spacing_style
if not SPACING_STYLE in [' ', ",", "-", "_"]:
    SPACING_STYLE = ' '
QUOTING_STYLE = args.quoting_style
if not QUOTING_STYLE in ['"', "'", ""]:
    QUOTING_STYLE = '"'


sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")

depth = previous_depth = results = index = 0
link = name = ""
list_path = []
path = []
depth_scan = html_open_dl_p = html_closed_dl_p = previous_line_open_dl_p = False
regexes = r'(?P<html_hr><HR>)', r'(?P<html_link><DT><A HREF="https?:[^"]+"[^>]*>[^<]*</A>)', r'(?P<html_folder><DT><H3 [^>]*>[^<]*</H3>)', r'(?P<html_open_dl_p><DL><p>)', r'(?P<html_closed_dl_p></DL><p>)'
combinedRegex = re.compile('|'.join('(?:{0})'.format(x) for x in regexes), re.IGNORECASE)


def stdout(list_stdout):
    if args.extended_parsing:
        print(f"{SPACING_STYLE}".join(list_stdout).replace('"', f'{QUOTING_STYLE}'))
    else:
        print(f"{list_stdout[0]} " + f"{SPACING_STYLE}".join(list_stdout[1:]).replace('"', f'{QUOTING_STYLE}'))


for line in open(args.bookmarks_file, "r", encoding="utf-8"):
    if html_open_dl_p:
        previous_line_open_dl_p = html_open_dl_p
    else:
        previous_line_open_dl_p = False
    for html_hr, html_link, html_folder, html_open_dl_p, html_closed_dl_p in combinedRegex.findall(line):
        if html_link:
            if html_folder:
                continue

        if html_closed_dl_p:
            if previous_line_open_dl_p:
                list_path = list_path[:-1]
            continue
        elif html_open_dl_p:
            continue

        if args.list_index:
            index += 1

        if html_link:
            regex = re.compile(r'<DT><A HREF="(?P<link>https?:[^"]+)"[^>]*>(?P<name>[^<]*)</A>', re.IGNORECASE)
            match = re.search(regex, html_link)
            link = match["link"]
            name = match["name"]
        elif html_folder:
            regex = re.compile(r'<DT><H3 [^>]*>(?P<name>[^<]*)</H3>', re.IGNORECASE)
            match = re.search(regex, html_folder)
            name = match["name"]

        previous_depth = depth
        depth = ((len(line) - len(line.lstrip(" "))) // 4) - 1

        if (html_link or html_folder or html_hr):
            if args.folders_path:
                if depth < previous_depth:
                    list_path = list_path[:-(previous_depth - depth)]
                if html_folder:
                    list_path.append(name.replace("\\", "\\\\").replace("/", "\\/") + "/")
                    if args.extended_parsing:
                        path = "".join(list_path[:-1])[:-1]
                else:
                    path = "".join(list_path)[:-1]

        if not str(args.depth) == "False":
            if not depth == args.depth:
                continue

        if args.folders_case_sensitive or args.folders_case_insensitive:
            if not html_folder:
                continue
            if (args.folders_case_sensitive and name != args.folders_case_sensitive) or (args.folders_case_insensitive and name.lower() != args.folders_case_insensitive.lower()):
                continue

        if args.folders_all_case_sensitive or args.folders_all_case_insensitive:
            if str(depth_scan) == "False":
                if html_folder and ((args.folders_all_case_insensitive and name.lower() == args.folders_all_case_insensitive.lower()) or
                                    (not args.folders_all_case_insensitive and name == args.folders_all_case_sensitive)):
                    depth_scan = depth
                else:
                    continue
            elif depth <= depth_scan:
                depth_scan = False
                continue

        if html_hr:
            if args.list_hr:
                list_stdout = []
                if args.extended_parsing:
                    list_stdout.append('"HR"')
                else:
                    prefix = " " * (depth)
                    list_stdout.append(f"{prefix} -")
                if args.extended_parsing:
                    list_stdout.append(f'"{depth}"')
                if args.list_results:
                    results += 1
                    list_stdout.append(f'"{results}"')
                if args.list_index:
                    list_stdout.append(f'"{index}"')
                if args.folders_path:
                    list_stdout.append(f'"{path}"')
                list_stdout.append(f"--------------------")
                stdout(list_stdout)
                continue

        if html_link:
            if link:
                if args.list_links:
                    list_stdout = []
                    if args.extended_parsing:
                        list_stdout.append('"LINK"')
                    else:
                        prefix = " " * (depth)
                        list_stdout.append(f"{prefix} -")
                    if args.extended_parsing:
                        list_stdout.append(f'"{depth}"')
                    if args.list_results:
                        results += 1
                        list_stdout.append(f'"{results}"')
                    if args.list_index:
                        list_stdout.append(f'"{index}"')
                    if args.folders_path:
                        list_stdout.append(f'"{path}"')
                    list_stdout.extend((f'"{link}"', f'"{name}"'))
                    stdout(list_stdout)
                    continue

        elif html_folder:
            if args.list_folders:
                list_stdout = []
                if args.extended_parsing:
                    if args.folders_path:
                        list_stdout.append('"PATH"')
                    else:
                        list_stdout.append('"FOLDER"')
                else:
                    prefix = "-" * (depth + 1)
                    list_stdout.append(f"{prefix}")
                if args.extended_parsing:
                    list_stdout.append(f'"{depth}"')
                if args.list_results:
                    results += 1
                    list_stdout.append(f'"{results}"')
                if args.list_index:
                    list_stdout.append(f'"{index}"')
                if args.folders_path:
                    list_stdout.extend((f'"{path}"', f'"{name}"'))
                else:
                    list_stdout.append(f'"{name}"')
                stdout(list_stdout)
                continue
