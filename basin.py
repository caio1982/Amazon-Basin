#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2012 - Caio Begotti <caio1982@gmail.com>
# Distributed under the GPLv2, see the LICENSE file.

import re

import web
from web import form

from amazonwish.config import *

from amazonwish.amazonwish import Search
from amazonwish.amazonwish import Profile
from amazonwish.amazonwish import Wishlist

render = web.template.render( 'templates/', base='layout')

urls = (
    '/(.*)', 'index'
)

form = form.Form(
    form.Textbox('search',
                 form.notnull,
                 description='',
                 size='25'
                 ))

app = web.application(urls, globals(), True)

class index:        
    def GET(self, term):
        res = web.input()
        if len(res) == 0:
            f = form()
            return render.form(f)

        site = 'us'
        if 'site' in res:
            site = res['site']

        if 'search' in res:
            wl = []
            p = []
            term = res['search']
            s = Search(term, country=site)
            if len(s.list()) > 0:
                wishlist = s.list()[0][1]
                wl = Wishlist(wishlist, country=site)
                p = Profile(wishlist, country=site)
            else:
                print 'NOT FOUND! 404: ' + term
        elif 'list' in res:
            id = res['list']
            wl = Wishlist(id, country=site)
            p = Profile(id, country=site)
        else:
            f = form()
            return render.form(f)

        info = p.basicInfo()          
        total = wl.total_expenses()
        covers = wl.covers()
        urls = wl.urls()
        titles = wl.titles()
        authors = wl.authors()
        prices = wl.prices()
        items = zip(covers, urls, titles, authors, prices)
            
        listnames = p.wishlists()
        listcodes = p.wishlistsDetails()[0]
        listsizes = p.wishlistsDetails()[1]
        lists = zip(listnames, listsizes, listcodes)
        return render.result(lists, total, info, items, wl.currency)

#web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)

if __name__ == "__main__":
    #web.runwsgi = web.runfcgi
    app.run()
