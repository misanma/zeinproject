import psycopg2

class DbInterface:
	"""Interface of local database"""
	def __init__(self,\
	 			name,\
				table_name):
		#initialize connection and cursor
		self.table_name = table_name
		self.conn = psycopg2.connect("dbname="+name)
		self.cur = self.conn.cursor()


	def insert(self, result):
		#Insert a row into database
		self.cur.execute("INSERT INTO " \
					+self.table_name \
					+" (prediction, solubility, n_sub, charge, numK, numR, numH, numD, numE, seq)"\
					+" VALUES"\
					+' ('+ str(result)[1:-1] + ');')
		self.conn.commit()

	def close_connection(self):
		#close database connection
		self.cur.close()
		self.conn.close()

	def print_all(self):
		#print all
		self.cur.execute("select * from " + self.table_name)
		recs = self.cur.fetchall()
		print(recs)
