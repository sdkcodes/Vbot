import bs4
import requests
import sys
import os
import Post_Class
from DBHelper import DBHelper
from bs4 import BeautifulSoup
import string
import random

class VconBot:
    category_url = ""
    no_of_pages = ""
    category_name = "" 
    categories_links_file_name = ""

    def __init__(self, category_url):
        self.category_url = category_url
        category_data = requests.get(self.category_url)
        soup = bs4.BeautifulSoup(category_data.text, "lxml")
        counts_tag = soup.find(class_="listing-result-count")
        #get the string in the counts_tag, split the string to create the list, and retrieve the first element 
        #in the list, which will then be total number of results
        #convert count string to integer and divide by the number of busineses listed per page (10)
        count_string = counts_tag.string.split()[0]
        count_string = count_string.replace(",", "")
        self.no_of_pages = round(int(count_string)/10)
        cat_name_tag = soup.find(class_="listing-breadcrumbs-list")
        cat_name = cat_name_tag.find_all("li")[1].string
        self.category_name = cat_name
        self.categories_links_file_name = cat_name + ".txt"
        
    def buildCategoryPages(self):
        print ("Building pages url")
        i = 2
        categories_links_file = open(self.categories_links_file_name, "w") #category file object
        categories_links_file.write(self.category_url + "\n")
        while (i <= self.no_of_pages):
            categories_links_file.write(self.category_url + "-page" + str(i) + "\n")
            #print ("written " + self.category_url + "-page" + str(i))
            i += 1
        categories_links_file.close();

    def listLinks(self):
        file = open(self.categories_links_file_name, "r")
        file_contents = file.read()
        print (file_contents.split())
    def generate_random(self,length=10):
    	s = string.ascii_lowercase+string.digits
    	return ''.join(random.sample(s, length))

    def category_file_exists(self):
        if (os.path.exists(self.categories_links_file_name) and os.path.getsize(self.categories_links_file_name) > 0):
            return True
    def get_categories_links_file_name(self):
        return self.categories_links_file_name

    def get_business_info(self, business_url):
        #print ("getting business info");
        business_content = requests.get(business_url)
        soup = BeautifulSoup(business_content.text, "lxml")
        desc_tag = soup.find(class_="js-section-content")
        description = ""
        
        try:
            description = desc_tag.contents[0]
            description = """ {"en": "<div>%s</div>"} """ % description
            
        
        except:
            try:
                if (type(desc_tag.next_element) == bs4.element.Tag and  desc_tag.next_element.name == "p"):
                    description = desc_tag.next_element.string
                    description = """ {"en": "<div>%s</div>"} """ % description
                    
            except:
                description = ""
            # description = description
            

        address_tag = soup.find("i", class_="icon-address")
        try:
            address = address_tag.next_element.next_element.contents[1].string
        except Exception as e:
            address = ""
        
        website_tag = soup.find("a", string="Visit this business website")
        try:
            website = website_tag["href"]
        except:
            website = ""
        try:
            business_name = soup.find("h1", class_="business-name").string
            business_name = """{"en": "%s"} """ % business_name
            print (business_name)
        except Exception as e:
            business_name = ""

        phone_url = soup.find("a", string="View phone number")
        try:
            phone_url = phone_url["href"]
            phone_url = "http://vconnect.com" + phone_url[1:]
            phone_number = self.get_phone_number(phone_url)
        except:
            phone_number = ""
        category_name = self.category_name
        id_length = random.randint(10, 15)
        unique_id = self.generate_random(id_length)

        postObject = Post_Class.Post(unique_id, business_name, category_name, 
            description, website, address, phone_number)
        dbHelper = DBHelper(postObject)
        if (dbHelper.postExists(business_name) != True):
            dbHelper.save()
            #print ("saved")
        else:
            print ("exists")
        

    def get_phone_number(self, url):
        result = requests.get(url)
        soup = bs4.BeautifulSoup(result.text, "lxml")
        phone = soup.find("div", class_="big")
        return phone.string

    def get_category_business_links(self, page_url):    
        category_data = requests.get(page_url)
        cat_soup = BeautifulSoup(category_data.text, "lxml")
        cat_tags = cat_soup.find_all(class_="business-title")
        a_cat_tags_list = []
        for tag in cat_tags:
            a_cat_tags_list.append(tag.a["href"])
        return a_cat_tags_list
    def crawl_businesses_from_categories(self):
        if (not self.category_file_exists()):
            self.buildCategoryPages();

        cat_file = open(self.categories_links_file_name, "r")
        file_contents = cat_file.read()
        file_contents = file_contents.split()
        # print (file_contents)
        for each_url in file_contents:
            print ("Crawling: " + each_url)
            businesses_list = self.get_category_business_links(each_url)
            for business_url in businesses_list:
                self.get_business_info(business_url)
            #file_contents.remove(each_url)
            print ("Removed : " + each_url)
        cat_file.close();
        cat_file = open(self.categories_links_file_name, "w")

        # for line in file_contents:
        #     cat_file.write(line + "\n")
        # cat_file.close()


if __name__ == '__main__':
    print ("Enter category Url: ->")
    cat_url = input("")
    bot = VconBot(cat_url)
    #bot.buildCategoryPages()
    bot.crawl_businesses_from_categories();

