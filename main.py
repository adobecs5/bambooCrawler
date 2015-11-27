from bs4 import BeautifulSoup as bs
import urllib
import http.cookiejar

def login_and_return_opener():
    cj = http.cookiejar.LWPCookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    urllib.request.install_opener(opener)

    homepage_url = "https://bamboofo.rest/users/sign_in"
    user_id = "download@kaist.ac.kr"
    user_pass = "00000000"
    a = opener.open(homepage_url)
    soup = bs(a, "html.parser")
    CSRF_token = str(soup.find(attrs={"name": "csrf-token"})).split(" ")[1].split("=")[1][1:] + "="

    params = urllib.parse.urlencode({"utf-8":"✓", "authenticity_token": CSRF_token,"user[email]":user_id, "user[password]":user_pass})
    params = params.encode('utf-8')
    req = urllib.request.Request(homepage_url, params)
    res = opener.open(req)
    return opener

def get_new_posts(opener):
    page = "https://bamboofo.rest/posts"
    page = opener.open("https://bamboofo.rest/posts")
    soup = bs(page, "html.parser")
    # print(soup)
    new_posts = soup.findAll("tr", { "class" : "row_type_N" }) # get New posts
    links = []
    for post in new_posts:
        links.append(post.attrs['href'].split("/")[-1])
    return links

def get_updated_posts(opener):
    links = []
    page = "https://bamboofo.rest/posts"
    page = opener.open("https://bamboofo.rest/posts")
    soup = bs(page, "html.parser")
    updated_posts = soup.findAll("tr", { "class" : "row_type_U" }) # get Updated posts
    for post in updated_posts:
        links.append(post.attrs['href'].split("/")[-1])
    return links

def get_post(opener, aLink):
    full_url = "https://bamboofo.rest/posts/" + aLink
    req = urllib.request.Request(full_url)
    res = opener.open(req)
    soup = bs(res, "html.parser")

class post(object):
    def __init__(self, post, comments):
        self.writer = post["writer"]
        self.board = post["board"]
        self.title = post["title"]
        self.body = post["body"]
        self.comments = comments

    def addComment(self, aComment):
        for i in range(len(self.comment)):
            comment = self.comment[i]
            if comment.writer == aComment.writer:
                self.comment[i].updown = aComment.updown
                return
        self.comments.append(aComment)

    class comment(object):
        def __init__(self, writer, updown, body):
            self.writer = writer
            self.updown = updown
            self.body = body

    def __repr__(self):
        return self.title

#print(soup)
def get_texts(soup):
    # crawl post body and comments
    upperbar = soup.find("h3").contents
    board = upperbar[1].text
    title = upperbar[3]
    name = soup.find("span", {"class" : "col-md-3"}).text.replace("\n", "").replace(" ", "")
    body = soup.find("div", {"class":"col-md-12"}).text
    aPost = {"writer":name, "board":board, "title":title, "body":body}
    comments_raw = soup.findAll("div", {"class":"comment"})
    comments = []
    for comment_raw in comments_raw:
        one_comment = comment_raw.contents
        comment_writer = one_comment[1].contents[1].text.replace("\n", "").replace(" ", "")
        comment_updown = one_comment[1].contents[3].text.replace("\n", "")
        comment_body = one_comment[3].text
        aComment = post.comment(comment_writer, comment_updown, comment_body)
        comments.append(aComment)
    return post(aPost, comments)


#comment = soup.findAll("div", {"class" : "col-md-3"})
#print(comment[0].text.replace(" ", "").replace("\n", ""))
if __name__ == "main":
    opener = login_and_return_opener()
    page = "https://bamboofo.rest/posts"
    page = opener.open("https://bamboofo.rest/posts")
    soup = bs(page, "html.parser")
    a = get_texts(soup)
    print (a)
