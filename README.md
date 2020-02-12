# ghost2md

## Ghost JSON Export to Markdown Text File Converter for Python 3.x

This python 3.x script will convert a Ghost export file into a collection of markdown formatted text files.

Usage:

`python ghost2md.py <export file> <output folder>`

e.g.

`python ghost2md.py c:\temp\blog_export.json c:\temp\output`


### Output

The script creates a folder structure within the output folder of years, and months (in yyyy-mm format). Each markdown file within those folders will be named by it's published post date (in yyyy-mm-dd format) along with the post title - e.g. `2019-07-08 Hello World.md`.

Within each markdown file, the original post title is on the first line, the date in long format (e.g. Monday 8th July 2019) is on the third line, and content begins on the 5th line.


### Notes

I have not experimented with replacing extended characters (curly quotes, etc). Perhaps a project for the future!
