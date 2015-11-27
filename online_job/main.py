import http.cookiejar as cookielib
import urllib
from bs4 import BeautifulSoup as bs

def set_cookie():
    """
    Set up a cookie for keeping the login status
    :rtype : None
    :return: None
    """
    cj = cookielib.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    return opener

def login_w_cookie(email, password, opener):
    """
    input:
    email, password - email and password for bamboofo.rest.

    output:
    none

    exp:
    this function logs you into the bamboo.
    Please do not modify this without proven necessity.

    even if your id/pass is wrong, this function would not raise any error. so be careful.
    """
    # Set up login info
    url = "https://bamboofo.rest/users/sign_in"  #login page
    data = urllib.request.urlopen(url)  #open url for token preparation
    soup = bs(data, "html.parser")  #boil soup page for token preparation
    #get CSRF-TOKEN
    CSRF_token = str(soup.find(attrs={"name": "csrf-token"})).split(" ")[1].split("=")[1][1:] + "="
    #set login information
    login_info = urllib.parse.urlencode({
                                    "utf-8" : "✓",
                                    "authenticity_token": CSRF_token,
                                    "user[email]": email,
                                    "user[password]": password})
    login_info = login_info.encode("utf-8")
    req = urllib.request.Request(url, login_info)  #send queries for login (request)
    res = opener.open(req)  #get response
    print(res)
    data = opener.open(url)
    soup = bs(data, "html.parser")
    print(soup)



