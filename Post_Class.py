class Post:
	
	title = ""
	category = ""
	website = ""
	address = ""
	description = ""
	phone = ""
	unique_id = ""

	"""docstring for Post"""
	def __init__(self, unique_id="", title="", category="", description="", website="", address="", phone=""):
		self.title = title
		self.category = category
		self.description = description
		self.website = website
		self.address = address
		self.phone = phone
		self.unique_id = unique_id


	def toString(self):
		return (self.title, "\n", self.category, 
			"\n", self.description, "\n", self.website,
			"\n", self.address, "\n", self.phone)


