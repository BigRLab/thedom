#!/usr/bin/python
"""
   Name:
       Inputs

   Description:
       Contains Elements that make data entry easy by providing reusable input elements

"""

import types

import Base
import DictUtils
import Factory
from MethodUtils import CallBack
from StringUtils import interpretAsString

Factory = Factory.Factory("Inputs")


class ValueElement(Base.WebElement):
    """
        Defines a base value containing WebElement
    """
    __slots__ = ('key', '_value')
    signals = Base.WebElement.signals + ['valueChanged']
    properties = Base.WebElement.properties.copy()
    properties['text'] = {'action':'setValue'}
    properties['value'] = {'action':'setValue'}
    properties['tabindex'] = {'action':'attribute'}
    properties['onchange'] = {'action':'javascriptEvent'}
    properties['onclick'] = {'action':'javascriptEvent'}
    properties['onblur'] = {'action':'javascriptEvent'}

    def __init__(self, id, name=None, parent=None, key=None):
        Base.WebElement.__init__(self, id, name, parent)
        self.key = key
        self._value = ''
        self.attributes['value'] = CallBack(self, 'value')

    def insertVariables(self, variableDict=None):
        """
            Updates the value based on a dictionary, popping it out afterwards
        """
        if variableDict == None:
            variableDict = {}

        Base.WebElement.insertVariables(self, variableDict)

        value = None
        removeFromDictionary = True
        if self.key:
            value = DictUtils.getNestedValue(variableDict, self.key)
        if self.fullId() and value == None:
            value = variableDict.get(self.fullId(), None)
            if value and type(value) in (types.ListType, types.TupleType):
                if len(value) > 1:
                    removeFromDictionary = False
                value = value.pop(0)
        if self.id and value == None:
            value = variableDict.get(self.id, None)
            if value and type(value) in (types.ListType, types.TupleType):
                if len(value) > 1:
                    removeFromDictionary = False
                value = value.pop(0)
        if self.name and value == None:
            value = variableDict.get(self.fullName(), None)
            if value == None:
                value = variableDict.get(self.name, None)

            if value and type(value) in (types.ListType, types.TupleType):
                if len(value) > 1:
                    removeFromDictionary = False
                value = value.pop(0)
        if value != None:
            self.setValue(value)

        if removeFromDictionary:
            self._removeFromDictionary(variableDict)

    def _removeFromDictionary(self, dictionary):
        for key in [self.id, self.name, self.fullId(), self.fullName()]:
            dictionary.pop(key, False)

    def exportVariables(self, exportedVariables=None, flat=False):
        """
            return the used webelements variables as a dictionary
        """
        if exportedVariables == None:
            exportedVariables = {}

        if flat:
            if self.name:
                prevValue = exportedVariables.get(self.name, None)
                if type(prevValue) == list:
                    prevValue.append(self.value)
                elif prevValue != None:
                    exportedVariables[self.name] = [prevValue, self.value()]
                else:
                    exportedVariables[self.name] = self.value()
            elif self.id:
                exportedVariables[self.id] = self.value()
        else:
            if self.key:
                DictUtils.setNestedValue(exportedVariables, self.key, self.value())

        Base.WebElement.exportVariables(self, exportedVariables, flat)
        return exportedVariables

    def setValue(self, value):
        """
            Sets the value associated with the element
        """
        if value != self._value:
            self._value = value
            self.emit('valueChanged', value)

    def value(self):
        """
            Returns the value associated with the element
        """
        return self._value


class InputElement(ValueElement):
    """
        Defines a base '<input>' webelement
    """
    __slots__ = ()
    tagName = "input"
    tagSelfCloses = True
    allowsChildren = False

    def __init__(self, id, name=None, parent=None, key=None):
        ValueElement.__init__(self, id, name, parent, key=key)

        self.connect('beforeToHtml', None, self, '_updateReadOnly_')

    def _updateReadOnly_(self):
        """
            Update readonly attribute to reflect editable status
        """
        if not self.editable():
            self.attributes['readonly'] = 'readonly'

    def setDisabledJs(self, disabled):
        '''
        Returns javascript to disable this input clientside
        '''
        return 'WEGetElement(\'%s\').disabled = %s;' % (self.id, str(disabled))


class CheckBox(InputElement):
    """
        Defines a checkbox '<input type="checkbox">' webelement
    """
    __slots__ = ()
    properties = InputElement.properties.copy()
    properties['valueAttribute'] = {'action':'setValueAttributeFromString'}

    def __init__(self, id=None, name=None, parent=None, key=None):
        InputElement.__init__(self, id, name, parent, key=key)

        self._value = False
        self.attributes['value'] = None
        self.attributes['type'] = 'checkbox'
        self.attributes['disabled'] = CallBack(self, 'disabled')

    def disabled(self):
        """
            Returns true if the checkbox is set to non editable
        """
        if self.editable():
            return None
        else:
            return True

    def setValue(self, value):
        """
            Sets the checkbox to a True or False value
        """
        if value == "False":
            value = False
        elif value == "True":
            value = True

        if value and not self.value() == True:
            InputElement.setValue(self, True)
            self.attributes['checked'] = 'on'
        elif (not value) and self.value() == True:
            self.attributes['checked'] = None
            InputElement.setValue(self, False)

    def insertVariables(self, fieldDict=None):
        if self.editable():
            self.setValue(False)
        return InputElement.insertVariables(self, fieldDict)

    def setCheckedJs(self, checked):
        '''
        Return javascript to check/uncheck the checkbox.
        '''
        return 'WEGetElement(\'%s\').checked = %s' % (self.id, str(checked))

    def setValueAttributeFromString(self, value):
        '''
        Sets the value attribute for the checkbox,
        (not to be confused with checked/unchecked state).
        '''
        self.attributes['value'] = value

Factory.addProduct(CheckBox)


class Radio(CheckBox):
    """
        Defines a base radio webElement:
        where the name represents the radio group identifier and the id reperents the individual
        radio buttons identifier
    """
    __slots__ = ()
    def __init__(self, id=None, name=None, parent=None, key=None):
        CheckBox.__init__(self, id, name, parent, key=key)
        self.attributes['type'] = "radio"
        self.setId(id)

    def insertVariables(self, variableDict=None):
        if variableDict == None:
            variableDict = {}

        selected = variableDict.get(self.fullName(), variableDict.get(self.name, None))
        if selected == self.id:
            self.setValue(True)
            self._removeFromDictionary(variableDict)
        else:
            self.setValue(False)

    def setId(self, value):
        """
            Sets the radios value and id
        """
        self.attributes['value'] = value
        self.id = value

Factory.addProduct(Radio)


class TextBox(InputElement):
    """
        Defines a textbox '<input>' webelement
    """
    __slots__ = ('length', )
    properties = InputElement.properties.copy()
    properties['size'] = {'action':'attribute'}
    properties['maxlength'] = {'action':'attribute'}
    properties['password'] = {'action':'setIsPassword', 'type':'bool'}
    properties['autocomplete'] = {'action':'attribute'}
    properties['onkeydown'] = {'action' : 'javascriptEvent' }
    properties['onkeyup'] = {'action' : 'javascriptEvent' }

    def __init__(self, id, name=None, parent=None, key=None):
        InputElement.__init__(self, id, name, parent, key)
        self.attributes['type'] = 'text'
        self.length = None

    def setIsPassword(self, isPassword):
        """
            If set to true '*'s will replace normal text while a user is typing
        """
        if isPassword:
            self.attributes['type'] = 'password'

    def isPassword(self):
        """
            Returns true if the textbox is in password input mode
        """
        return self.attributes['type'] == 'password'

    def jsSelectAll(self, id=None):
        """
            Returns the javascript to select all the text in the textbox clientside
        """
        return """textBox = WEGetElement('""" + (id or self.id) + """');
                  textBox.focus();
                  textBox.select();"""

Factory.addProduct(TextBox)


class IntegerTextBox(TextBox):
    """
        Defines a textbox '<input>' webelement that can only contain integer values
    """
    __slots__ = ('maximum', 'minimum')
    properties = TextBox.properties.copy()
    properties['maximum'] = {'action':'classAttribute', 'type':'int'}
    properties['minimum'] = {'action':'classAttribute', 'type':'int'}

    def __init__(self, id, name=None, parent=None, key=None):
        TextBox.__init__(self, id, name, parent, key)
        self.maximum = None
        self.minimum = None
        self.attributes['size'] = '4'
        self.setValue(0)

    def setValue(self, value):
        """
            Sets the integer value of the input
        """
        if value is None:
            return TextBox.setValue(self, None)

        try:
            value = int(value)
        except ValueError:
            value = 0

        if self.maximum is not None:
            maximum = int(self.maximum)
            if value > maximum:
                value = maximum
        if self.minimum is not None:
            minimum = int(self.minimum)
            if value < minimum:
                value = minimum

        return TextBox.setValue(self, value)

    def value(self):
        """
            Returns the integer value of the input
        """
        value = TextBox.value(self)
        if value is None:
            return value
        return int(value)

Factory.addProduct(IntegerTextBox)


class FileUpload(InputElement):
    """
        An input for uploading files to the server
    """
    __slots__ = ()
    properties = InputElement.properties.copy()
    properties['size'] = {'action':'attribute'}
    properties['maxlength'] = {'action':'attribute'}

    def __init__(self, id, name=None, parent=None, key=None):
        InputElement.__init__(self, id, name, parent, key=key)

        self.attributes['type'] = "file"

Factory.addProduct(FileUpload)


class TextArea(ValueElement):
    """
        Defines a <textarea> webelement (A multi line textbox)
    """
    __slots__ = ()
    tagName = "textarea"
    allowsChildren = False
    properties = ValueElement.properties.copy()
    properties['cols'] = {'action':'attribute'}
    properties['rows'] = {'action':'attribute'}
    properties['wrap'] = {'action':'attribute'}
    properties['onkeydown'] = {'action':'javascriptEvent'}

    def __init__(self, id, name=None, parent=None, key=None):
        ValueElement.__init__(self, id, name, parent, key=key)

    def content(self, formatted=False):
        return self.value() or ""

    def toHtml(self, formatted=False):
        if not self.editable():
            self.attributes['readonly'] = 'readonly'

        return ValueElement.toHtml(self)

Factory.addProduct(TextArea)

class Option(ValueElement):
    """
        Defines a select '<option>' webelement
    """
    __slots__ = ('_selected', '_textNode')
    tagName = "option"
    signals = ValueElement.signals + ['selected', 'unselected']
    properties = ValueElement.properties.copy()
    properties['select'] = {'action':'call'}
    properties['selected'] = {'action':'setSelected', 'type':'bool'}
    properties['text'] = {'action':'setText'}

    def __init__(self, id=None, name=None, parent=None, key=None):
        ValueElement.__init__(self, id, name, parent, key=key)

        self._selected = False
        self._textNode = self.addChildElement(Base.TextNode())

    def selected(self):
        """
            Returns True if the option has been selected
        """
        return self._selected

    def setSelected(self, selected):
        """
            Selects or unselects the option
        """
        if selected:
            self.select()
        else:
            self.unselect()

    def select(self):
        """
            Selects the option
        """
        self._selected = True
        self.attributes['selected'] = True
        self.emit('selected')

    def unselect(self):
        """
            Unselects the option
        """
        self._selected = False
        self.attributes['selected'] = None
        self.emit('unselected')

    def setText(self, text):
        """
            Sets the displayed text of the option
        """
        self._textNode.setText(text)

    def text(self):
        """
            Returns the displayed text of the option
        """
        return self._textNode.text()

Factory.addProduct(Option)


class Select(ValueElement):
    """
        Provides a way to let a user choose one out of several options
    """
    __slots__ = ()
    tagName = "select"
    properties = ValueElement.properties.copy()
    properties['multiple'] = {'action':'attribute', 'type':'bool'}
    signals = ValueElement.signals + ['selectionChanged']

    def __init__(self, id, name=None, parent=None):
        ValueElement.__init__(self, id, name, parent)

        self.connect('beforeToHtml', None, self, '_updateReadOnly_')

    def _updateReadOnly_(self):
        if not self.editable():
            self.attributes['disabled'] = 'True'

    def addOptions(self, options, displayKeys=False):
        """
            Adds a group of options to a select box:

            options - Takes a dictonary of option keys to option values
                      or a straight list of option names

            displayKeys(False) - if dictionaries keys will be used for display and the values
                                 will be used for keys
        """
        if isinstance(options, dict):
            for key, value in options.iteritems():
                self.addOption(key, value, displayKeys)
        else:
            for option in options:
                if type(option) == tuple:
                    self.addOption(option[0], option[1])
                else:
                    self.addOption(option)

    def addOptionList(self, options, displayKeys=True):
        """
            Adds a options based on a list of tuple(key-value) pairs
        """
        for option in options:
            name = option['name']
            value = option['value']
            self.addOption(name, value, displayKeys)

    def addOption(self, key, value=None, displayKeys=True):
        """
            Adds options based on a key-value dictionary
        """
        newOption = Option()
        if not value:
            value = key

        key = interpretAsString(key)
        value = interpretAsString(value)
        if displayKeys:
            newOption.setValue(value)
            newOption.setText(key)
        else:
            newOption.setValue(key)
            newOption.setText(value)

        newOption.connect('selected', None, self, 'emit', 'selectionChanged')
        return self.addChildElement(newOption)

    def options(self):
        """
            Returns all options within the selectbox
        """
        options = {}
        for option in self.childElements:
            options[option.value()] = option.text()

        return options

    def selected(self):
        """
            Returns the selected options on the select box
        """
        for option in self.childElements:
            if option.selected():
                return option

    def setValue(self, value):
        """
            Selects a child select option
        """
        strValue = interpretAsString(value)
        for obj in self.childElements:
            if strValue and ((obj.fullId() == strValue) or (str(obj.value()) == strValue) or
                             (obj._textNode.text() == strValue)):
                obj.select()
            else:
                obj.unselect()

    def value(self):
        """
            Returns the selected options value
        """
        for option in self.childElements:
            if option.selected():
                return option.value()
        if self.childElements:
            return self.childElements[0].value()

Factory.addProduct(Select)


class MultiSelect(Select):
    """
        Provides a way for a user to select a portion of several choices
    """
    __slots__ = ()

    def __init__(self, id, name=None, parent=None):
        Select.__init__(self, id, name, parent)
        self.attributes['multiple'] = True

    def selected(self):
        """
            Returns all selected options
        """
        selected = []
        for option in self.childElements:
            if option.selected():
                selected.append(option)

        return selected

    def value(self):
        """
            Returns a list of the values associated with each selected option
        """
        values = []
        for option in self.childElements:
            if option.selected():
                values.append(option.value())

        return values

    def setValue(self, value):
        """
            Selects a child select option
        """
        if type(value) in types.StringTypes:
            value = [value]

        for obj in self.childElements:
            if (obj.fullId() in value) or (str(obj.value()) in value) or \
                (obj._textNode.text() in value):
                obj.select()
            else:
                obj.unselect()

    def insertVariables(self, variableDict=None):
        if variableDict == None:
            variableDict = {}

        value = None
        if self.key:
            value = DictUtils.getNestedValue(variableDict, self.key)
        if self.fullId() and value == None:
            value = variableDict.get(self.fullId(), None)
        if self.id and value == None:
            value = variableDict.get(self.id, None)
        if self.name and value == None:
            value = variableDict.get(self.fullName(), None)
        if value != None:
            self.setValue(value)

        self._removeFromDictionary(variableDict)

Factory.addProduct(MultiSelect)
