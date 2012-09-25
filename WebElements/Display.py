#!/usr/bin/python
"""
   Name:
       Display

   Description:
       Contains elements that are used solely to display information on the screen

"""

import Base
import DictUtils
import DOM
import Factory
from Inputs import ValueElement
from MethodUtils import CallBack

Factory = Factory.Factory("Display")


class Image(ValueElement):
    """
        Adds an image to the page
    """
    __slots__ = ()

    tagName = "img"
    allowsChildren = False
    tagSelfCloses = True
    properties = ValueElement.properties.copy()
    properties['src'] = {'action':'setValue'}

    def __init__(self, id=None, name=None, parent=None):
        ValueElement.__init__(self, id, name, parent)

    def setValue(self, value):
        """
            Sets the location from which to load the image
        """
        ValueElement.setValue(self, value)
        self.attributes['src'] = value

Factory.addProduct(Image)


class HoverImage(Image):
    """
        Defines an image that changes on mouseover
    """
    __slots__ = ()

    properties = ValueElement.properties.copy()
    properties['imageOnHover'] = {'action':'classAttribute'}
    properties['imageOnClick'] = {'action':'classAttribute'}
    imageOnHover = None
    imageOnClick = None

    def __init__(self, id=None, name=None, parent=None):
        Image.__init__(self, id, name, parent)

        self.connect("beforeToHtml", None, self, "__addEvents__")

    def __addEvents__(self):
        if self.imageOnHover:
            self.addJavascriptEvent('onmouseover', "this.src = '%s';" % self.imageOnHover)
            self.addJavascriptEvent('onmouseout', "this.src = '%s';" % self.value())
        if self.imageOnClick:
            self.addJavascriptEvent('onmousedown', "this.src = '%s';" % self.imageOnClick)
            self.addJavascriptEvent('onmouseup', "this.src = '%s';" % self.value())

Factory.addProduct(HoverImage)


class List(Base.WebElement):
    """
        Defines a list webelement (that will automatically list out its child elements in the format chosen)
    """
    __slots__ = ('ordered')

    tagName = "ul"
    properties = Base.WebElement.properties.copy()
    properties['ordered'] = {'action':'classAttribute', 'type':'bool'}
    properties['type'] = {'action':'attribute'}

    class Item(Base.WebElement):
        """
            Defines an individual Item within a list
        """
        __slots__ = ('_textNode')

        tagName = "li"

        def __init__(self, id=None, name=None, parent=None):
            Base.WebElement.__init__(self, id=id, name=name, parent=parent)

            self._textNode = self.addChildElement(Base.TextNode())

        def setText(self, text):
            """
                Sets the displayed item text
            """
            self._textNode.setText(text)

        def text(self):
            """
                Returns the displayed item text
            """
            return self._textNode.text()

    def __init__(self, id=None, name=None, parent=None):
        Base.WebElement.__init__(self, id=id, name=name, parent=parent)
        self.ordered = False
        self.connect("beforeToHtml", None, self, "__updateTag__")

    def addChildElement(self, childElement):
        item = self.Item()
        item.addChildElement(childElement)
        Base.WebElement.addChildElement(self, item)

        return childElement

    def addItem(self, name):
        """
            Adds an item to the list with text set as name
        """
        item = self.Item()
        item.setText(name)
        return Base.WebElement.addChildElement(self, item)

    def __updateTag__(self):
        if self.ordered:
            self._tagName = "ol"

Item = List.Item
Factory.addProduct(List)


class Label(Base.WebElement):
    """
        Defines a label webelement, which will display a single string of text to the user
    """
    __slots__ = ('_textNode')

    tagName = 'span'
    signals = Base.WebElement.signals + ['textChanged']
    properties = Base.WebElement.properties.copy()
    properties['text'] = {'action':'setText'}
    properties['useNBSP'] = {'action':'call', 'type':'bool'}
    properties['strong'] = {'action':'call', 'name':'makeStrong', 'type':'bool'}
    properties['emphasis'] = {'action':'call', 'name':'addEmphasis', 'type':'bool'}

    def __init__(self, id=None, name=None, parent=None):
        Base.WebElement.__init__(self, id=id, name=name, parent=parent)

        self._textNode = self.addChildElement(Base.TextNode())

    def setText(self, text):
        """
            Sets the displayed text
        """
        if text != self._textNode.text():
            self._textNode.setText(text)
            self.emit('textChanged', text)

    def useNBSP(self):
        """
            Replaces the text with a single space character
        """
        self.setText('&nbsp;')

    def text(self):
        """
            Returns the displayed text
        """
        return self._textNode.text()

    def appendText(self, text):
        """
            Adds a new line character followed by additional text
        """
        prevText = self.text()
        if not prevText:
            return self.setText(text)

        self.setText(prevText + "<br />" + text)

    def makeStrong(self):
        """
            wraps into a strong tag - requires parent element to be defined
        """
        strong = DOM.Strong()
        self.replaceWith(strong)
        strong.addChildElement(self)
        strong.addChildElementsTo = self

    def addEmphasis(self):
        """
            wraps into an emphasis tag - requires parent element to be defined
        """
        emphasis = DOM.Em()
        self.replaceWith(emphasis)
        emphasis.addChildElement(self)
        emphasis.addChildElementsTo = self

Factory.addProduct(Label)


class Paragraph(Label):
    """
        Defines a paragraph element
    """
    __slots__ = ()
    tagName = "p"

Factory.addProduct(Paragraph)


class Subscript(Label):
    """
        Defines a subscripted text element
    """
    __slots__ = ()
    tagName = "sub"

Factory.addProduct(Subscript)


class Superscript(Label):
    """
        Defines a superscripted text element
    """
    __slots__ = ()
    tagName = "sup"

Factory.addProduct(Superscript)


class PreformattedText(Label):
    """
        Defines a preformatted text label, where no forced format should be applied (such as single space)
    """
    __slots__ = ()
    tagName = "pre"

Factory.addProduct(PreformattedText)


class HeaderLabel(Label):
    """
        Defined a heading (h1-h6) label
    """
    __slots__ = ('level')
    properties = Label.properties.copy()
    properties['level'] = {'action':'classAttribute', 'type':'int'}

    def __init__(self, id=None, name=None, parent=None):
        Label.__init__(self, id, name, parent=parent)
        self.level = 2

    def toHtml(self, formatted=False):
        self.level = int(self.level)
        if self.level > 6 or self.level < 1:
            raise ValueError("Valid levels for headers are 1-6 (h1-6)")

        self._tagName = "h%d" % self.level
        return Label.toHtml(self, formatted)

Factory.addProduct(HeaderLabel)


class FreeText(Label):
    """
        A Free text element is a label without a border
    """
    __slots__ = ()
    tagName = ''

Factory.addProduct(FreeText)


class LabeledData(Label):
    """
        Defines a label data pair, where the value type is defined by the label
    """
    __slots__ = ('__data__', )

    properties = Base.WebElement.properties.copy()
    properties['label'] = {'action':'setText'}
    properties['data'] = {'action':'setData'}

    def __init__(self, id=None, name=None, parent=None, label=""):
        Label.__init__(self, id, name, parent=parent)
        self.style['vertical-align'] = "middle"
        self.__data__ = self.addChildElement(Label)
        self.__data__.addClass('WDataLabeled')
        self.setText(label)
        self.addClass("WLabeledData")

    def setData(self, data):
        """
            Sets the displayed data
        """
        return self.__data__.setText(data)

    def data(self):
        """
            Returns the displayed data
        """
        return self.__data__.text()

Factory.addProduct(LabeledData)


class Error(Label):
    """
        Defines an error webElement
    """
    __slots__ = ()
    tagName = "div"

    def __init__(self, id=None, name=None, parent=None):
        Label.__init__(self, id, name, parent)

Factory.addProduct(Error)


class FormError(Label):
    """
        Defines a '<form:error>' web element, which is used by formencode, or dynamics forms error processor to
        know where to place an error when present
    """
    __slots__ = ()
    displayable = False
    tagName = 'form:error'
    tagSelfCloses = True

    def __init__(self, id=None, name=None, parent=None):
        if id and not name:
            name = id or "ErrorGettingName"
            id = None

        Label.__init__(self, id, name, parent)

    def setError(self, errorText):
        """
            Sets the error text
        """
        self._tagName = "span"
        self.addClass("error-message")
        self.tagSelfCloses = False
        if not getattr(self, '_textNode', None):
            self.textNode = Base.TextNode()
        self._textNode.setText(errorText)

    def shown(self):
        """
            Form Errors are never visible but only replaced
        """
        return False

Factory.addProduct(FormError)


class BlankRendered(Base.WebElement):
    """
        Outupts nothing but still renders child elements
    """
    __slots__ = ()
    displayable = False

    def toHtml(self, formatted=False):
        Base.WebElement.toHtml(self, False)
        return ""

    def shown(self):
        return False

Factory.addProduct(BlankRendered)


class Empty(Base.WebElement):
    """
        Outputs nothing to the page -- a useful placeholder
    """
    __slots__ = ()
    displayable = False

    def __init__(self, name=None, id=None, parent=None):
        Base.WebElement.__init__(self, None, None, parent)

    def toHtml(self, formatted=False):
        return ""

    def shown(self):
        return False

Factory.addProduct(Empty)


class HTML(Base.WebElement):
    """
        Simply displays the html as it is given
    """
    __slots__ = ('html')
    properties = Base.WebElement.properties.copy()
    properties['html'] = {'action':'classAttribute'}

    def __init__(self, name=None, id=None, parent=None, html=""):
        Base.WebElement.__init__(self, None, None, parent)

        self.html = html

    def toHtml(self, formatted=False):
        return self.html

Factory.addProduct(HTML)


class StatusIndicator(Base.WebElement):
    """
        Shows a visual indication of status from incomplete to complete
    """
    __slots__ = ('status')
    statuses = ['StatusIncomplete', 'StatusPartial', 'StatusComplete']
    Incomplete = 0
    Partial = 1
    Complete = 2

    tagName = "div"
    properties = Base.WebElement.properties.copy()
    properties['setStatus'] = {'action':'setStatus', 'type':'int'}

    def __init__(self, name=None, id=None, parent=None):
        Base.WebElement.__init__(self, name=name, id=id, parent=parent)
        self.setStatus(StatusIndicator.Incomplete)
        self.style['height'] = "100%"
        self.addClass('hidePrint')
        self.addClass('WStatusIndicator')

    def setStatus(self, status):
        """
            Sets the current displayed status
        """
        self.status = int(status)
        statusClass = self.statuses[self.status]
        self.chooseClass(self.statuses, statusClass)

Factory.addProduct(StatusIndicator)


class CacheElement(Base.WebElement):
    """
        Renders an element once caches the result and returns the cache every time after
    """
    __slots__ = ('__cachedHTML__')

    def __init__(self, id=None, name=None, parent=None):
        Base.WebElement.__init__(self, id, name, parent)
        self.__cachedHTML__ = None

    def toHtml(self, formatted=False):
        if self.__cachedHTML__ == None:
            self.__cachedHTML__ = Base.WebElement.toHtml(self, formatted)
        return self.__cachedHTML__

Factory.addProduct(CacheElement)
