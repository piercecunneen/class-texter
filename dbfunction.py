import sqlite3 as lite

# Adds a form submission to the database

DB_PATH = "/Users/piercecunneen/Documents/class-texter/text_alerts.sqlite"

def add_row(form, subject):
	""" Get data from form
	

	"""	
	crn = form['crn']
	number = form['phone_number']
	verified = 0
	
	# Connect to db
	data = [crn, number, verified, subject]
	conn = lite.connect(DB_PATH)
	
	# Add row to db
	with conn:
		c = conn.cursor()
		c.executemany('INSERT INTO textAlerts VALUES(?,?,?,?)',(data,))

	return True

# Update a phone number after an 'accept' reply
def verify_number(number):
	conn = lite.connect(DB_PATH)
	with conn:
		c = conn.cursor()
		c.execute("UPDATE textAlerts SET verified = 1 WHERE number = '%s'" % "{}".format(number))

# Remove a number completely from the db
def remove_number(number):
	conn = lite.connect(DB_PATH)
	with conn:
		c = conn.cursor()
		c.execute("DELETE FROM textAlerts WHERE number = '%s'" % "{}".format(number))

if __name__ == "__main__":
	verify_number("456")
	# remove_number("456")