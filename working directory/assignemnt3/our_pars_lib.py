# coding: utf-8

url = "www.example.com:80/path/to/myfile.html?key1=value1&key2=value2#InTheDocument"

def get_protocol(url):
    if "://" not in url:
        return ""
    return url.split(":")[0]


def get_port(url):
    if get_protocol(url) != "":
        if len(url.split(":")) > 2:
            return url.split(":")[2].split("/")[0]
        else:
            return url.split(":")[1].split("/")[0]
    elif get_protocol(url) == "":
        if len(url.split(":")) > 1:
            return url.split(":")[1].split("/")[0]
        else:
            return ""


def get_params(url):
    if "?" not in url:
        return ""
    splited = url.split("?")[1]
    if "#" in splited:
        splited = splited.split("#")[0]
    return splited.split("&")

def get_fragment(url):
    if "#" not in url:
        return ""
    else:
        return url.split("#")[1]

def get_domain(url):
    if get_port(url) != "" and get_protocol(url) != "":
        return url.split(":")[1].strip("//").strip("www.")
    elif get_protocol(url) == "":
        return url.split(":")[0].strip("www.")
    elif get_port(url) != "":
         return url.split("://")[1].strip("www.")


def get_subdomain(domain):
    if len(domain.split(".")) < 3:
        return ""
    return domain.split(".")


def get_params(url):
    if "?" not in url:
        return ""
    splited = url.split("?")[1]
    if "#" in splited:
        splited = splited.split("#")[0]
    return splited.split("&")


def get_fragment(url):
    if "#" not in url:
        return ""
    else:
        return url.split("#")[1]


url = "http://www.example.com:80/path/to/myfile.html?key1=value1&key2=value2#InTheDocument"
def get_path(url):
    x = url
    if get_protocol(x) != "":
        x = x.split("://")[1]
        #print(x)
    if get_port(x) != "":
        port = get_port(x)
        x = x.split(":")[1]
        x = x.strip(port)
        #print(x)
    else:
        y = x.split("/")[1:]
        x = "/"+"/".join(y)
    if "#" in x:
        x = x.split("#")[0]
    if "?" in x:
        x = x.split("?")[0]
    if "/" not in x or len(x) < 2:
        x = ""
    return x


# In[33]:

url = "www.example.com"
get_path(url)

