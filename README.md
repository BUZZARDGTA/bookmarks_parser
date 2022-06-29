```
usage: bookmarks_parser.py [-h] [-f] [-l] [-r] [-i] [-e] [--folders-name | --folders-path]
                           [--folders <folder> | --folders-all <folder>] [--depth <depth>]
                           [--spacing-style <spacing style>] [--quoting-style <quoting style>]
                           <bookmarks file>

Parse a HTML bookmark file.

positional arguments:
  <bookmarks file>      the path of the bookmark file

options:
  -h, --help            show this help message and exit
  -f, --list-folders    list the folders (default)
  -l, --list-links      list the links (default)
  -r, --list-results    list the results numbers
  -i, --list-index      list the index numbers
  -e, --extended-parsing
                        alternative display easily manipulable for developers
  --folders-name        display the folders name (default)
  --folders-path        display the folders path
  --folders <folder>    list all folders matching <folder>
  --folders-all <folder>
                        list all content from folders matching <folder>
  --depth <depth>       list the choosen depth only
  --spacing-style <spacing style>
                        Change the spacing style. Valid inputs are: [ ]/[,]/[-]/[_] (default: [ ])
  --quoting-style <quoting style>
                        Change the quoting style. Valid inputs are: ["]/[']. (default: ["])
```
