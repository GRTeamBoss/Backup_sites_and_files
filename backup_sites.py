from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import re

intro = "Backup\n1.filename\n2.url\n1.1.site\n1.2.tags\n2.1.site\n2.2.tags\nAttention: only '1.x' or '2.x'."
print(intro)
method_parse = str(input(": "))

source = str(input("source: "))

class Backup:

	def __init__(self):
		self.var = method_parse
		self.tags_intro = "Choose\n1.all <tag> in html document\n2.one <tag> in html document"
		self.tags_search = ''
		self.tags = ''
		self.count = ''
		self.page = ''
		self.file_read = ''
		self.tags_search_start = ''
		self.tags_search_end = ''
		self.tags_search_start_full = ''
		self.data = ''

		if self.var == '1.1': #-filename -site
			self.get_file()
			self.backup_file_site()
		elif self.var == '1.2': #-filename -tags
			self.get_file()
			print(self.tags_intro)
			self.tags_method = str(input(": "))
			self.backup_file_site_tags()
		elif self.var == '2.1': #-url -site
			self.get_url()
			self.backup_site()
		elif self.var == '2.2': #-url -tags
			self.get_url()
			print(self.tags_intro)
			self.tags_method = str(input(": "))
			self.backup_site_tags()
		else:
			print('Error!')

	def get_url(self):
		self.page = urlopen('%s' % source)
		self.data = self.page.read()

	def get_file(self):
		file = open("%s" % source, "r")
		self.file_read = file.read()
		file.close()

	def backup_site(self):
		backup_post = open("backup_site.txt", "a")
		backup_post.write(str(time.ctime()) + ":\n" + str(self.data) + "\n")
		backup_post.close()
		

	def backup_site_tags(self):
		soup = BeautifulSoup(self.data)
		if self.tags_method == "1":
			self.tags_search = str(input("Please input without '<' and '>' symbols\n: "))
			self.tags = soup.findAll("%s" % self.tags_search)
			backup_post = open("backup_site_" + self.tags_search + "s.txt", "a")
			backup_post.write(str(time.ctime()) + ": \n" + self.tags + "\n")
			backup_post.close()
		elif self.tags_method == "2":
			self.tags_search = str(input("Please input without '<' and '>' symbols\n: "))
			self.tags_get = soup.findAll("%s" % self.tags_search)
			self.count = str(input("Please input which tag parse, example: '0' - it's first tag.\n: "))
			backup_post = open("backup_site_" + self.tags_search + ".txt", "a")
			backup_post.write(str(time.ctime()) + ": \n" + str(self.tags_get[int(self.count)]) + "\n")
			backup_post.close()
		else:
			print("Error!")

	def backup_file_site(self):
		backup_post = open("backup_file_site.txt", "a")
		backup_post.write(str(time.ctime()) + ":\n" + self.file_read + "\n")
		backup_post.close()

	def backup_file_site_tags(self):
		if self.tags_method == "1":
			self.tags_search = str(input("Please input without '<' and '>' symbols\n: "))
			self.tags_search_start = "<" + self.tags_search
			self.tags_search_end = "</" + self.tags_search + ">"
			self.tags_search_start_full = "<" + self.tags_search + ">"
			text_list = self.file_read.split();
			n = 0
			m = 0
			value_start = ''
			value_end = ''
			for i in range(0, len(text_list)):
				if self.tags_search_start == text_list[i]:
					n += 1
					value_start += str(i) + ' '
				else:
					pass
			if n == 0:
				for i in range(0, len(text_list)):
					if self.tags_search_start_full == text_list[i]:
						m += 1
						value_start += str(i) + ' '
					else:
						pass				
			else:
				pass
			print(value_start)
			m = 0
			for i in range(0, len(text_list)):
				if self.tags_search_end == text_list[i]:
					m += 1
					value_end += str(i) + ' '
				else:
					pass
			if m == 0:
				print("end tag not found!")
			else:
				pass

			value_split_start = value_start.split()
			value_split_end = value_end.split()
			value_content = []
			tag_end = re.compile('[a-zA-Z(-=\!\s\~\@\#\$\)\(\%\^\&\*\_\+\'\")]+[>]')

			if m == 0:
				for i in range(0, len(value_split_start)):
					value_content.append([])
					n = int(value_split_start[i]) + 1
					for b in range(n, n + 10):
						if text_list[b] != ''.join(tag_end.findall(text_list[b])):
							value_content[i].append(text_list[b])
						elif text_list[b] == ''.join(tag_end.findall(text_list[b])):
							value_content[i].append(text_list[b])
							print(tag_end.findall(text_list[b]))
							break
						else:
							pass
			else:
				for i in range(0, len(value_split_start)):
					value_content.append([])
					n = int(value_split_start[i]) + 1
					while n < int(value_split_end[i]):
						value_content[i].append(text_list[n])
						n += 1

			self.tags = []

			if m == 0:
				for i in range(0, len(value_split_start)):
					self.tags.append(str(''.join(text_list[int(value_split_start[i])])) + ' ' + str(' '.join(value_content[i])))
			else:	
				for i in range(0, len(value_split_start)):
					self.tags.append(str(''.join(text_list[int(value_split_start[i])])) + ' ' + str(' '.join(value_content[i])) + ' ' + str(''.join(text_list[int(value_split_end[i])])))

			backup_post = open("backup_file_site_" + self.tags_search + "s.txt", "a")
			backup_post.write(str(time.ctime()) + ": \n" + str(''.join(self.tags)) + "\n")
			backup_post.close()
		elif self.tags_method == "2":
			self.tags_search = str(input("Please input without '<' and '>' symbols\n: "))
			self.count = str(input("Please input which tag parse, example: '0' - it's first tag.\n: "))
			self.tags_search_start = "<" + self.tags_search
			self.tags_search_start_full = "<" + self.tags_search + ">"
			self.tags_search_end = "</" + self.tags_search + ">" 
			text_list = self.file_read.split();
			n = 0
			m = 0
			value_start = ''
			value_end = ''
			for i in range(0, len(text_list)):
				if self.tags_search_start == text_list[i]:
					n += 1
					value_start += str(i) + ' '
				else:
					pass
			if n == 0:
				for i in range(0, len(text_list)):
					if self.tags_search_start_full == text_list[i]:
						m += 1
						value_start += str(i) + ' '
					else:
						pass				
			else:
				pass
			print(value_start)
			n = 0
			for i in range(0, len(text_list)):
				if self.tags_search_end == text_list[i]:
					n += 1
					value_end += str(i) + ' '
				else:
					pass
			if n == 0:
				print("end tags not found!")
			else:
				pass
			value_split_start = value_start.split()
			value_split_end = value_end.split()
			value_content = []
			tag_end = re.compile("""[a-zA-Z(-=\'\"\!\s\~\@\#\(\)\$\%\^\&\*\_\+)]+[>]""")

			for i in range(0, len(value_split_start)):
				value_content.append([])
				n = int(value_split_start[i]) + 1
				if int(self.count) == i:
					if len(value_end) == 0:
						for b in range(n, n + 10):
							if text_list[b] != ''.join(tag_end.findall(text_list[b])):
								value_content[i].append(text_list[b])
							elif text_list[b] == ''.join(tag_end.findall(text_list[b])):
								value_content[i].append(text_list[b])
								print(tag_end.findall(text_list[b]))
								break
							else:
								pass
					else:
						while n < int(value_split_end[i]):
							value_content[i].append(text_list[n])
							n += 1
				else:
					pass
			if len(value_end) == 0:
				self.tags_get = str(''.join(text_list[int(value_split_start[int(self.count)])])) + ' ' + str(' '.join(value_content[int(self.count)]))
			else:
				self.tags_get = str(''.join(text_list[int(value_split_start[int(self.count)])])) + ' ' + str(' '.join(value_content[int(self.count)])) + ' ' + str(''.join(text_list[int(value_split_end[int(self.count)])]))

			backup_post = open("backup_file_site_" + self.tags_search + ".txt", "a")
			backup_post.write(str(time.ctime()) + ": \n" + str(self.tags_get) + "\n")
			backup_post.close()
		else:
			print("Error!")

Backup()