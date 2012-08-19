#!/usr/bin/python
"""
   Name:
       Fields

   Description:
       Complex input elements

"""

import operator
import types

import Base
import Buttons
import Display
import Factory
import HiddenInputs
import Inputs
import Layout
import ToClientSide
import UITemplate
from Factory import Composite
from MethodUtils import CallBack
from StringUtils import interpretAsString, listReplace

Factory = Factory.Factory(Base.Invalid, name="Fields")

class BaseField(Layout.Box):
    """
        Base field implementation where a field is defined as:
            a label, input, and validator paired together
    """
    inputElement = None
    properties = Base.WebElement.properties.copy()
    Base.addChildProperties(properties, Display.Label, 'label')
    properties['labelContainerStyle'] = {'action':'labelContainer.setStyleFromString'}
    properties['text'] = {'action':'setText'}
    properties['setApart'] = {'action':'call', 'type':'bool'}
    properties['value'] = {'action':'setValue'}
    properties['labelStyle'] = {'action':'label.setStyleFromString'}
    properties['inputStyle'] = {'action':'userInput.setStyleFromString'}
    properties['required'] = {'action' : 'call' , 'name' : 'setRequired', 'type':'bool'}
    properties['key'] = {'action':'userInput.classAttribute'}
    properties['submitIfDisabled'] = {'action':'setSubmitIfDisabled', 'type':'bool'}
    properties['flip'] = {'action':'call', 'type':'bool'}

    def __init__(self, id, name=None, parent=None):
        Layout.Box.__init__(self, id + "Field", name, parent)
        self.submitIfDisabled = False

        self.layout = self.addChildElement(Layout.Vertical(id + "Container"))
        self.inputContainer = self.layout.addChildElement(Layout.Horizontal())

        self.label = self.inputContainer.addChildElement(Display.Label())

        self.inputAndActions = self.inputContainer.addChildElement(Layout.Horizontal())
        self.userInput = self.inputAndActions.addChildElement(self.inputElement(id, name=name))
        self.fieldActions = self.inputAndActions.addChildElement(Layout.Box())
        self.addChildElementsTo = self.fieldActions

        errorContainer = self.layout.addChildElement(Layout.Horizontal())
        self.formError = errorContainer.addChildElement(Display.FormError(id, parent=self))
        self.layout.addChildElement(errorContainer)

        self.connect('beforeToHtml', None, self, '__checkIfNeedsValidation__')
        self.connect('beforeToHtml', None, self, '__updateReadOnly__')

    def flip(self):
        self.inputAndActions.replaceWith(self.label)
        self.label.replaceWith(self.inputAndActions)

    def __checkIfNeedsValidation__(self):
        if not self.formError.name:
            self.formError.remove()

    def __updateReadOnly__(self):
        if not self.editable() and self.submitIfDisabled:
            # Creates a hidden input for a disabled field so that the field value
            # is still submitted even if the field is set as read-only
            value = self.value()
            if type(value) != types.ListType:
                value = [value,]
            for val in value:
                hiddenValue = HiddenInputs.HiddenValue(name=self.name)
                hiddenValue.setValue(val)
                self.addChildElement(hiddenValue)

    def setSubmitIfDisabled(self, submit):
        """
            If set to true the value will still be passed through on a submit even if the field is disabled
        """
        self.submitIfDisabled = submit

    def changeId(self, newId):
        """
            Updates the id for not only the field but the associated userInput and formError
        """
        self.userInput.id = newId
        self.userInput.name = newId
        self.formError.name = newId
        self.id = newId + "Field"

    def validators(self, useFullId=True):
        """
            Returns the validators associated with the field
        """
        validators = Layout.Box.validators(self, useFullId=useFullId)
        if useFullId:
            validators.pop(self.fullId(), None)
        else:
            validators.pop(self.id, None)

        validator = getattr(self, 'validator', None)
        if self.editable() and self.shown() and validator:
            if useFullId:
                id = self.userInput.fullId()
            else:
                id = self.userInput.id
            validators[id] = validator

        return validators

    def setRequired(self):
        """
            Sets the field to required and changes the display to communicate that to the user
        """
        label = Display.Label()
        label.addClass("Required")
        label.setText('*')
        self.userInput.addClass("RequiredField")
        self.label.addChildElement(label)

    def setValue(self, value):
        """
            Sets the value for the fields input element
        """
        self.userInput.setValue(value)

    def value(self):
        """
            Returns the value set on the input element of the field
        """
        return self.userInput.value()

    def setText(self, text):
        """
            Sets the displayed text associated with the field
        """
        self.label.setText(text)

    def text(self):
        """
            Returns the displayed text associated with the field
        """
        return self.label.text()

    def setApart(self):
        """
            Moves the label and field away from each other (seperated as far left-right as possible)
        """
        self.inputAndActions.parent.style['float'] = 'right'
        self.formError.parent.style['float'] = 'right'

class TextField(BaseField):
    """
        A field with a textbox as the input
    """
    inputElement = Inputs.TextBox
    properties = BaseField.properties.copy()
    Base.addChildProperties(properties, Inputs.TextBox, 'userInput')

Factory.addProduct(TextField)


class RadioField(BaseField):
    """
        A field with a radio button as the input
    """
    inputElement = Inputs.Radio
    properties = BaseField.properties.copy()
    Base.addChildProperties(properties, Inputs.Radio, 'userInput')

    def __updateReadOnly__(self):
        # Only create the hidden input if the original radio button is selected to simulate
        # how an actual radio control would work
        if not self.editable() and self.submitIfDisabled and self.value():
            hiddenValue = HiddenInputs.HiddenValue(name=self.name)
            hiddenValue.setValue(self.userInput.id)
            self.addChildElement(hiddenValue)

    def setId(self, value):
        """
            Sets the id of the userInput
        """
        self.userInput.setId(value)

    def setName(self, value):
        """
            Sets the name of the userInput
        """
        self.userInput.setName(value)

    def selectJs(self):
        '''
        Returns the javascript to select this option clientside.
        The element's id must be set.
        '''
        return "document.getElementById('%s').checked=true;" % self.userInput.id

Factory.addProduct(RadioField)


class TextAreaField(BaseField):
    """
        A field with a textarea as the input
    """
    inputElement = Inputs.TextArea
    properties = BaseField.properties.copy()
    Base.addChildProperties(properties, Inputs.TextArea, 'userInput')

Factory.addProduct(TextAreaField)


class AutoField(Layout.Vertical):
    """
        Allows you to use any input element as a field (text label, inputElement, validator pair)
        simply by adding it as a childElement
    """
    properties = Base.WebElement.properties.copy()
    properties['text'] = {'action':'setText'}
    properties['setApart'] = {'action':'call', 'type':'bool'}
    properties['value'] = {'action':'setValue'}

    def __init__(self, id, name=None, parent=None):
        Layout.Vertical.__init__(self, id, name, parent=parent)

        self.inputContainer = self.addChildElement(Layout.Horizontal())

        self.label = self.inputContainer.addChildElement(Display.Label())
        self.fieldActions = self.inputContainer.addChildElement(Layout.Box())
        self.addChildElementsTo = self.fieldActions
        self.userInput = self.inputContainer.addChildElement(Base.Invalid())

        errorContainer = self.addChildElement(Layout.Horizontal())
        self.formError = errorContainer.addChildElement(Display.FormError(id, parent=self))

    def exportVariables(self, exportedVariables=None, flat=False):
        if not self.userInput.key and self.key:
            self.userInput.key = self.key
            self.key = None

        Layout.Vertical.exportVariables(self, exportedVariables, flat)

    def setValue(self, value):
        """
            Sets the input elements value
        """
        self.userInput.setValue(value)

    def value(self):
        """
            Returns the input elements value
        """
        return self.userInput.value()

    def setText(self, text):
        """
            Sets the text displayed on the fields label
        """
        self.label.setText(text)

    def text(self):
        """
            Returns the text that will be displayed on the fields label
        """
        return self.label.text()

    def setApart(self):
        """
            Moves the input as far right (away from the label) as possible
        """
        self.inputContainer.style['float'] = 'right'

    def setInputElement(self, element):
        """
            Sets the input element for the field
        """
        self.userInput = self.userInput.replaceWith(element)
        self.formError.name = self.userInput.name or self.userInput.id
        return self.userInput

    def addChildElement(self, childElement, style=None):
        if (isinstance(childElement, Inputs.ValueElement) or hasattr(childElement, 'userInput')) and type(self.userInput) == Base.Invalid:
            return self.setInputElement(childElement)
        else:
            return Layout.Vertical.addChildElement(self, childElement, style)


Factory.addProduct(AutoField)


class SelectField(BaseField):
    """
        A field with a select box as the input
    """
    inputElement = Inputs.Select
    properties = BaseField.properties.copy()
    Base.addChildProperties(properties, Inputs.Select, 'userInput')

    def __init__(self, id, name=None, parent=None):
        self.fieldActions = None
        BaseField.__init__(self, id, name, parent)
        self.addChildElementsTo = self

    def addChildElement(self, childElement):
        if isinstance(childElement, Inputs.Option):
            return self.userInput.addChildElement(childElement)
        elif self.fieldActions:
            return self.fieldActions.addChildElement(childElement)
        return BaseField.addChildElement(self, childElement)

    def addOptions(self, dictionary, displayKeys=False):
        """
            Adds options to the fields select box where the options are passed in as a dictionary of id-value pairs.
        """
        return self.userInput.addOptions(dictionary, displayKeys)

    def addOptionList(self, options, displayKeys=True):
        """
            Adds options to the fields select box where the options are passed in as a list of tuples of id-value pairs.
        """
        return self.userInput.addOptionList(options, displayKeys=displayKeys)

    def addOption(self, key, value=None, displayKeys=True):
        """
            Adds a single option the fields select box, based on key/value
        """
        return self.userInput.addOption(key, value=value, displayKeys=displayKeys)

    def options(self):
        """
            Returns a list of available options associated with the fields select box
        """
        return self.userInput.options()

    def selected(self):
        """
            Returns all selected options
        """
        return self.userInput.selected()

Factory.addProduct(SelectField)

@ToClientSide.Convert
class MultiFieldClientSide(object):

    def removeSelectedOption(self, button, sortBy):
        selectionBox = JUFellowChild(button, 'multiField', 'selectionBox')
        hiddenMultiSelect = JUFellowChild(button, 'multiField', 'hiddenMultiSelectionField')
        shownOption = JUGetElementByClassName('valueSelected', button.parentNode)
        hiddenOption = JUGetElementByInnerHTML(hiddenMultiSelect, shownOption.innerHTML)
        JUAddOption(selectionBox, hiddenOption.innerHTML, hiddenOption.value)
        JURemoveElement(button.parentNode)
        JURemoveElement(hiddenOption)
        if sortBy == "innerHTML":
            JUSortSelect(selectionBox)
        elif sortBy == "value":
            JUSortSelectByValue(selectionBox)

    def addSelectedOption(self, selectBox):
        shownSelection = JUFellowChild(selectBox, 'multiField', 'selectContainer')
        hiddenMultiSelect = JUFellowChild(selectBox, 'multiField', 'hiddenMultiSelectionField')
        selected = JUSelectedOption(selectBox)
        shownSelection.innerHTML += JUUnserialize('%s')
        JUAddOption(hiddenMultiSelect, selected.innerHTML, selected.value)
        JUSelectOption(selectBox, ' ')
        JURemoveElement(selected)
        JUSelectAllOptions(hiddenMultiSelect)

class MultiField(SelectField):
    """
        The multifield is a multi select field, where each individual option is selected in the same mannor
        as a normal select field to make it more intuitive for users
    """
    properties = SelectField.properties.copy()
    properties['validator'] = {'action': 'hiddenMultiSelect.classAttribute', 'name': 'validator'}
    properties['sortBy'] = {'action': 'classAttribute'}
    def __createNewSelection__(self, name):
        new = Layout.Horizontal()
        new.addClass('WSelectedMultiOption')
        label = new.addChildElement(Display.Label())
        label.setText(name)
        label.style['overflow'] = 'hidden'
        label.attributes['title'] = name
        label.addClass('valueSelected')
        remove = new.addChildElement(Buttons.Button())
        remove.setText("Remove")
        remove.name = "MultiFieldRemove" + name
        remove.addJavascriptEvent('onclick', 'multiField.removeSelectedOption(this, "%s");' % self.sortBy)

        return new

    def __init__(self, id, name=None, parent=None):
        SelectField.__init__(self, id, name, parent)
        self.sortBy = "innerHTML"
        self.userInput.id = id + "MultiField"
        self.userInput.name = (name or id) + "MultiField"

        self.selectContainer = self.addChildElement(Layout.Vertical())
        self.hiddenMultiSelect = self.addChildElement(Inputs.MultiSelect(id))
        self.hiddenMultiSelect.hide()
        self.hiddenMultiSelect.addClass('hiddenMultiSelectionField')
        self.selectContainer.addClass('selectContainer')
        self.userInput.addClass('selectionBox')
        self.userInput.addOption(' Click to add', ' ')
        self.addClass('multiField')

        self.userInput.addClientSideEvent('onChange', 'multiField.addSelectedOption(this)')

        self.connect('beforeToHtml', None,  self, 'sort')

    def sort(self):
        """
            Sorts the options list based on the key value
        """
        self.userInput.childElements.sort(key=Inputs.Option.value)

    def loadFromDictionary(self, valueDict):
        SelectField.loadFromDictionary(self, valueDict)

        new = self.__createNewSelection__("' + selected.innerHTML + '")
        self.addScript(str(MultiFieldClientSide) % listReplace(new.toHtml(), ('"', '<', '>'), ('\\"', '&lt;', '&gt;')))
        self.runClientSide("multiField = MultiFieldClientSide()")

    def insertVariables(self, valueDict=None):
        """
            Overrides the insertVariable call to create the new selection objects and populate the hidden multiselect
        """
        if valueDict == None: valueDict = {}
        selectedOptions = valueDict.pop(self.hiddenMultiSelect.id, [])
        if type(selectedOptions) != list:
            selectedOptions = [selectedOptions]

        for option in selectedOptions:
            optionObject = self.userInput.query().filter(_value=option)[0]
            optionObject.select()
            self.hiddenMultiSelect.addChildElement(optionObject)
            self.selectContainer.addChildElement(self.__createNewSelection__(optionObject.text()))

        return SelectField.insertVariables(self, valueDict)

Factory.addProduct(MultiField)

class MultiSelectField(BaseField):
    """
        A field with a multiselect as the input
    """
    inputElement = Inputs.MultiSelect
    properties = BaseField.properties.copy()
    Base.addChildProperties(properties, Inputs.MultiSelect, 'userInput')

    def __init__(self, id, name=None, parent=None):
        self.fieldActions = None
        BaseField.__init__(self, id, name, parent)
        self.addChildElementsTo = self
        self.userInput.attributes['multiple'] = True

    def addChildElement(self, childElement):
        if isinstance(childElement, Inputs.Option):
            return self.userInput.addChildElement(childElement)
        elif self.fieldActions:
            return self.fieldActions.addChildElement(childElement)
        return BaseField.addChildElement(self, childElement)

    def addOptions(self, dictionary, displayKeys=False):
        """
            Adds options to the fields select box where the options are passed in as a dictionary of id-value pairs.
        """
        return self.userInput.addOptions(dictionary, displayKeys)

    def addOptionList(self, options, displayKeys=True):
        """
            Adds options to the fields select box where the options are passed in as a list of tuples of id-value pairs.
        """
        return self.userInput.addOptionList(options, displayKeys=displayKeys)

    def addOption(self, key, value=None, displayKeys=True):
        """
            Adds a single option the fields select box, based on key/value
        """
        return self.userInput.addOption(key, value=value, displayKeys=displayKeys)

    def options(self):
        """
            Returns a list of available options associated with the fields select box
        """
        return self.userInput.options()

    def selected(self):
        """
            Returns all selected options
        """
        return self.userInput.selected()

Factory.addProduct(MultiSelectField)

class CheckboxField(BaseField):
    """
        A field with a checkbox as the input
    """
    properties = BaseField.properties.copy()
    Base.addChildProperties(properties, Inputs.CheckBox, 'userInput')
    properties['checked'] = {'action':'setValue', 'type':'bool'}
    inputElement = Inputs.CheckBox

    def __init__(self, id, name=None, parent=None, key=None):
        BaseField.__init__(self, id, name, parent)
        self.key = key

        inputContainer = Layout.Box(id + "_inputContainer", '', self)
        inputContainer.style['float'] = 'left'
        inputContainer.style['clear'] = 'none'
        userInput = Inputs.CheckBox(id, None, self, key=key)
        self.userInput.addJavascriptEvent('onload', 'CCClickCheckbox(this)')
        self.userInput.addJavascriptEvent('onclick', CallBack(self, 'toggleChildren'))
        self.userInput = self.userInput.replaceWith(userInput)
        self.inputContainer = self.addChildElement(inputContainer)

        labelContainer = Layout.Box(id + "_labelContainer", '', self)
        labelContainer.style['float'] = 'left'
        labelContainer.style['clear'] = 'none'
        labelContainer.style['margin-top'] = "3px"
        label = Display.Label(id + "_label", '' , self)
        self.label = labelContainer.addChildElement(label)
        self.labelContainer = self.addChildElement(labelContainer)

        self.addChildElement(Layout.LineBreak())

        childContainer = Layout.Box(id + "_childContainer", name, self)
        childContainer.style['display'] = CallBack(self, 'displayValue')
        self.childContainer = self.addChildElement(childContainer)
        self.addChildElementsTo = childContainer

    def __updateReadOnly__(self):
        # Only create the hidden input if the original checkbox is checked to simulate
        # how an actual checkbox control would work
        if not self.editable() and self.submitIfDisabled and self.value():
            hiddenValue = HiddenInputs.HiddenValue(name=self.name)
            hiddenValue.setValue('on')
            self.addChildElement(hiddenValue)

    def loadFromDictionary(self, valueDict):
        BaseField.loadFromDictionary(self, valueDict)
        if self.key:
            self.userInput.key = self.key
            self.key = None

    def setValue(self, value):
        """
            Sets the value on the checkbox
        """
        self.userInput.setValue(value)

    def displayValue(self):
        """
            Returns the css display value for the checkbox field children
        """
        if not self.userInput.value():
            return 'none'

        return 'block'

    def toggleChildren(self):
        """
            Returns javascript that will toggle the visibility of the checkbox field child elements clientside
        """
        javascript = "JUToggleElement('" + self.childContainer.fullId() + "');"
        return javascript

    def validators(self, useFullId=True):
        # Only use the validators contained in the
        # childElements when the checkbox is clicked
        if not self.userInput.value():
            return {}

        return BaseField.validators(self, useFullId)

    def exportVariables(self, exportedVariables=None, flat=False):
        if exportedVariables == None: exportedVariables = {}

        # Only export child values when thet checkbox is clicked
        if not self.userInput.value():
            self.userInput.exportVariables(exportedVariables, flat)
        else:
            BaseField.exportVariables(self, exportedVariables, flat)

        return exportedVariables

Factory.addProduct(CheckboxField)

class IntegerField(BaseField):
    """
        A field with a incremntable and deincrementable textfield (with up and down arrows) as the input
    """
    inputElement = Inputs.IntegerTextBox
    validator = "NewValidators.Int()"
    properties = TextField.properties.copy()
    Base.addChildProperties(properties, Inputs.IntegerTextBox, 'userInput')

    def __init__(self, id, name, parent):
        BaseField.__init__(self, id, name=None, parent=None)

        self.toggleLayout = self.addChildElement(Layout.Vertical())
        self.toggleLayout.style["font-size"] = "75%"
        self.toggleLayout.addClass("Clickable")

        self.label.style['display'] = "block"
        self.label.style['margin-top'] = "5px;"
        self.up = self.toggleLayout.addChildElement(Buttons.UpButton())
        self.up.addClass("hidePrint")
        self.down = self.toggleLayout.addChildElement(Buttons.DownButton())
        self.down.setValue('images/count_down.png')
        self.down.addClass("hidePrint")
        self.userInput.setValue(0)

        self.connect("beforeToHtml", None, self, "__addEvents__")
        self.connect("beforeToHtml", None, self, "__updateReadOnly__")

    def __addEvents__(self):
        minimum = self.userInput.minimum
        if minimum == None:
            minimum = "undefined"
        maximum = self.userInput.maximum
        if maximum == None:
            maximum = "undefined"
        self.up.addJavascriptEvent('onclick', "JUIncrement('%s', %s);" %
                                 (self.userInput.jsId(), str(maximum)))
        self.down.addJavascriptEvent('onclick', "JUDeincrement('%s', %s);" %
                                 (self.userInput.jsId(), str(minimum)))

    def __updateReadOnly__(self):
        if not self.editable():
            self.toggleLayout.remove()

Factory.addProduct(IntegerField)


class DateField(TextField):
    """
        A field with a date widget as the input (which provides a browseable way to select the date)
    """
    properties = TextField.properties.copy()
    Base.addChildProperties(properties, Display.Label, 'calendarTypeLabel')
    properties['isZulu'] = {'action':'setIsZulu', 'type':'bool'}
    properties['hideTypeLabel'] = {'action':'formatDisplay.call', 'name':'hide', 'type':'bool'}
    properties['dateFormat'] = {'action':'classAttribute'}

    def __init__(self, id, name=None, parent=None):
        TextField.__init__(self, id, name, parent)
        self.userInput.style['width'] = '7.5em'
        self.dateFormat = "dd-mmm-yyyy"

        layout = self.addChildElement(Layout.Horizontal())
        layout.addClass("FieldDescription")
        self.calendarLink = layout.addChildElement(Display.Image(id + "CalendarLink"))
        self.calendarLink.addClass('Clickable')
        self.calendarLink.addClass('hidePrint')
        self.calendarLink.setValue('images/calendar_icon.gif')
        self.calendarLink.addJavascriptEvent('onclick', CallBack(self, "jsOpenCalendar"))

        self.calendarTypeLabel = layout.addChildElement(Display.Label())
        self.calendarTypeLabel.style['margin-left'] = "4px;"
        self.calendarTypeLabel.style['margin-right'] = "4px;"
        self.calendarTypeLabel.style['display'] = "block;"

        self.setIsZulu(False)
        self.formatDisplay = layout.addChildElement(Display.Label())

        self.connect('beforeToHtml', None, self, '__updateDisplay__')

    def setIsZulu(self, isZulu):
        """
            If set to true the calender will use the zulu date
        """
        self.isZulu = isZulu
        if isZulu:
            self.calendarTypeLabel.setText("Z")
        else:
            self.calendarTypeLabel.setText("LCL")

    def __updateDisplay__(self):
        if not self.editable():
            self.calendarLink.hide()
        self.formatDisplay.setText(self.dateFormat)

    def jsOpenCalendar(self):
        """
            Returns the javascript that will open the calender clientside
        """
        if self.isZulu:
            calendarType = "zulu"
        else:
            calendarType = "lcl"

        return ("%sCalendar.popUpCalendar(this, JUGetElement('%s'), '%s')" %
                (calendarType, self.userInput.fullId(), self.dateFormat))

Factory.addProduct(DateField)


class NestedSelect(Layout.Vertical):
    """
        Defines two select Layout.Boxes where the selection of an item from the first will trigger
        the population of the second.
    """
    properties = Layout.Vertical.properties.copy()
    properties['groupData'] = {'action':'setGroupData'}
    properties['groupLabel'] = {'action':'setGroupLabel'}
    properties['itemLabel'] = {'action':'setItemLabel'}
    properties['selectWidth'] = {'action':'setSelectWidth'}

    def __init__(self, id=None, name=None, parent=None):
        Layout.Vertical.__init__(self, id + "NestedSelect", name, parent)

        self.groupLabel = self.addChildElement(Display.Label())
        self.groupSelect = self.addChildElement(Inputs.Select(id))
        self.groupSelect.addJavascriptEvent('onclick', CallBack(self, "jsPopulateItemSelect"))
        self.groupSelect.connect('selectionChanged', None, self, 'updateItems')

        self.itemLabel = self.addChildElement(Display.Label())
        self.itemSelect = self.addChildElement(Inputs.Select(id + "Items"))

        self.groups = []
        self.items = {}

    def updateItems(self):
        """
            Updates the items select Layout.Box to load the items contained in the currently
            selected group.
        """
        selected = self.groupSelect.selected()
        if selected:
            for item in self.items[selected.value()]:
                self.itemSelect.addOption(item)

    def setGroupData(self, data):
        """
            Sets the groups and the items each group should contain
                data - a list of groupnames and item lists, for example:
                    [{'name':'fruits, 'value':['apple', 'orange', 'grape']}]
        """
        self.groupSelect.reset()
        self.itemSelect.reset()
        self.groups = []
        self.items = {}
        for group in data:
            newGroup = group['name']
            items = group['value']
            self.groups.append(newGroup)
            self.items[newGroup] = items
            self.groupSelect.addOption(newGroup, newGroup)

        self.addScript(CallBack(self, "jsGroups"))
        self.addScript(CallBack(self, "jsPopulateItemSelect"))

    def setGroupLabel(self, text):
        """
            Sets the text to be shown above the group selectbox
                text - the labels text
        """
        self.groupLabel.setText(text)

    def setItemLabel(self, text):
        """
            Sets the text to be shown above the item selectbox
                text - the labels text
        """
        self.itemLabel.setText(text)
        self.itemSelect.id = self.groupSelect.id + text

    def setSelectWidth(self, width):
        """
            Sets the width of both select Layout.Boxes
        """
        self.groupSelect.style['width'] = width
        self.itemSelect.style['width'] = width

    def jsGroups(self):
        """
            Creates the group structure client side
        """
        return """document.%(groupId)s = %(groups)s;
                  document.%(itemId)s = %(items)s;
               """ % {'items':self.items, 'groups':self.groups, 'id':self.jsId(),
                      'itemId':self.itemSelect.jsId(), 'groupId':self.groupSelect.jsId()}

    def jsPopulateItemSelect(self):
        """
            Populates the item select Layout.Box with the items contained in the selected group
        """
        return """populateSelect(document.getElementById('%(itemSelectId)s'),
                     document.%(itemSelectId)s[document.getElementById('%(groupSelectId)s').value]);
               """ % {'itemSelectId':self.itemSelect.jsId(),
                      'groupSelectId':self.groupSelect.jsId()}

Factory.addProduct(NestedSelect)


class Filter(Layout.Box):
    """
        Defines a dynamic and expandable list of filters
    """

    jsFunctions = ["javascriptAddFilter", "javascriptRemoveFilter"]

    def __init__(self, id, name=None, parent=None):
        Layout.Box.__init__(self, id, name, parent)

        self.searchFieldList = []
        self.filters = [self, ]
        self.isSubFilter = False

        filterContainer = Layout.Box(id + ":Container")
        filterContainer.addClass('Filter')
        self.filterContainer = self.addChildElement(filterContainer)

        filterInput = Layout.Box()
        filterInput.style['float'] = 'left'
        filterContainer.addChildElement(filterInput)

        label = Display.Label('filterTermLabel')
        label.setText('Search for:')
        filterInput.addChildElement(label)

        searchTerm = Inputs.TextBox(id + ":SearchTerm", "FilterTerm")
        searchTerm.addClass("FilterTerm")
        self.searchTerm = filterInput.addChildElement(searchTerm)

        label = Display.Label('filterFieldLabel')
        label.setText('in:')
        filterInput.addChildElement(label)

        searchFields = Inputs.Select(id + ":SearchFields", "FilterField")
        searchFields.addClass("FilterField")
        self.searchFields = filterInput.addChildElement(searchFields)

        filterType = Inputs.TextBox(id + ":FilterType", "FilterType")
        filterType.addClass('filterType')
        filterType.attributes['type'] = "hidden"
        filterType.setValue("BaseFilter")
        self.filterType = filterInput.addChildElement(filterType)

        removeButton = Buttons.Link(id + ":Remove")
        removeButton.style['float'] = 'right'
        removeButton.style['display'] = 'none'
        removeButton.setText("")
        removeButton.textBeforeChildren = "<img src='images/close.gif' />"
        removeButton.addClass('Clickable')
        removeButton.addClass('RemoveFilter')
        removeButton.addJavascriptEvent("onclick", CallBack(self, 'jsRemoveFilter'))
        removeButton.addJavascriptEvent("onmouseover",
                                        """JUAddClass(JUParentElement(this,
                                                                      'Filter'),
                                                        'FilterHighlight');""")
        removeButton.addJavascriptEvent("onmouseout",
                                        """JURemoveClass(JUParentElement(this,
                                                                      'Filter'),
                                                        'FilterHighlight');""")
        self.removeButton = filterContainer.addChildElement(removeButton)

        addFilter = Layout.Box()
        addFilter.addClass('AddFilter')
        addFilter.style['clear'] = 'both'
        addAndFilter = Buttons.ToggleButton(id + ":And")
        addAndFilter.button.addClass('AddFilterButton')
        addAndFilter.button.addClass('AddAndFilter')
        addAndFilter.setValue("And")
        self.addAndFilter = addFilter.addChildElement(addAndFilter)
        addOrFilter = Buttons.ToggleButton(id + ":Or")
        addOrFilter.button.addClass('AddFilterButton')
        addOrFilter.button.addClass('AddOrFilter')
        addOrFilter.setValue("Or")
        self.addOrFilter = addFilter.addChildElement(addOrFilter)
        self.addFilter = filterContainer.addChildElement(addFilter)

        subFilter = Layout.Box()
        subFilter.addClass('subFilter')
        self.subFilter = self.addChildElement(subFilter)

        addOrFilter.connect('toggled', True, addAndFilter, 'toggleOff')
        addOrFilter.connect('jsToggled', None, self, 'jsAddOrFilter')
        addOrFilter.connect('jsToggled', True, addAndFilter, 'jsToggleOff')

        addAndFilter.connect('toggled', True, addOrFilter, 'toggleOff')
        addAndFilter.connect('jsToggled', None, self, 'jsAddAndFilter')
        addAndFilter.connect('jsToggled', True, addOrFilter, 'jsToggleOff')

        self.addJSFunctions(self.__class__)

    def jsAddAndFilter(self, toggledOn):
        """
            Return the javascript to add an And filter to the filter list clientside
        """
        return self.jsAddFilter("And", toggledOn)

    def jsAddOrFilter(self, toggledOn):
        """
            Return the javascript to add an Or filter to the filter list clientside
        """
        return self.jsAddFilter("Or", toggledOn)

    def jsAddFilter(self, filterType, toggledOn):
        """
            Return the javascript to add a filter to the filter list clientside
        """
        return "javascriptAddFilter(this, '" + filterType + "', " + \
                                    interpretAsString(toggledOn) + ");"

    def jsRemoveFilter(self):
        """
            Return the javascript to remove a filter to the filter list clientside
        """
        return "javascriptRemoveFilter(this);"

    @staticmethod
    def javascriptAddFilter(element, filterType, toggledOn):
        return """
            if(toggledOn){
                parentFilter = JUParentElement(element, 'WFilter');
                filter = JUGetElementByClassName('WFilter', parentFilter);
                if(!filter){
                    filter = JUCopy(parentFilter,
                                    JUGetElementByClassName('subFilter',
                                                            parentFilter));
                    oldTerm = JUGetElementByClassName('FilterTerm',
                                                        parentFilter);
                    newTerm = JUGetElementByClassName('FilterTerm', filter);
                    newTerm.value = oldTerm.value;
                    newTerm.focus();
                    newTerm.select();
                    JUGetElementByClassName('RemoveFilter', filter).style.display = 'block';
                }
                JUGetElementByClassName('filterType', filter).value = filterType;
            }
            else{
                JURemoveElement(JUGetElementByClassName('WFilter',
                                        JUParentElement(element, 'WFilter')));
            }"""

    @staticmethod
    def javascriptRemoveFilter(element):
        return """
                thisFilter = JUParentElement(element, 'WFilter');
                childFilter = JUGetElementByClassName('WFilter', thisFilter);
                filterType = JUGetElementByClassName('filterType',
                                                     childFilter).value;

                AndButton = JUGetElementByClassName('AddAndFilter', thisFilter);
                OrButton = JUGetElementByClassName('AddOrFilter', thisFilter);
                parentFilter = JUParentElement(thisFilter, 'WFilter');

                parentAndButton = JUGetElementByClassName('AddAndFilter',
                                                          parentFilter);
                parentOrButton = JUGetElementByClassName('AddOrFilter',
                                                         parentFilter);

                parentOrButton.className = OrButton.className;
                parentAndButton.className = AndButton.className;

                if(filterType == 'Or'){
                    JUNextElement(parentOrButton).value = 'on';
                    JUNextElement(parentAndButton).value = 'off';
                }
                else if(filterType == 'And'){
                    JUNextElement(parentAndButton).value = 'on';
                    JUNextElement(parentOrButton).value = 'off';
                }
                else{
                    JUNextElement(parentAndButton).value = 'off';
                    JUNextElement(parentOrButton).value = 'off';
                }

                if(childFilter)
                {
                    JUMove(childFilter,
                        JUGetElementByClassName('subFilter', parentFilter));
                }
                JURemoveElement(thisFilter);
               """

    def addSearchField(self, searchField):
        """
            Adds a search field (a filter) for rendering
        """
        field = Inputs.Option("field:" + searchField)
        field.setText(searchField)
        field.setValue(searchField)
        self.searchFieldList.append(searchField)
        self.searchFields.addChildElement(field)

    def insertVariables(self, valueDict=None):
        if valueDict == None: valueDict = {}

        if self.isSubFilter:
            return Layout.Box.insertVariables(self, valueDict)

        searchTerms = valueDict.get(self.searchTerm.name, '')
        if type(searchTerms) == list:
            currentFilter = self
            for index in xrange(1, len(searchTerms)):
                newFilter = Filter(self.id + unicode(index))
                newFilter.searchFields.addOptions(self.searchFields.options())
                newFilter.removeButton.style['display'] = 'block'
                newFilter.isSubFilter = True
                self.filters.append(newFilter)

                currentFilter = currentFilter.subFilter.addChildElement(newFilter)

        Layout.Box.insertVariables(self, valueDict)

    def filterList(self, valueDict=None):
        """
            Returns the set list of filters
        """
        filterList = []
        for filter in self.filters:
            if filter.searchTerm.value():
                filterList.append({'term':filter.searchTerm.value(),
                                   'field':filter.searchFields.value(),
                                   'type':filter.filterType.value()})

        return filterList

Factory.addProduct(Filter)
