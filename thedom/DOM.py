'''
    DOM.py

    Contains all elements defined in the most recent version of the HTML specification
    (currently version 5)

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

from . import DictUtils, Factory
from .Base import Settings, Node
from .MethodUtils import CallBack
from .MultiplePythonSupport import *

Factory = Factory.Factory("DOM")

class A(Node):
    """
        Defines a link that when clicked changes the currently viewed page
    """
    __slots__ = ()
    tagName = "a"
    properties = Node.properties.copy()
    properties['href'] = {'action':'attribute'}
    properties['media'] = {'action':'attribute'}
    properties['rel'] = {'action':'attribute'}
    properties['target'] = {'action':'attribute'}
    properties['type'] = {'action':'attribute'}

Factory.addProduct(A)


class Abr(Node):
    """
        Defines an abbreviation or an acronym
    """
    __slots__ = ()
    tagName = "abr"

Factory.addProduct(Abr)


class Address(Node):
    """
        Defines contact info for the author of a document or article
    """
    __slots__ = ()
    tagName = "address"

Factory.addProduct(Address)


class Area(Node):
    """
        Defines an area inside an image map
    """
    __slots__ = ()
    tagName = "area"
    properties = Node.properties.copy()
    properties['alt'] = {'action':'attribute'}
    properties['coords'] = {'action':'attribute'}
    properties['href'] = {'action':'attribute'}
    properties['hreflang'] = {'action':'attribute'}
    properties['media'] = {'action':'attribute'}
    properties['rel'] = {'action':'attribute'}
    properties['shape'] = {'action':'attribute'}
    properties['target'] = {'action':'attribute'}
    properties['type'] = {'action':'attribute'}

Factory.addProduct(Area)


class Article(Node):
    """
        Defines an independent, self-contained content
    """
    __slots__ = ()
    tagName = "article"

Factory.addProduct(Article)


class Aside(Node):
    """
        Defines content as being aside from the content it is placed in
    """
    __slots__ = ()
    tagName = "aside"

Factory.addProduct(Aside)


class Audio(Node):
    """
        Defines sound, such as music or other audio streams
    """
    __slots__ = ()
    tagName = "audio"
    properties = Node.properties.copy()
    properties['autoplay'] = {'action':'attribute', 'type':'bool'}
    properties['controls'] = {'action':'attribute', 'type':'bool'}
    properties['loop'] = {'action':'attribute', 'type':'bool'}
    properties['src'] = {'action':'attribute'}

Factory.addProduct(Audio)


class B(Node):
    """
        Defines bold text
        NOTE: avoid using this element, when possible use elements that describe the content
              instead of the appearance
    """
    __slots__ = ()
    tagName = "b"

Factory.addProduct(B)


class Base(Node):
    """
        Defines the base URL for all relative URLs in a document
    """
    __slots__ = ()
    tagName = "base"
    properties = Node.properties.copy()
    properties['href'] = {'action':'attribute'}
    properties['target'] = {'action':'attribute'}

Factory.addProduct(Base)


class BDI(Node):
    """
        Defines a part of text that should be formatted in a different direction
        from the other text outside it
    """
    __slots__ = ()
    tagName = "bdi"

Factory.addProduct(BDI)


class BDO(Node):
    """
        Defines an override of the current text-direction
    """
    __slots__ = ()
    tagName = "bdo"
    properties = Node.properties.copy()
    properties['dir'] = {'action':'attribute'}

Factory.addProduct(BDO)


class BlockQuote(Node):
    """
        Defines a section that is quoted from another source
    """
    __slots__ = ()
    tagName = "blockquote"
    properties = Node.properties.copy()
    properties['cite'] = {'action':'attribute'}

Factory.addProduct(BlockQuote)


class Body(Node):
    """
        Defines the document's body - which contains all the visible parts of an HTML document
    """
    __slots__ = ()
    tagName = "body"

Factory.addProduct(Body)


class Br(Node):
    """
        Defines a single line break
    """
    __slots__ = ()
    tagName = "br"
    tagSelfCloses = True
    allowsChildren = False

Factory.addProduct(Br)


class Button(Node):
    """
        Defines a click-able button
    """
    __slots__ = ()
    tagName = "button"
    properties = Node.properties.copy()
    properties['autofocus'] = {'action':'attribute', 'type':'bool'}
    properties['disabled'] = {'action':'attribute', 'type':'bool'}
    properties['form'] = {'action':'attribute'}
    properties['formaction'] = {'action':'attribute'}
    properties['formenctype'] = {'action':'attribute'}
    properties['formnovalidate'] = {'action':'attribute', 'type':'bool'}
    properties['formtarget'] = {'action':'attribute'}
    properties['type'] = {'action':'attribute'}
    properties['value'] = {'action':'attribute'}

Factory.addProduct(Button)


class Canvas(Node):
    """
        Defines an area of the screen to draw graphic on the fly
    """
    __slots__ = ()
    tagName = "canvas"
    allowsChildren = False
    properties = Node.properties.copy()
    properties['height'] = {'action':'attribute', 'type':'int'}
    properties['width'] = {'action':'attribute', 'type':'int'}

Factory.addProduct(Canvas)


class Caption(Node):
    """
        Defines a table caption
    """
    __slots__ = ()
    tagName = "caption"

Factory.addProduct(Caption)


class Cite(Node):
    """
        Defines the title of a work
    """
    __slots__ = ()
    tagName = "cite"

Factory.addProduct(Cite)


class Code(Node):
    """
        Defines a piece of programming code
    """
    __slots__ = ()
    tagName = "code"

Factory.addProduct(Code)


class Col(Node):
    """
        Defines a table column
    """
    __slots__ = ()
    tagName = "col"
    properties = Node.properties.copy()
    properties['span'] = {'action':'attribute', 'type':'int'}

Factory.addProduct(Col)


class ColGroup(Node):
    """
        Defines a group of one or more columns in a table
    """
    __slots__ = ()
    tagName = "colgroup"
    properties = Node.properties.copy()
    properties['span'] = {'action':'attribute', 'type':'int'}

Factory.addProduct(ColGroup)


class Command(Node):
    """
        Defines a click-able command button
    """
    __slots__ = ()
    tagName = "command"
    properties = Node.properties.copy()
    properties['checked'] = {'action':'attribute', 'type':'bool'}
    properties['disabled'] = {'action':'attribute', 'type':'bool'}
    properties['icon'] = {'action':'attribute'}
    properties['label'] = {'action':'attribute'}
    properties['radiogroup'] = {'action':'attribute'}
    properties['type'] = {'action':'attribute'}

Factory.addProduct(Command)


class DataList(Node):
    """
        Defines a list of pre-defined options for input controls
    """
    __slots__ = ()
    tagName = "datalist"

Factory.addProduct(DataList)


class DD(Node):
    """
        Defines a description of an item in a definition list
    """
    __slots__ = ()
    tagName = "dd"

Factory.addProduct(DD)


class Del(Node):
    """
        Defines text that has been deleted from a document
    """
    __slots__ = ()
    tagName = "del"
    properties = Node.properties.copy()
    properties['cite'] = {'action':'attribute'}
    properties['datetime'] = {'action':'attribute'}

Factory.addProduct(Del)


class Details(Node):
    """
        Defines collapse-able details
    """
    __slots__ = ()
    tagName = "details"
    properties = Node.properties.copy()
    properties['open'] = {'action':'attribute'}

Factory.addProduct(Details)


class Dfn(Node):
    """
        Defines a definition term
    """
    __slots__ = ()
    tagName = "dfn"

Factory.addProduct(Dfn)


class Div(Node):
    """
        Defines a section of a document
    """
    __slots__ = ()
    tagName = "div"

Factory.addProduct(Div)


class DL(Node):
    """
        Defines a definition list
    """
    __slots__ = ()
    tagName = "dl"

Factory.addProduct(DL)


class DT(Node):
    """
        Defines a term (an item) in a definition list
    """
    __slots__ = ()
    tagName = "dt"

Factory.addProduct(DT)


class Em(Node):
    """
        Defines emphasized text
    """
    __slots__ = ()
    tagName = "em"

Factory.addProduct(Em)


class Embed(Node):
    """
        Defines a container for an external (non-HTML) application
    """
    __slots__ = ()
    tagName = "embed"
    properties = Node.properties.copy()
    properties['height'] = {'action':'attribute'}
    properties['src'] = {'action':'attribute'}
    properties['types'] = {'action':'attribute'}
    properties['width'] = {'action':'attribute', 'type':'int'}

Factory.addProduct(Embed)


class FieldSet(Node):
    """
        Defines a group of related elements in a form
    """
    __slots__ = ()
    tagName = "fieldset"
    properties = Node.properties.copy()
    properties['disabled'] = {'action':'attribute', 'type':'bool'}
    properties['form'] = {'action':'attribute'}

Factory.addProduct(FieldSet)


class FigCaption(Node):
    """
        Defines a caption for a figure element
    """
    __slots__ = ()
    tagName = "figcaption"

Factory.addProduct(FigCaption)


class Figure(Node):
    """
        Defines self-contained figure content
    """
    __slots__ = ()
    tagName = "figure"

Factory.addProduct(Figure)


class Footer(Node):
    """
        Defines a footer for a document or section
    """
    __slots__ = ()
    tagName = "footer"

Factory.addProduct(Footer)


class Form(Node):
    """
        Defines a form for user input
    """
    __slots__ = ()
    tagName = "form"
    properties = Node.properties.copy()
    properties['accept'] = {'action':'attribute'}
    properties['accept-charset'] = {'action':'attribute'}
    properties['action'] = {'action':'attribute'}
    properties['autocomplete'] = {'action':'attribute', 'type':'bool'}
    properties['enctype'] = {'action':'attribute'}
    properties['method'] = {'action':'attribute'}
    properties['name'] = {'action':'attribute'}
    properties['novalidate'] = {'action':'attribute'}
    properties['target'] = {'action':'attribute'}

Factory.addProduct(Form)


class H(Node):
    """
        Defines the abstract concept of an HTML header
    """
    __slots__ = ()


class H1(H):
    """
        Defines the most important heading
    """
    __slots__ = ()
    tagName = "h1"

Factory.addProduct(H1)


class H2(H):
    """
        Defines the 2nd most important heading
    """
    __slots__ = ()
    tagName = "h2"

Factory.addProduct(H2)


class H3(H):
    """
        Defines the 3rd most important heading
    """
    __slots__ = ()
    tagName = "h3"

Factory.addProduct(H3)


class H4(H):
    """
        Defines the 4th most important heading
    """
    __slots__ = ()
    tagName = "h4"

Factory.addProduct(H4)


class H5(H):
    """
        Defines the 5th most important heading
    """
    __slots__ = ()
    tagName = "h5"

Factory.addProduct(H5)


class H6(H):
    """
        Defines the least important heading
    """
    __slots__ = ()
    tagName = "h6"

Factory.addProduct(H6)


class Head(Node):
    """
        Defines information about the document
    """
    __slots__ = ()
    tagName = "head"

Factory.addProduct(Head)


class Header(Node):
    """
        Defines a header for a document or section
    """
    __slots__ = ()
    tagName = "header"

Factory.addProduct(Header)


class HGroup(Node):
    """
        Defines a grouping of multiple header elements
    """
    __slots__ = ()
    tagName = "hgroup"

Factory.addProduct(HGroup)


class HR(Node):
    """
        Defines a thematic change in the content horizontally
    """
    __slots__ = ()
    tagName = "hr"
    tagSelfCloses = True
    allowsChildren = False

Factory.addProduct(HR)


class HTML(Node):
    """
        Defines the root of an HTML document
    """
    __slots__ = ()
    tagName = "html"
    properties = Node.properties.copy()
    properties['manifest'] = {'action':'attribute'}

Factory.addProduct(HTML)


class I(Node):
    """
        Defines text that is in an alternate voice or mood
        NOTE: avoid using this element, when possible use elements that describe the content
              instead of the appearance
    """
    __slots__ = ()
    tagName = "i"

Factory.addProduct(I)


class IFrame(Node):
    """
        Defines an inline frame
    """
    __slots__ = ()
    tagName = "iframe"
    properties = Node.properties.copy()
    properties['sandbox'] = {'action':'attribute'}
    properties['seamless'] = {'action':'attribute', 'type':'bool'}
    properties['src'] = {'action':'attribute'}
    properties['srcdoc'] = {'action':'attribute'}
    properties['width'] = {'action':'attribute', 'type':'int'}
    properties['frameborder'] = {'action':'attribute'}

Factory.addProduct(IFrame)


class Img(Node):
    """
        Defines an image
    """
    __slots__ = ()
    tagName = "img"
    tagSelfCloses = True
    allowsChildren = False
    properties = Node.properties.copy()
    properties['src'] = {'action':'setImage'}
    properties['alt'] = {'action':'attribute'}
    properties['crossorigin'] = {'action':'attribute'}
    properties['ismap'] = {'action':'attribute', 'type':'bool'}
    properties['width'] = {'action':'attribute', 'type':'int'}
    properties['height'] = {'action':'attribute', 'type':'int'}

    def setImage(self, image):
        self.attributes['src'] = Settings.STATIC_URL + image

    def image(self):
        return self.attributes['src'].replace(Settings.STATIC_URL, "")

Factory.addProduct(Img)


class Input(Node):
    """
        Defines an input control
    """
    __slots__ = ()
    tagName = "input"
    tagSelfCloses = True
    allowsChildren = False
    properties = Node.properties.copy()
    properties['accept'] = {'action':'attribute'}
    properties['alt'] = {'action':'attribute'}
    properties['autocomplete'] = {'action':'attribute', 'type':'bool'}
    properties['autofocus'] = {'action':'attribute', 'type':'bool'}
    properties['checked'] = {'action':'attribute', 'type':'bool'}
    properties['disabled'] = {'action':'attribute', 'type':'bool'}
    properties['form'] = {'action':'attribute'}
    properties['formaction'] = {'action':'attribute'}
    properties['formenctype'] = {'action':'attribute'}
    properties['formmethod'] = {'action':'attribute'}
    properties['formnovalidate'] = {'action':'attribute'}
    properties['formtarget'] = {'action':'attribute'}
    properties['height'] = {'action':'attribute', 'type':'int'}
    properties['list'] = {'action':'attribute'}
    properties['max'] = {'action':'attribute'}
    properties['maxlength'] = {'action':'attribute', 'type':'int'}
    properties['min'] = {'action':'attribute'}
    properties['multiple'] = {'action':'attribute', 'type':'bool'}
    properties['pattern'] = {'action':'attribute'}
    properties['placeholder'] = {'action':'attribute'}
    properties['readonly'] = {'action':'attribute', 'type':'bool'}
    properties['required'] = {'action':'attribute', 'type':'bool'}
    properties['size'] = {'action':'attribute', 'type':'int'}
    properties['src'] = {'action':'attribute'}
    properties['step'] = {'action':'attribute', 'type':'int'}
    properties['type'] = {'action':'attribute'}
    properties['value'] = {'action':'attribute'}
    properties['width'] = {'action':'attribute', 'type':'int'}

Factory.addProduct(Input)


class Ins(Node):
    """
        Defines text that has been inserted into a document
    """
    __slots__ = ()
    tagName = "ins"
    properties = Node.properties.copy()
    properties['cite'] = {'action':'attribute'}
    properties['datetime'] = {'action':'attribute'}

Factory.addProduct(Ins)


class Kbd(Node):
    """
        Defines keyboard input
    """
    __slots__ = ()
    tagName = "kbd"

Factory.addProduct(Kbd)


class KeyGen(Node):
    """
        Defines a key-pair generator field
    """
    __slots__ = ()
    tagName = "keygen"
    properties = Node.properties.copy()
    properties['autofocus'] = {'action':'attribute', 'type':'bool'}
    properties['challenge'] = {'action':'attribute', 'type':'bool'}
    properties['disabled'] = {'action':'attribute', 'type':'bool'}
    properties['form'] = {'action':'attribute'}
    properties['keytype'] = {'action':'attribute'}
    properties['name'] = {'action':'attribute'}

Factory.addProduct(KeyGen)


class Label(Node):
    """
        Defines a label for an input element
    """
    __slots__ = ()
    tagName = "label"
    properties = Node.properties.copy()
    properties['for'] = {'action':'attribute'}
    properties['form'] = {'action':'attribute'}

Factory.addProduct(Label)


class Legend(Node):
    """
        Defines a caption for a fieldset, figure or details element
    """
    __slots__ = ()
    tagName = "legend"

Factory.addProduct(Legend)


class LI(Node):
    """
        Defines a list item
    """
    __slots__ = ()
    tagName = "li"
    properties = Node.properties.copy()
    properties['value'] = {'action':'attribute', 'type':'int'}

Factory.addProduct(LI)


class Link(Node):
    """
        Defines the relationship between a document an external resource
    """
    __slots__ = ()
    tagName = "link"
    tagSelfCloses = True
    allowsChildren = False
    properties = Node.properties.copy()
    properties['charset'] = {'action':'attribute'}
    properties['src'] = {'action':'setSource'}
    properties['href'] = {'action':'setHref'}
    properties['hreflang'] = {'action':'attribute'}
    properties['media'] = {'action':'attribute'}
    properties['rel'] = {'action':'attribute'}
    properties['type'] = {'action':'attribute'}
    properties['sizes'] = {'action':'attribute'}

    def setHref(self, href):
        self.attributes['href'] = Settings.STATIC_URL + href

    def href(self):
        return self.attributes['href'].replace(Settings.STATIC_URL, "")

    def setSource(self, source):
        self.attributes['src'] = Settings.STATIC_URL + source

    def source(self, source):
        return self.attributes['src'].replace(Settings.STATIC_URL, "")

Factory.addProduct(Link)


class Map(Node):
    """
        Defines a client side image map
    """
    __slots__ = ()
    tagName = "map"

Factory.addProduct(Map)


class Mark(Node):
    """
        Defines marked / highlighted text
    """
    __slots__ = ()
    tagName = "mark"

Factory.addProduct(Mark)


class Meta(Node):
    """
        Defines metadata about an HTML document
    """
    __slots__ = ()
    tagName = "meta"
    tagSelfCloses = True
    allowsChildren = False
    properties = Node.properties.copy()
    properties['charset'] = {'action':'attribute'}
    properties['content'] = {'action':'attribute'}
    properties['http-equiv'] = {'action':'attribute'}

Factory.addProduct(Meta)


class Meter(Node):
    """
        Defines a scalar measurement within a known range
    """
    __slots__ = ()
    tagName = "meter"
    properties = Node.properties.copy()
    properties['form'] = {'action':'attribute'}
    properties['high'] = {'action':'attribute', 'type':'int'}
    properties['low'] = {'action':'attribute', 'type':'int'}
    properties['max'] = {'action':'attribute', 'type':'int'}
    properties['min'] = {'action':'attribute', 'type':'int'}
    properties['optimum'] = {'action':'attribute', 'type':'int'}
    properties['value'] = {'action':'attribute', 'type':'int'}

Factory.addProduct(Meter)


class Nav(Node):
    """
        Defines navigation links
    """
    __slots__ = ()
    tagName = "nav"

Factory.addProduct(Nav)


class NoScript(Node):
    """
        Defines alternate content for users that do not support client side scripts
    """
    __slots__ = ()
    tagName = "noscript"

Factory.addProduct(NoScript)


class Object(Node):
    """
        Defines an embedded object
    """
    __slots__ = ()
    tagName = "object"
    properties = Node.properties.copy()
    properties['form'] = {'action':'attribute'}
    properties['height'] = {'action':'attribute', 'type':'int'}
    properties['type'] = {'action':'attribute'}
    properties['usemap'] = {'action':'attribute'}
    properties['width'] = {'action':'attribute', 'type':'int'}

Factory.addProduct(Object)


class OL(Node):
    """
        Defines an ordered list
    """
    __slots__ = ()
    tagName = "ol"
    properties = Node.properties.copy()
    properties['reversed'] = {'action':'attribute', 'type':'bool'}
    properties['start'] = {'action':'attribute', 'type':'int'}
    properties['type'] = {'action':'attribute'}

Factory.addProduct(OL)


class OptGroup(Node):
    """
        Defines a group of related options in a drop-down list
    """
    __slots__ = ()
    tagName = "optgroup"
    properties = Node.properties.copy()
    properties['disabled'] = {'action':'attribute', 'type':'bool'}
    properties['label'] = {'action':'attribute'}

Factory.addProduct(OptGroup)


class Option(Node):
    """
        Defines an option in a drop-down list
    """
    __slots__ = ()
    tagName = "option"
    properties = Node.properties.copy()
    properties['disabled'] = {'action':'attribute', 'type':'bool'}
    properties['label'] = {'action':'attribute'}
    properties['selected'] = {'action':'attribute', 'type':'bool'}
    properties['value'] = {'action':'attribute'}

Factory.addProduct(Option)


class Output(Node):
    """
        Defines the result of a calculation
    """
    __slots__ = ()
    tagName = "output"
    properties = Node.properties.copy()
    properties['for'] = {'action':'attribute'}
    properties['form'] = {'action':'attribute'}

Factory.addProduct(Output)


class P(Node):
    """
        Defines a paragraph
    """
    __slots__ = ()
    tagName = "p"

Factory.addProduct(P)


class Param(Node):
    """
        Defines a parameter for an object
    """
    __slots__ = ()
    tagName = "param"
    tagSelfCloses = True
    allowsChildren = False
    properties = Node.properties.copy()
    properties['value'] = {'action':'attribute'}

Factory.addProduct(Param)


class Pre(Node):
    """
        Defines pre formatted text
    """
    __slots__ = ()
    tagName = "pre"

Factory.addProduct(Pre)


class Progress(Node):
    """
        Defines the progress of a task
    """
    __slots__ = ()
    tagName = "progress"
    properties = Node.properties.copy()
    properties['max'] = {'action':'attribute', 'type':'int'}
    properties['value'] = {'action':'attribute', 'type':'int'}

Factory.addProduct(Progress)


class Q(Node):
    """
        Defines a short quotation
    """
    __slots__ = ()
    tagName = "q"
    properties = Node.properties.copy()
    properties['cite'] = {'action':'attribute'}

Factory.addProduct(Q)


class RP(Node):
    """
        Defines what to show in browsers that do not support ruby annotations
    """
    __slots__ = ()
    tagName = "rp"

Factory.addProduct(RP)


class RT(Node):
    """
        Defines an explanation / pronunciation of characters (for East Asian typography)
    """
    __slots__ = ()
    tagName = "rt"

Factory.addProduct(RT)


class Ruby(Node):
    """
        Defines ruby annotations (for East Asian typography)
    """
    __slots__ = ()
    tagName = "ruby"

Factory.addProduct(Ruby)


class S(Node):
    """
        Defines text that is no longer correct
    """
    __slots__ = ()
    tagName = "s"

Factory.addProduct(S)


class Samp(Node):
    """
        Defines sample output from a computer program
    """
    __slots__ = ()
    tagName = "samp"

Factory.addProduct(Samp)


class Script(Node):
    """
        Defines a client-side script
    """
    __slots__ = ()
    tagName = "script"
    properties = Node.properties.copy()
    properties['async'] = {'action':'attribute', 'type':'bool'}
    properties['defer'] = {'action':'attribute', 'type':'bool'}
    properties['type'] = {'action':'attribute'}
    properties['charset'] = {'action':'attribute'}
    properties['src'] = {'action':'setScriptFile'}

    def setScriptFile(self, scriptFile):
        self.attributes['src'] = Settings.STATIC_URL + scriptFile

    def scriptFile(self):
        return self.attributes['src'].replace(Settings.STATIC_URL, "")

Factory.addProduct(Script)


class Section(Node):
    """
        Defines a section of the document
    """
    __slots__ = ()
    tagName = "section"

Factory.addProduct(Section)


class Select(Node):
    """
        Defines a drop-down list
    """
    __slots__ = ()
    tagName = "select"
    properties = Node.properties.copy()
    properties['autofocus'] = {'action':'attribute', 'type':'bool'}
    properties['disabled'] = {'action':'attribute', 'type':'bool'}
    properties['form'] = {'action':'attribute'}
    properties['multiple'] = {'action':'attribute', 'type':'bool'}
    properties['size'] = {'action':'attribute', 'type':'int'}

Factory.addProduct(Select)


class Small(Node):
    """
        Defines smaller text
        NOTE: avoid using this element, when possible use elements that describe the content
              instead of the appearance
    """
    __slots__ = ()
    tagName = "small"

Factory.addProduct(Small)


class Source(Node):
    """
        Defines multiple media resources for media elements
    """
    __slots__ = ()
    tagName = "source"
    properties = Node.properties.copy()
    properties['media'] = {'action':'attribute'}
    properties['src'] = {'action':'attribute'}
    properties['type'] = {'action':'attribute'}

Factory.addProduct(Source)


class Span(Node):
    """
        Defines a section in a document
    """
    __slots__ = ()
    tagName = "span"

Factory.addProduct(Span)


class Strong(Node):
    """
        Defines important text
    """
    __slots__ = ()
    tagName = "strong"

Factory.addProduct(Strong)


class Style(Node):
    """
        Defines style information for a document
    """
    __slots__ = ()
    tagName = "style"
    properties = Node.properties.copy()
    properties['media'] = {'action':'attribute'}
    properties['scoped'] = {'action':'attribute', 'type':'bool'}
    properties['type'] = {'action':'attribute'}

Factory.addProduct(Style)


class Sub(Node):
    """
        Defines sub-scripted text
    """
    __slots__ = ()
    tagName = "sub"

Factory.addProduct(Sub)


class Summary(Node):
    """
        Defines a visible heading for a details element
    """
    __slots__ = ()
    tagName = "summary"

Factory.addProduct(Summary)


class Sup(Node):
    """
        Defines super-scripted text
    """
    __slots__ = ()
    tagName = "sup"

Factory.addProduct(Sup)


class Table(Node):
    """
        Defines a table - should be used for tables of data only (not for layout)
    """
    __slots__ = ()
    tagName = "table"
    properties = Node.properties.copy()
    properties['border'] = {'action':'attribute', 'type':'bool'}

Factory.addProduct(Table)


class TBody(Node):
    """
        Defines a group of content within a table
    """
    __slots__ = ()
    tagName = "tbody"

Factory.addProduct(TBody)


class TD(Node):
    """
        Defines a table cell
    """
    __slots__ = ()
    tagName = "td"
    properties = Node.properties.copy()
    properties['colspan'] = {'action':'attribute', 'type':'number'}
    properties['headers'] = {'action':'attribute'}
    properties['rowspan'] = {'action':'attribute', 'type':'number'}

Factory.addProduct(TD)


class TextArea(Node):
    """
        Defines multi-line text input
    """
    __slots__ = ()
    tagName = "textarea"
    properties = Node.properties.copy()
    properties['autofocus'] = {'action':'attribute', 'type':'bool'}
    properties['cols'] = {'action':'attribute', 'type':'int'}
    properties['disabled'] = {'action':'attribute', 'type':'bool'}
    properties['form'] = {'action':'attribute'}
    properties['maxlength'] = {'action':'attribute', 'type':'int'}
    properties['placeholder'] = {'action':'attribute'}
    properties['readonly'] = {'action':'attribute', 'type':'bool'}
    properties['required'] = {'action':'attribute', 'type':'bool'}
    properties['rows'] = {'action':'attribute', 'type':'int'}
    properties['wrap'] = {'action':'attribute'}

Factory.addProduct(TextArea)


class TFoot(Node):
    """
        Defines the footer of a table
    """
    __slots__ = ()
    tagName = "tfoot"

Factory.addProduct(TFoot)


class TH(Node):
    """
        Defines the header cell within a table
    """
    __slots__ = ()
    tagName = "th"
    properties = Node.properties.copy()
    properties['colspan'] = {'action':'attribute', 'type':'int'}
    properties['headers'] = {'action':'attribute'}
    properties['rowspan'] = {'action':'attribute', 'type':'int'}
    properties['scope'] = {'action':'attribute'}

Factory.addProduct(TH)


class THead(Node):
    """
        Defines header content within a table
    """
    __slots__ = ()
    tagName = "thead"

Factory.addProduct(THead)


class Time(Node):
    """
        Defines a date / time
    """
    __slots__ = ()
    tagName = "time"
    properties = Node.properties.copy()
    properties['datetime'] = {'action':'attribute'}
    properties['pubdate'] = {'action':'attribute'}

Factory.addProduct(Time)


class Title(Node):
    """
        Defines the title of a document
    """
    __slots__ = ()
    tagName = "title"

Factory.addProduct(Title)


class TR(Node):
    """
        Defines a table row
    """
    __slots__ = ()
    tagName = "tr"

Factory.addProduct(TR)


class Track(Node):
    """
        Defines text tracks for media elements
    """
    __slots__ = ()
    tagName = "track"
    properties = Node.properties.copy()
    properties['default'] = {'action':'attribute', 'type':'bool'}
    properties['kind'] = {'action':'attribute'}
    properties['label'] = {'action':'attribute'}
    properties['src'] = {'action':'attribute'}
    properties['srclang'] = {'action':'attribute'}

Factory.addProduct(Track)


class U(Node):
    """
        Defines text that should be stylistically different from normal text
        NOTE: avoid using this element, when possible use elements that describe the content
              instead of the appearance
    """
    __slots__ = ()
    tagName = "u"

Factory.addProduct(U)


class UL(Node):
    """
        Defines an unordered list
    """
    __slots__ = ()
    tagName = "ul"

Factory.addProduct(UL)


class Var(Node):
    """
        Defines a variable
    """
    __slots__ = ()
    tagName = "var"

Factory.addProduct(Var)


class Video(Node):
    """
        Defines a video or movie
    """
    __slots__ = ()
    tagName = "video"
    properties = Node.properties.copy()
    properties['autoplay'] = {'action':'attribute', 'type':'bool'}
    properties['controls'] = {'action':'attribute', 'type':'bool'}
    properties['height'] = {'action':'attribute', 'type':'int'}
    properties['loop'] = {'action':'attribute', 'type':'bool'}
    properties['muted'] = {'action':'attribute', 'type':'bool'}
    properties['poster'] = {'action':'attribute'}
    properties['preload'] = {'action':'attribute'}
    properties['src'] = {'action':'attribute'}
    properties['width'] = {'action':'attribute', 'type':'int'}

Factory.addProduct(Video)


class Wbr(Node):
    """
        Defines a possible line-break
    """
    __slots__ = ()
    tagName = "wbr"

Factory.addProduct(Wbr)
