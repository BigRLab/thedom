'''
    test_DataViews.py

    Tests the functionality of thedom/DataViews.py

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

from test_WebElement_Base import ElementTester
from thedom.All import Factory
from thedom.DataViews import Table


class TestTable(ElementTester):

    class TestColumn(ElementTester):

        def setup_class(self):
            self.element = Table.Column("Test")

        def test_text(self):
            assert self.element.text() == ""
            self.element.setText("I changed the text")
            assert self.element.text() == "I changed the text"
            assert "I changed the text" in self.element.toHTML()

    def setup_method(self, element):
        self.element = Factory.build("Table", "Test")

    def test_attributes(self):
        assert self.element.rows == []
        assert self.element.columns == []

    def test_addRow(self):
        row = self.element.addRow()
        assert len(self.element.rows) == 1
        assert self.element.columns == []

        assert not row.actualCell("Name")
        assert self.element.header.childElements == []

        #Setting a cell with a valid row & not yet created column
        #should automatically create the header and column
        row.cell("Name").setText("Timothy")
        assert row.cell("Name").text() == "Timothy"
        assert type(row.actualCell("Name")) == Table.Column
        assert len(self.element.header.childElements) == 1

        row.cell("Name").setText("Josh")
        assert row.cell("Name").text() == "Josh"
        assert type(row.actualCell("Name")) == Table.Column
        assert len(self.element.header.childElements) == 1

        row.cell("Type").setText("Person")
        assert row.cell("Type").text() == "Person"
        assert type(row.actualCell("Type")) == Table.Column
        assert len(self.element.header.childElements) == 2

    def test_addRows(self):
        # Using a list of dictionaries to populate a table is the most straight-forward method, but looses column
        # order
        self.element.addRows(({'B':'Row1', 'A':'Row1'}, {'B':'Row2', 'A':'Row2'}))
        assert self.element.columns == ['A', 'B']

        # Using nested tuples when adding rows should allow you to define the order of columns
        newTable = Factory.build('Table', 'Test2')
        newTable.addRows(((('B','Row1'), ('A','Row1')), (('B','Row2'), ('A','Row2'))))
        assert newTable.columns == ['B', 'A']

    def test_reorderingColumns(self):
        self.element.addRows(({'B':'Cell1', 'A':'Cell2'}, {'B':'Cell3', 'A':'Cell4'}))
        assert self.element.columns == ['A', 'B']
        assert self.element.rows[0][0][0].text() == "Cell2"
        assert self.element.rows[0][1][0].text() == "Cell1"
        assert self.element.rows[1][0][0].text() == "Cell4"
        assert self.element.rows[1][1][0].text() == "Cell3"

        self.element.columns = ['B', 'A']
        assert self.element.columns == ['B', 'A']
        assert self.element.rows[0][0][0].text() == "Cell1"
        assert self.element.rows[0][1][0].text() == "Cell2"
        assert self.element.rows[1][0][0].text() == "Cell3"
        assert self.element.rows[1][1][0].text() == "Cell4"

    def test_setCell(self):
        newRow = self.element.addRow()
        newRow.cell("Name").setText("Tim")
        newRow.cell("Type").setText("Developer")
        newRow.cell("Country").setText("United States")

        assert newRow.cell('Name').text() == "Tim"
        assert newRow.cell('Type').text() == "Developer"
        assert newRow.cell('Country').text() == "United States"

    def test_appendToCell(self):
        newRow = self.element.addRow()
        newRow.cell("Name").setText("Tim")
        newRow.cell("Type").setText("Developer")
        newRow.cell("Country").setText("United")

        assert newRow.cell('Name').text() == "Tim"
        assert newRow.cell('Type').text() == "Developer"
        assert newRow.cell('Country').text() == "United"

        newRow.cell("Name").appendText("Crosley")
        newRow.cell("Country").appendText("States")

        assert newRow.cell('Name').text() == "Tim" # Appended text is only visible by going through label tree
        assert newRow.cell('Type').text() == "Developer"
        assert newRow.cell('Country').text() == "United"

    def test_addColumn(self):
        column1 = self.element.addColumn("Name")
        column2 = self.element.addColumn("Type")
        column3 = self.element.addColumn("Super Powers")
        assert len(self.element.rows) == 0
        assert self.element.columns == ["Name", "Type", "Super Powers"]
        assert len(self.element.header.childElements) == 3

        # assert it returns existing column if it is added a second
        column1again = self.element.addColumn("Name")
        column2again = self.element.addColumn("Type")
        assert column1again == column1
        assert column2again == column2

        row = self.element.addRow()
        assert len(self.element.rows) == 1
        assert row.cell("Name").text() == ""
        assert row.cell("Type").text() == ""
        assert row.cell("Super Powers").text() == ""
        assert type(row.actualCell("Name")) == Table.Column
        assert type(row.actualCell("Type")) == Table.Column
        assert type(row.actualCell("Super Powers")) == Table.Column

        row.cell("Name").setText("Timothy")
        row.cell("Type").setText("Person")
        row.cell("Super Powers").setText("Bassically all of them.")
        assert row.cell("Name").text() == "Timothy"
        assert row.cell("Type").text() == "Person"
        assert row.cell("Super Powers").text() == "Bassically all of them."

        self.element.addColumn("Lied About Super Powers")
        assert self.element.columns == ["Name", "Type", "Super Powers",
                                        "Lied About Super Powers"]
        assert len(self.element.header.childElements) == 4

        assert row.cell("Lied About Super Powers").text() == ""
        row.cell("Lied About Super Powers").setText("Ok Maybee a little bit...")
        assert row.cell("Lied About Super Powers").text() == "Ok Maybee a little bit..."

    def test_setProperties(self):
        data = (("columns", ["Name", "Type", "Location"]),
                ("rows", [{"Name":"start.bin",
                          "Type":"Binary",
                          "Location":"/usr/bin"},
                          {"Name":"document.txt",
                           "Type":"Text File",
                           "Location":"~/documents"}]))

        self.element.setProperties(data)
        assert len(self.element.rows) == 2
        assert self.element.columns == ["Name", "Type", "Location"]
        assert len(self.element.header.childElements) == 3
        self.element.cell(0, "Name").setText("start.bin")
        self.element.cell(0, "Type").setText("Binary")
        self.element.cell(0, "Location").setText("/usr/bin")
        self.element.cell(1, "Name").setText("document.txt")
        self.element.cell(1, "Type").setText("Text File")
        self.element.cell(1, "Location").setText("~/documents")


class TestStoredValue(ElementTester):

    def setup_class(self):
        self.element = Factory.build("storedValue", "Test", "Test")
