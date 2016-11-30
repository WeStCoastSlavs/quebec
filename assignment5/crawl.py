import os
import time
import traceback
from collections import deque
from urllib.error import HTTPError
from urllib.parse import urlparse, urljoin
from urllib.request import urlopen

import matplotlib.pyplot as plt
import numpy as np
import wget
from Node import Node
from bs4 import BeautifulSoup
from scipy.stats import gaussian_kde

from assignment5 import helper

visited = set([])


def download_urllib(url):
    parsed_url = urlparse(url)
    if parsed_url.path.find('.') == -1:
        name = 'index.html'
        file_path = parsed_url.path
        print("Filename not found!!!")
    else:
        name = parsed_url.path.split('/')[-1]
        file_path = parsed_url.path.split('/')[:-1]
        file_path = "/".join(file_path)
    try:
        response = urlopen(url)
        data = response.read()
        text = data.decode('utf-8')
        if not os.path.exists("junk/" + file_path):
            os.makedirs("junk/" + file_path)
        f = open("junk{}/{}".format(file_path, name), mode="x", encoding="utf-8")
        f.write(text)
        f.close()
        return text
    except UnicodeDecodeError:
        # traceback.print_exc()
        print("Failed decoding file: " + name)
        return False
    except HTTPError:
        # traceback.print_exc()
        return False
    except Exception:
        # traceback.print_exc()
        return False


def get_links_from_text(file):
    urls = []
    internal = 0
    external = 0
    file = file.split('\n')
    for line in file:
        while line.find('<a') != -1:
            a_start = line.find('<a')
            whole_tag = line[a_start + 2:]
            a_tag = whole_tag[:whole_tag.find('>')]
            if a_tag.find("href") == -1:
                line = line[a_start + 2:]
                continue
            href = a_tag[a_tag.find('href="') + 6:]
            path = href[:href.find('"')]
            if path.find("http") == 0:
                external += 1
            else:
                internal += 1
            urls.append(path)
            line = line[a_start + 4:]
    Node.int_link.append(internal)
    Node.ext_link.append(external)
    Node.total_num_links += len(urls)
    Node.links_in_page.append(len(urls))
    return urls


def bs_soup(text):
    urls = []
    internal = 0
    external = 0
    soup = BeautifulSoup(text, 'lxml')
    for a_tag in soup.find_all('a'):
        path = a_tag.get('href')
        if path is not None:
            if path.find("http") == 0:
                external += 1
            else:
                internal += 1
            urls.append(path)
    Node.int_link.append(internal)
    Node.ext_link.append(external)
    Node.total_num_links += len(urls)
    Node.links_in_page.append(len(urls))
    return urls


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
        if ur in visited:
            continue
        node = Node(parent, ur)
        nodes.append(node)
    return nodes


def remove_file_name(full_url):
    if full_url.find('.') == -1: return full_url
    return '/'.join(full_url.split('/')[:-1])


def make_hist(x):
    x = [s for s in x if s <= 150]
    n, bins, patches = plt.hist(x, bins=30, normed=0, facecolor='blue', alpha=0.75)
    plt.xlabel('Number of links')
    plt.ylabel('Number of pages')
    plt.title('Distribution of links')
    plt.axis([0, 150, 0, 8000])
    plt.grid(True)

    plt.show()


def make_heatmap(x,y):
    xy = list(zip(x,y))
    xy = filter(lambda p: p[0]<400 and p[1]<200, xy)
    xy = list(map(list, zip(*xy)))
    x = xy[0]
    y = xy[1]
    xy = np.vstack([x, y])
    z = gaussian_kde(xy)(xy)

    fig, ax = plt.subplots()
    plt.axis([0, 400, 0, 200])
    ax.scatter(x, y, c=z, s=100, edgecolor='')
    plt.show()

def make_scat(x,y):
    # x = [s for s in x if s < 400]
    # y = [s for s in y if s < 200]
    plt.axis([0, 400, 0, 200])
    plt.scatter(x,y)
    plt.show()


if __name__ == "__main__":
    start_time = time.time()
    start_url = "http://141.26.208.82/articles/g/e/r/Germany.html"
    start_url = "http://localhost/simple/articles/g/e/r/Germany.html"
    # start_url = "http://141.26.208.82/index.html"
    file_name = download(start_url)
    init_node = Node(None, start_url)
    init_node.node_children = get_children_from_urls(get_links(file_name), init_node)

    # init_node.node_children = list(set(init_node.node_children))

    visited.add(start_url)
    queue = deque([])
    queue.extend(init_node.node_children)

    try:
        while queue:
            # print("Size of queue {}".format(len(queue)))
            if Node.total_web_pages % 1000 == 0:
                print("Total web pages crawled: {}".format(Node.total_web_pages))
            if Node.total_web_pages == 150000:
                break
            current_node = queue.popleft()
            # print("Level of node is: {}".format(current_node.level))
            if current_node.node_url.find('http') == 0 or current_node.node_url.find('#') == 0:
                continue
            # link = urljoin(start_url, link)
            current_node.node_url = urljoin(current_node.parent.node_url, current_node.node_url)
            link = current_node.node_url
            if link in visited:
                continue
            else:
                # filename = download(link)
                filename = download_urllib(link)
                if not filename:
                    continue
                else:
                    Node.total_web_pages += 1

                current_node.node_children = get_children_from_urls(get_links_from_text(filename), current_node)
                queue.extend(current_node.node_children)
                visited.add(link)
    except KeyboardInterrupt:
        pass
    helper.write()
    end_time = time.time()
    print("\nResults:\n")
    print("Time taken to finish: {}".format(end_time-start_time))
    print("Total web pages: {}".format(Node.total_web_pages))
    print("Total link number: {}".format(Node.total_num_links))
    print("Average links per page: {}".format(np.mean(Node.links_in_page)))
    print("Median links per page: {}".format(np.median(Node.links_in_page)))
    # print("Internal and external links found: {}, {}".format(Node.int_link, Node.ext_link))
    make_hist(Node.links_in_page)
    make_scat(Node.int_link, Node.ext_link)


