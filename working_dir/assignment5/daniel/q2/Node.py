class Node:
    def __init__(self, _parent, _node_url):
        self.parent = _parent
        self.node_url = _node_url
        self.node_children = []
        if _parent is None:
            self.level = 0
        else:
            self.level = _parent.level+1
        self.link_num = 0

    total_web_pages = 1
    total_num_links = 0
    links_in_page = []
    int_link = []
    ext_link = []

