"""Model for RoomEase site."""

import sqlite3

class Roommate(object):
	"""
	"""

	def __init__(self,
				first_name,
				last_name,
				age)

		self.first_name = first_name
		self.last_name = last_name
		self.age = age

	def __repr__(self):
        """Show information about roommate in console."""

        return "<Roommate: %s, %s, %s>" % (
            self.first_name, self.last_name, self.age

    @classmethod
    def get_by_name (cls, first_name):
    	"""Query for a specific roommate in the database."""

    	cursor = db_connect()
    	QUERY = """
    		SELECT first_name, last_name, age
    		FROM Roommates
    		WHERE first_name = ?
    		"""

    		cursor.execute(QUERY, (first_name,))
    		row = cursor.fetchone()

    		if not row:
    			return "No roommate by that name."

    		roommate = Roommate(*row)

    		return roommate