# Script         : Wordpress to Markdown
# Author         : Jonathan Beckett (jonbeckett@outlook.com)
# Compatibility  : Python 3.x
# Pre-Requisites : Markdownify and Unidecode
#
# To install the pre-requisites, run the following commands from the command prompt:
# > pip install markdownify
# > pip install unidecode

import sys
import os
import time
import datetime
import re
import json

# if the tool is run with no arguments, display a title
if (len(sys.argv)==1):
	print("\nghost2md.py - Ghost Export to Markdown Conversion Tool, by Jonathan Beckett\n")

# check we have parameters - inform the user if not
if len(sys.argv)<3:
	print("Tool expects two arguments.")
	print("Format : python ghost2md.py <source_file> <output_path>")
	print("e.g. python ghost2md.py c:\\temp\\export.json c:\\temp\\output")
	sys.exit(0)
	
# get the parameters from the command line
source_file = sys.argv[1]
output_path = sys.argv[2]


if not os.path.isfile(source_file):
	print("The input file (" + source_file +") does not exist")
	sys.exit(0)
	
if not os.path.isdir(output_path):
	print("The output directory (" + output_path +") does not exist")
	sys.exit(0)


# utility function to strip invalid characters from filenames (needed because we use post titles in filenames)
def get_valid_filename(fn):
	fn = str(fn).strip()
	return re.sub(r'(?u)[^-\w\ ]', '', fn)


# read the JSON file
with open(source_file, encoding='latin-1') as json_file:

	json_data = json.load(json_file)
	
	print("Loaded JSON Data")
	print("Number of Posts : " + str(len(json_data["db"][0]["data"]["posts"])))
	
	for post in json_data["db"][0]["data"]["posts"]:
	
		post_title = post["title"]
		post_slug = post["slug"]
		post_content = post["plaintext"]
		post_date = post["published_at"]
		
		# replace extended characters, tags, etc
		if (post_content != None):
		
			post_content = post_content.replace("\n\n","$$")
			post_content = post_content.replace("\n"," ")
			post_content = post_content.replace("$$","\n\n")
			
			# get the post date
			post_year = post_date[0:4]
			post_month = post_date[5:7]
			post_day = post_date[8:10]
			post_day_digit = post_day[-1:]
			post_date = datetime.datetime.strptime(post_year + "-" + post_month + "-" + post_day, '%Y-%m-%d')

			# work out the suffix for the date
			post_day_suffixes = {"1":"st" , "2":"nd" , "3":"rd"}
			post_day_suffix = post_day_suffixes.get(post_day_digit,"th")
			
			# make a nicely formatted date (e.g. Monday 8th July 2019)
			post_date_formatted = post_date.strftime("%A ") + post_day.lstrip("0") + post_day_suffix + post_date.strftime(" %B %Y")
			
			# create a filename for the post
			post_filename = post_year + "-" + post_month + "-" + post_day + " " + post_title
			
			# create a year folder
			post_parent_path = os.path.join(output_path,post_year)
			if not os.path.exists(post_parent_path):
				os.makedirs(post_parent_path)
				print("Creating Parent Path for " + post_year)
			
			# create a month folder within the year folder
			post_child_path = os.path.join(output_path,post_year,post_year + "-" + post_month)
			if not os.path.exists(post_child_path):
				os.makedirs(post_child_path)
				print("Creating Child Path for " + post_year + "-" + post_month)
			
			# construct a valid filename
			output_filename = os.path.join(post_child_path,get_valid_filename(post_filename) + ".md")
			
			# write the markdown into a file
			post_file = open(output_filename, "w", encoding='latin-1')
			post_file.write("# " + post_title + "\n\n")
			post_file.write("## " + post_date_formatted + "\n\n")
			post_file.write(post_content)
			post_file.close()
			
			# output the filename (to show progress)
			print(output_filename)