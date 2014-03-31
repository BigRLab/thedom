'''
    Document.py

    Provides elements that define the html document being served to the client-side

    Copyright (C) 2013  Timothy Edmund Crosley

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

from . import Base, Factory
from .MethodUtils import CallBack
from .MultiplePythonSupport import *
from .Resources import ResourceFile

Factory = Factory.Factory("Document")

DOCTYPE_XHTML_TRANSITIONAL = ('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" '
                              '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">')
DOCTYPE_XHTML_STRICT = ('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" '
                        '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">')
DOCTYPE_XHTML_FRAMESET = ('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" '
                          '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">')
DOCTYPE_HTML4_TRANSITIONAL = ('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" '
                              '"http://www.w3.org/TR/REC-html40/loose.dtd">')
DOCTYPE_HTML4_STRICT = ('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"'
                        '"http://www.w3.org/TR/html4/strict.dtd">')
DOCTYPE_HTML4_FRAMESET = ('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" '
                          '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">')
DOCTYPE_HTML5 = "<!DOCTYPE html>"

class MetaData(Base.Node):
    """
        A webelement implementation of the meta tag
    """
    __slots__ = ()
    tagName = "meta"
    displayable = False

    properties = Base.Node.properties.copy()
    properties['value'] = {'action':'setValue'}
    properties['name'] = {'action':'setName'}
    properties['http-equiv'] = {'action':'attribute'}

    def _create(self, id=None, name=None, parent=None, **kwargs):
        Base.Node._create(self)

    def value(self):
        """
            Returns the meta tags value
        """
        return self.attributes.get('content')

    def setValue(self, value):
        """
            Sets the meta tags value
        """
        self.attributes['content'] = value

    def getName(self):
        """
            Returns the name of the meta tag
         """
        return self.name

    def setName(self, name):
        """
            Sets the name of the meta tag
        """
        self.name = name

    def shown(self):
        """
            Meta tags are never visible
        """
        return False

Factory.addProduct(MetaData)


class HTTPHeader(MetaData):
    """
        A webelement that represents an http header meta tag
    """
    __slots__ = ()
    def getName(self):
        """
            Returns the headers name
        """
        return self.attributes.get('http-equiv')

    def setName(self, name):
        """
            Sets the headers name
        """
        self.attributes['http-equiv'] = name

Factory.addProduct(HTTPHeader)


class Document(Base.Node):
    """
        A Node representation of the overall document that fills a single page
    """
    __slots__ = ('head', 'body', 'title', 'contentType')
    doctype = DOCTYPE_HTML5
    tagName = "html"
    properties = Base.Node.properties.copy()
    properties['doctype'] = {'action':'classAttribute'}
    properties['title'] = {'action':'title.setText'}
    properties['contentType'] = {'action':'contentType.setValue'}
    properties['xmlns'] = {'action':'attribute'}

    class Head(Base.Node):
        """
            Documents Head
        """
        tagName = "head"

    class Body(Base.Node):
        """
            Documents Body
        """
        tagName = "body"

    class Title(Base.Node):
        """
            Documents Title
        """
        tagName = "title"

        def _create(self, id=None, name=None, parent=None, **kwargs):
            Base.Node._create(self, id=id, name=name, parent=parent)

            self._textNode = self.add(Base.TextNode())


        def setText(self, text):
            """
                Sets the document title
            """
            self._textNode.setText(text)

        def text(self):
            """
                Returns the document title
            """
            return self._textNode.text(text)

    def _create(self, id=None, name=None, parent=None, **kwargs):
        Base.Node._create(self)
        self.head = self.add(self.Head())
        self.body = self.add(self.Body())
        self.title = self.head.add(self.Title())
        self.contentType = self.addHeader('Content-Type', 'text/html; charset=UTF-8')

    def addMetaData(self, name=None, value="", **kwargs):
        """
            Will add a meta tag based on name+value pair
        """
        metaTag = self.head.add(MetaData(**kwargs))
        metaTag.setName(name)
        metaTag.setValue(value)
        return metaTag

    def addHeader(self, name, value):
        """
            Will add an HTTP header pair based on name + value pair
        """
        header = self.head.add(HTTPHeader())
        header.setName(name)
        header.setValue(value)
        return header

    def toHTML(self, formatted=False, *args, **kwargs):
        """
            Overrides toHTML to include the doctype definition before the open tag.
        """
        return self.doctype + "\n" + Base.Node.toHTML(self, formatted, *args, **kwargs)

    def add(self, childElement, ensureUnique=True):
        """
            Overrides add to place header elements and resources in the head
            and all others in the body.
        """
        if type(childElement) in [self.Head, self.Body]:
            return Base.Node.add(self, childElement, ensureUnique)
        elif type(childElement) == ResourceFile or childElement._tagName in ['title', 'base', 'link',
                                                                             'meta', 'script', 'style']:
            return self.head.add(childElement, ensureUnique)
        else:
            return self.body.add(childElement, ensureUnique)

Head = Document.Head
Body = Document.Body
Title = Document.Title
Factory.addProduct(Document)
