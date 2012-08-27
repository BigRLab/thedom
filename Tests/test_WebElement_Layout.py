from test_WebElement_Base import ElementTester
from WebElements.All import Factory

class TestStack(ElementTester):

    def setup_class(self):
        self.element = Factory.build("Stack", name="Test")
        self.element.addChildElement(Factory.build("Button", name="Button"))
        self.element.addChildElement(Factory.build("box", name="box"))


class TestBox(ElementTester):

    def setup_class(self):
        self.element = Factory.build("Box", name="Test")

    def test_containerType(self):
        assert self.element.containerType() == "div"
        self.element.setContainerType("span")
        assert self.element.containerType() == "span"

        self.element.setContainerType("div")
        assert self.element.containerType() == "div"

        assert not self.element.setContainerType("fdsd")
        assert self.element.containerType() == "div"


class TestFlow(ElementTester):

    def setup_class(self):
        self.element = Factory.build("box", name="Test")
        self.flowContainer = self.element.addChildElement(Factory.build("flow", name="flow"))
        self.flowContainer.addChildElement(Factory.build("Button", name="Button"))
        self.flowContainer.addChildElement(Factory.build("box", name="box"))

class TestHorizontal(ElementTester):

    def setup_class(self):
        self.element = Factory.build("Horizontal", name="Test")
        self.element.addChildElement(Factory.build("Button", name="Button"))
        self.element.addChildElement(Factory.build("Container", name="Container"))


class TestVertical(ElementTester):

    def setup_class(self):
        self.element = Factory.build("Vertical", name="Test")
        self.element.addChildElement(Factory.build("Button", name="Button"))
        self.element.addChildElement(Factory.build("Container", name="Container"))


class TestFields(ElementTester):

    def setup_class(self):
        self.element = Factory.build("Fields", name="Test")


class TestLineBreak(ElementTester):

    def setup_class(self):
        self.element = Factory.build("lineBreak", name="Test")


class TestHorizontalRule(ElementTester):

    def setup_class(self):
        self.element = Factory.build('HorizontalRule', 'test')


class TestVerticalRule(ElementTester):

    def setup_class(self):
        self.element = Factory.build('VerticalRule', 'test')

if __name__ == "__main__":
    import subprocess
    subprocess.Popen("py.test test_WebElement_Layout.py", shell=True).wait()
