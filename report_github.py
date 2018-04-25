#!/usr/bin/env python3

# This program collect all issues from the repositories passed as argument and print a report about them
# Usage:
# ./report.py owner1/repo1 [ owner2/repo2 , ... ]

import sys
import requests
import json

# Function used to order the issues list by creation date
def getKey(item):
	return item["created_at"]

# Return a new dictionary with the summarized version of the issue containing only the requested fields
def summarize_issue(issue):
	summarized_issue = {}
	summarized_issue["created_at"]=issue["created_at"]
	summarized_issue["state"]=issue["state"]
	summarized_issue["id"]=issue["number"]
	summarized_issue["title"]=issue["title"]
	summarized_issue["repository"]=repository		# The format of this field is: owner/repository
	return summarized_issue

def main():
	result = {}
	issues = []
	days = {}

	# Correct usage comprobation
	if len(sys.argv) < 2:
		print("Error: At least 1 argument needed\nUsage: ./report.py owner1/repo1 [ owner2/repo2 , ... ]", file=sys.stderr)		# Error to stderr
		sys.exit(1)

	for repository in sys.argv[1:] : 
		# Ask Github for all issues related to repository, sorted by creation date with olders results first
		response = requests.get("https://api.github.com/repos/"+repository+"/issues?state=all&sort=created&direction=asc")
		if response.status_code == 200:		# Repository found
			data = response.json()
			for issue in data:
				# Create a new dictionary to insert in the list with the required data.
				dictionary_issue = summarize_issue(issue)
				day=issue["created_at"].split('T')[0]
				days[day] = []		# Initialization of day counters
			
			# Tracking the days where repositories has issues
			for issue in data:
				day=issue["created_at"].split('T')[0]
				days[day].append(repository)

		else:	# if Status code != 200, abort
			print("Error with: "+repository+" Error code: "+str(response.status_code), file=sys.stderr)		# Error to stderr
			sys.exit(1)

	# Insert the sorted list of issues into result dictionary. Github return sorted data, but we need to sort again because we have data from various repositories
	result["issues"]=sorted(issues, key=getKey)

	# Find the day with the maximum number of issues
	top_day = {}
	max_num = 0
	max_day = ""
	for day in days:
		if len(days[day]) >= max_num : 
			max_num=len(days[day])
			max_day=day

	top_day["day"]=max_day;
	
	# Find the repos with issues created on the top day
	occurrences = {}
	for repo in set(days[max_day]):		# Conversion to set to remove duplicates and iterate only among uniq values
		occurrences[repo]=0				# Initializing the counter
		for entry in days[max_day]:
			if entry == repo:
				occurrences[repo]+=1

	# Insert the top day info into result dictionary
	top_day["occurrences"]=occurrences
	result["top_day"]=top_day
	
	# Print final result
	result_json = json.dumps(result, sort_keys=True, indent=4)	# sort_keys makes appear the 'top_day' info always at the bottom
	print(result_json)
	sys.exit(0)

if __name__ == '__main__': 
 	main() 