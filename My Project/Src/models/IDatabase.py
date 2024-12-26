import mysql.connector
from mysql.connector.errors import Error

class IDatabase:
	def __init__(self, conn = {}, debug = False):
		self.conn = mysql.connector.connect(
			host = conn["host"],
			user = conn["user"],
			password = conn["password"],
			database = conn["database"],
		)
		self.debug = debug

	def get(self, table, where = [], groupby = "", having = "", orderby = "id", sort = "ASC"):
		parms = ""
		if where:
			parms += "WHERE " + " AND ".join(where)
	
		if groupby:
			parms += " GROUP BY " + groupby
			if having:
				parms += " HAVING " + having

		if orderby:
			parms += " ORDER BY " + orderby

		if sort:
			parms += " " + sort

		cursor = self.conn.cursor()
		command = f"SELECT * FROM {table} {parms}"
		if (self.debug):
			print("IDatabase Execute:", command)

		cursor.execute(command)
		return cursor.fetchall()
		

	def create(self, table, col = []):
		cursor = self.conn.cursor()
		parms = ""
		if (len(col) == 0):
			return False
		else:
			parms += ", ".join(col)
			command = f"CREATE TABLE {table} ({parms})"
			if (self.debug):
				print("IDatabase Execute:", command)
			return cursor.execute(command)

	def insert(self, table, ins = []):
		parms = ""
		if ins:
			parms += ", ".join(ins)

			try:
				cursor = self.conn.cursor()
				command = f"INSERT INTO {table} SET {parms}"
				if (self.debug):
					print("IDatabase Execute:", command)
				cursor.execute(command)
				self.conn.commit()
				
			except mysql.connector.Error as e:
				raise e
		else:
			return False
			

	def update(self, table, upd = [], where = []):
		parms = ""
		if upd:
			parms += ", ".join(upd)
			
			if where:
				parms += " WHERE " + " AND ".join(where)

			cursor = self.conn.cursor()
			command = f"UPDATE {table} SET {parms}"
			if (self.debug):
				print("IDatabase Execute:", command)
			cursor.execute(command)
			self.conn.commit()
		else:
			return False
			

	def delete(self, table, where = []):
		command = f"DELETE FROM {table}"
			
		if where:
			command += " WHERE " + " AND ".join(where)
			
		cursor = self.conn.cursor()
		if (self.debug):
			print("IDatabase Execute:", command)
		cursor.execute(command)
		self.conn.commit()

