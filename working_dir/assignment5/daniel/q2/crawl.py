import wget
from Node import Node
from urllib.parse import urlparse, urljoin
from collections import deque
import traceback
import numpy as np
import matplotlib.pyplot as plt
import time


def download(url):
    parsed_url = urlparse(url)
    # parsed_url = url
    if parsed_url.path.find('.') == -1:
        name = 'test.html'
    else:
        name = parsed_url.path.split('/')[-1]
    try:
        # final_link = parsed_url.scheme+ "://" + parsed_url.netloc + parsed_url.path
        filename = wget.download(url, "junk/"+name)
        # print(filename)
        return filename
    except Exception:
        # print("*****LINK FAILED*****\n"+url)
        # traceback.print_exc()
        # raise Exception("Link failed :" + url)
        return False


def get_links(filename):
    urls = []
    internal = 0
    external = 0
    try:
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
                        if path.find("http") == 0:
                            external += 1
                        else:
                            internal += 1
                        urls.append(path)
                        line = line[a_start+4:]
                        # helper.write(path + '\n')
        Node.int_link.append(internal)
        Node.ext_link.append(external)
        Node.total_num_links += len(urls)
        Node.links_in_page.append(len(urls))
        return urls
    except UnicodeDecodeError:
        traceback.print_exc()
        print("Failed decoding file: " + filename)
        return urls


def get_children_from_urls(urls, parent):
    nodes = []
    for ur in urls:
        node = Node(parent, ur)
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


def make_hist(x):
    n, bins, patches = plt.hist(x, 5, normed=0, range=(0,150), facecolor='blue', alpha=0.75)
    plt.xlabel('Number of pages')
    plt.ylabel('Number of links')
    plt.title('Distribution of links')
    # plt.axis([40, 160, 0, 0.03])
    plt.grid(True)

    plt.show()


def make_scat(x,y):

    plt.scatter(x,y)
    plt.show()

if __name__ == "__main__":

    start_time = time.time()
    host = "http://141.26.208.82/index.html"
    start_url = "http://141.26.208.82/articles/g/e/r/Germany.html"
    start_url = host
    file_name = download(start_url)
    init_node = Node(None, start_url)
    init_node.node_children = get_children_from_urls(get_links(file_name),init_node)

    # init_node.node_children = list(set(init_node.node_children))

    visited = set([start_url])
    queue = deque([])
    queue.extend(init_node.node_children)

    while queue:
        if Node.total_web_pages == 10000:
            break
        current_node = queue.popleft()
        # print("Level of node is: {}".format(current_node.level))
        link = current_node.node_url
        if link.find('http')==0 or link.find('#')==0:
            continue
        link = urljoin(start_url, link)
        if link in visited:
            continue
        else:
            filename = download(link)
            if not filename:
                continue
            else:
                Node.total_web_pages+= 1
            current_node.node_children = get_children_from_urls(get_links(filename), current_node)
            queue.extend(current_node.node_children)
            visited.add(link)
    end_time = time.time()
    print("\nResults:\n")
    print("Time taken to finish: {}".format(end_time-start_time))
    print("Total web pages: {}".format(Node.total_web_pages))
    print("Total link number: {}".format(Node.total_num_links))
    print("Average links per page: {}".format(np.mean(Node.links_in_page)))
    print("Median links per page: {}".format(np.median(Node.links_in_page)))
    print("Internal and external links found: {}, {}".format(Node.int_link, Node.ext_link))
    make_hist(Node.links_in_page)
    make_scat(Node.int_link, Node.ext_link)


