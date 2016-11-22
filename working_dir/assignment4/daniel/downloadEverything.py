from sys import argv
from working_dir.assignment4.daniel.httpClient import make_request
from urllib.parse import urlparse

# html_file = argv[1]
# url = argv[2]
html_file = "index.php"
url = "http://west.uni-koblenz.de/en/studying/courses/ws1617/introduction-to-web-science"
url = urlparse(url)

urls = []
with open(html_file, mode='r') as html:
    for line in html:
        while line.find('<img') != -1:
            img_start = line.find('<img')
            whole_tag = line[img_start + 4:]
            img_tag = whole_tag[:whole_tag.find('/>')]
            src = img_tag[img_tag.find('src="') + 5:]
            path = src[:src.find('"')]
            urls.append(path)
            line = line[img_start+4:]
print(urls)
for img_url in urls:
    img_url = urlparse(img_url)
    file_name = img_url.path.split('/')[-1]
    make_request("http://{}{}".format(url.netloc,img_url.path), filename=file_name)
