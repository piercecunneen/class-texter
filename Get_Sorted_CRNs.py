import requests
from bs4 import BeautifulSoup
from class_search_web_scrapping import  GetOptions, GetClasses
import time

SORTED_CRN_PATH = '/Users/piercecunneen/Documents/NDreviews/class_texter/sorted_CRNs.txt'

# Returns a list that is redonk large. Use Write_Courses_iter to return a generator with smaller pieces
def Write_Courses():
	Options = GetOptions()
	subjects = Options[3].values()
	term = "201620"
	ATTR = '0ANY'
	Division = "UG"
	Campus = "M"
	Credit = "A"
	Courses = GetClasses(term, subjects, Credit, ATTR, Division, Campus)
	return Courses

def Write_Sorted_CRNS():
	# with open('/home/pcunneen/class-texter/sorted_CRNs.txt', "") as f:
	courses = Write_Courses()
	sorted_courses = sorted(courses, key=lambda k: k['CRN'])
	with open(SORTED_CRN_PATH, "w") as f:
		for course in sorted_courses:
			f.write("{} {}\n".format(course['CRN'], course['View_Books'].split('dept-1=')[1].split('&course-1')[0]))

def Get_CRN_List():
	crn_list = []
	with open(SORTED_CRN_PATH, "r") as f:
		line = f.readline().rstrip()
		while line:
			crn_list.append(line)
			line = f.readline().rstrip()
	while crn_list[-1] == "":
		crn_list.pop()
	return crn_list

# Performs a binary search for value in CRN_Numbers
# returns a department if the crn value was found that cooresponds to the crn
# returns false if value not in CRN_Numbers
def is_Valid(value, CRN_Numbers):
	start = 0
	end = len(CRN_Numbers) - 1
	middle = (end) / 2

	while start <= end:
		middle_value = int(CRN_Numbers[middle].split(" ")[0])
		if middle_value > value:
			end = middle - 1
			middle = (start + end) / 2
		elif middle_value < value:
			start = middle + 1
			middle = (start + end) / 2
		else:
			return CRN_Numbers[middle].split(" ")[1]
	return False