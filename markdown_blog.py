#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import expanduser
import sys
home = expanduser("~")
sys.path.append(home + '/lib_p_bz')
sys.path.append('./markdown-search')
import tornado.ioloop
import tornado.web
import public_bz

from tornado.web import RequestHandler
import tornado_bz
import sys
from markdown_search import search

MD_PATH = home + '/Dropbox/blog/data/'

import misaka


def gfm(str_md=''):
    '''
    transform the markdown text to html, using github favoured markdown
    usage: str_html = gfm(str_md)
    '''
    str_html = ''
    return misaka.html(str_md, extensions=misaka.EXT_FENCED_CODE | misaka.EXT_NO_INTRA_EMPHASIS)
    # str_html = misaka.html(str_md,
    #                        extensions=misaka.EXT_NO_INTRA_EMPHASIS | misaka.EXT_FENCED_CODE |
    #                        misaka.EXT_AUTOLINK | misaka.HTML_HARD_WRAP |
    #                        misaka.EXT_TABLES | misaka.HTML_USE_XHTML |
    #                        misaka.HTML_HARD_WRAP)
    return str_html


def getContent(name):
    try:
        name_file = open(MD_PATH + name, 'r')
        content = name_file.read()
        name_file.close()
        return content
    except IOError:
        print public_bz.getExpInfoAll()
        return '0'


class blog(RequestHandler):

    '''
    显示 blog 的详细内容
    '''

    def get(self, name=None):
        if name is None:
            mds = search(MD_PATH, '*')
            self.redirect('/' + mds[0][0])
        else:
            print name
            content = getContent(name)
            content = gfm(content)

            if name.endswith('.md'):
                name = name[:-len('.md')]
            self.render('./blog.html', title=name, content=content)


if __name__ == "__main__":
    the_class = globals().copy()

    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    else:
        port = 8888
    print port

    url_map = tornado_bz.getURLMap(the_class)
    url_map.append((r'/(.*)', blog))
    url_map.append((r'/static/(.*)', tornado.web.StaticFileHandler, {'path': "./static"}))

    settings = tornado_bz.getSettings()

    application = tornado.web.Application(url_map, **settings)

    application.listen(port)
    ioloop = tornado.ioloop.IOLoop().instance()
    tornado.autoreload.start(ioloop)
    ioloop.start()