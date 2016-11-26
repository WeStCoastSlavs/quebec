import wget
from Node import Node
from urllib.parse import urlparse, urljoin
from collections import deque


def download(url):
    parsed_url = urlparse(url)
    # parsed_url = url
    if parsed_url.path.find('.') == -1:
        name = 'test'
    else:
        name = parsed_url.path.split('/')[-1]
    try:
        # final_link = parsed_url.scheme+ "://" + parsed_url.netloc + parsed_url.path
        filename = wget.download(url, "junk/"+name)
        print(filename)
        return filename
    except Exception:
        print("*****LINK FAILED*****\n"+url)
        # raise Exception("Link failed :" + url)
        return False


def get_links(filename):
    urls = []
    with open(filename, mode='r', encoding="utf-8") as file:
        # with open(filename+'.txt', mode='w') as helper:
            for line in file:
                while line.find('<a') != -1:
                    a_start = line.find('<a')
                    whole_tag = line[a_start + 2:]
                    a_tag = whole_tag[:whole_tag.find('>')]
                    if a_tag.find("href")==-1:
                        line = line[a_start+2:]
                        continue
                    href = a_tag[a_tag.find('href="') + 6:]
                    path = href[:href.find('"')]
                    urls.append(path)
                    line = line[a_start+4:]
                    # helper.write(path + '\n')
    return urls


def get_children_from_urls(urls, parent):
    nodes = []
    for ur in urls:
        node = Node()
        node.node_url = ur
        node.parent = parent
        nodes.append(node)
    return nodes


def parse_link(link, start_url):
    i = 0
    for elem in link.split('/'):
        if elem == "..":
            i += 1
    link = link.split('/')[i:]
    base = start_url.split('/')[:-i-1]
    base.extend(link)
    print(base)
    return '/'.join(base)


def remove_file_name(full_url):
    if full_url.find('.') == -1: return full_url
    return '/'.join(full_url.split('/')[:-1])


if __name__ == "__main__":
    host = "141.26.208.82"
    start_url = "http://141.26.208.82/articles/g/e/r/Germany.html"
    file_name = download(start_url)
    init_node = Node()
    init_node.node_url = start_url
    init_node.node_children = get_children_from_urls(get_links(file_name),init_node)

    # init_node.node_children = list(set(init_node.node_children))

    visited = [start_url]
    queue = deque([])
    queue.extend(init_node.node_children)

    while True:
        node = queue.popleft()
        link = node.node_url
        if link.find('http')==0 or link.find('#')==0:
            continue
        link = urljoin(start_url, link)
        if link in visited:
            continue
        else:
            filename = download(link)
            if not filename: continue
            node = Node()
            node.node_url = link
            node.node_children = get_children_from_urls(get_links(filename),node)
            queue.extend(node.node_children)
            visited.append(link)
