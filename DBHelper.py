import MySQLdb as mysql
class DBHelper:
	postObject = "";
	table = "dbc_posts_by_bot"
	dbObject = ""
	def __init__(self, postItem):
		self.postObject = postItem

	def connectToDb(self):
		db_host = "localhost"
		db_user = "root"
		db_pass = ""
		db_database = "searchit"
		dbConn = mysql.connect(db_host, db_user, 
			db_pass, db_database)
		self.dbObject = dbConn
		return dbConn

	def getPostObject(self):
		return self.postObject

	def save(self):
		cursor = self.connectToDb().cursor();
		
		#sql = "INSERT INTO dbc_posts_by_bot(title, description, category, address, phone, website) VALUES('%s', '%s', '%s', '%s', '%s', '%s')" % ('elusoni', 'describe what', 'cat', 'add', '0929033', 'www.yea.com')
		sql = "INSERT INTO dbc_posts_by_bot(unique_id, title, description, category_text, address, phone_no, website) VALUES(%s, %s, %s, %s, %s, %s, %s)"
		#print ("INSERT INTO dbc_posts_by_bot(title, description, category, address, phone, website) VALUES('%s', '%s', '%s', '%s', '%s', '%s')" % (self.getPostObject().title, self.getPostObject().description, self.getPostObject().category, self.getPostObject().address, self.getPostObject().phone, self.getPostObject().website))
		try:
			cursor.execute(sql, ((self.getPostObject().unique_id, self.getPostObject().title, self.getPostObject().description, self.getPostObject().category, self.getPostObject().address, self.getPostObject().phone, self.getPostObject().website)))
			self.dbObject.commit()
		except:
			self.dbObject.rollback()
		
	def postExists(self, post_title):
		cursor = self.connectToDb().cursor()

		sql = "SELECT count (1) FROM dbc_posts_by_bot WHERE title = %s"
		try:
			if (cursor.execute(sql, (post_title))):
				return True
			
		except Exception as e:
			self.dbObject.rollback()




		


		