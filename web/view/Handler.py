import logging

import tornado


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        data = self.get_argument('name',None)
        logging.info(data)
        self.render('hello.html',data=data)
        # self.write("hello smallqiang")
    def post(self):
        import time
        title = self.get_argument('title', None)
        content = self.get_argument('content', None)
        blog = dict()
        if title and content:
            blog['title'] = title
            blog['content'] = content
            blog['date'] = int(time.time())
            coll = self.application.db.blog
            coll.insert(blog)
            self.redirect('/blog')
        self.redirect('/')

class BlogHandler(tornado.web.RequestHandler):
    def get(self):
        coll = self.application.db.blog
        blog = coll.find_one()
        if blog:
            self.render("blog.html",
            page_title = blog['title'],
            blog = blog,
            )
        else:
            self.redirect('/')
class EditHandler(tornado.web.RequestHandler):
    def get(self, id=None):
        blog = dict()
        if id:
            coll = self.application.db.blog
            blog = coll.find_one({"id": int(id)})
        self.render("edit.html",
            blog = blog)

    def post(self, id=None):
        import time
        coll = self.application.db.blog
        blog = dict()
        if id:
            blog = coll.find_one({"id": int(id)})
        blog['title'] = self.get_argument("title", None)
        blog['content'] = self.get_argument("content", None)
        if id:
            coll.save(blog)
        else:
            last = coll.find().sort("id",pymongo.DESCENDING).limit(1)
            lastone = dict()
            for item in last:
                lastone = item
            blog['id'] = int(lastone['id']) + 1
            blog['date'] = int(time.time())
            coll.insert(blog)
        self.redirect("/")
class DelHandler(tornado.web.RequestHandler):
    def get(self, id=None):
        coll = self.application.db.blog
        if id:
            blog = coll.remove({"id": int(id)})
        self.redirect("/")
class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        data = self.get_argument("name","qiang")
        self.write(data)