```
usage: bookmarks_parser.py [-h] [-folders] [-links] [-hr] [-r] [-i] [-e] [-j] [--folders-name | --folders-path]
                           [--folders-case_sensitive <folder name> | --folders-case_insensitive <folder name> | --folders-all-case_sensitive <folder name> | --folders-all-case_insensitive <folder name>]
                           [--depth <depth>] [--spacing-style <character>] [--quoting-style <character>]
                           <bookmarks file>

Parse a HTML bookmark file.

positional arguments:
  <bookmarks file>      the path of the bookmark file

options:
  -h, --help            show this help message and exit
  -folders, --list-folders
                        list the folders (default)
  -links, --list-links  list the links (default)
  -hr, --list-hr        list the hr elements (default)
  -r, --list-results    list the results numbers
  -i, --list-index      list the index numbers
  -e, --extended-parsing
                        alternative display easily manipulable for developers
  -j, --json            output in JSON format
  --folders-name        display the folders name (default)
  --folders-path        display the folders path
  --folders-case_sensitive <folder name>
                        list all folders matching <folder name> with case sensitive.
  --folders-case_insensitive <folder name>
                        list all folders matching <folder name> with case insensitive.
  --folders-all-case_sensitive <folder name>
                        list all content from folders matching <folder name> with case sensitive.
  --folders-all-case_insensitive <folder name>
                        list all content from folders matching <folder name> with case insensitive.
  --depth <depth>       list the choosen depth only
  --spacing-style <character>
                        Change the spacing style <character>. Valid characters are: [ ]/[,]/[-]/[_] (default: [ ])
  --quoting-style <character>
                        Change the quoting style <character>. Valid characters are: ["]/[']. (default: ["])
```
