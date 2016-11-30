import json

import numpy as np

from assignment5.Node import Node


def write():
	with open("data.txt", 'x') as f:
		data = {'total_web_pages': Node.total_web_pages,
		'total_num_links': Node.total_num_links,
		'links_in_page': Node.links_in_page,
		'int_link': Node.int_link,
		'ext_link': Node.ext_link}
		obj = json.dumps(data)
		f.write(obj)


def load():
	with open ("data1.txt", 'r') as f:
		data = f.read()
		obj = json.loads(data)
		Node.total_web_pages = obj['total_web_pages']
		Node.total_num_links = obj['total_num_links']
		Node.links_in_page = obj['links_in_page']
		Node.int_link = obj['int_link']
		Node.ext_link = obj['ext_link']
		print("Total web pages: {}".format(Node.total_web_pages))
		print("Total link number: {}".format(Node.total_num_links))
		print("Average links per page: {}".format(np.mean(Node.links_in_page)))
		print("Median links per page: {}".format(np.median(Node.links_in_page)))

if __name__ == "__main__":
	from assignment5 import crawl

    load()
	crawl.make_hist(Node.links_in_page)
	crawl.make_scat(Node.int_link, Node.ext_link)