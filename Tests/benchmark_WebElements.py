import cPickle as pickle
import gc
import sys
import time

from WebElements.DictUtils import OrderedDict
from WebElements.All import Factory
from WebElements.Base import WebElement
from WebElements.Layout import Box
from WebElements.Resources import ScriptContainer

results = {'loopedCreate':0.0, 'loopedInit':0.0, 'loopedToHtml':0.0,
           'createAllOnce':0.0, 'longestCreationTime':0.0,
           'nestedNodeCreation':0.0}

def doneSection():
    sys.stdout.write(".")
    sys.stdout.flush()

def getSingleElementGenerationTimes():
    generationTimes = OrderedDict()
    for product in Factory.products.keys():
        if "." in product:
            continue
        doneSection()
        startTime = time.time()
        scripts = ScriptContainer()
        element = Factory.build(product, 'Test', 'Product')
        element.setScriptContainer(scripts)
        html = element.toHtml()
        html += scripts.toHtml()

        generationTime = time.time() - startTime
        results['createAllOnce'] += generationTime
        generationTimes[generationTime] = (product, len(html))
    results['longestCreationTime'] = generationTimes.orderedKeys[-1]
    return generationTimes

def getGenerationTimeForAllElementsLooped100Times():
    startTime = time.time()
    allProducts = Box('AllProducts')
    scripts = ScriptContainer()
    allProducts.setScriptContainer(scripts)
    for x in xrange(100):
        doneSection()
        for product in Factory.products.keys():
            allProducts.addChildElement(Factory.build(product, 'Test', 'Product'))
    instantiationTime = time.time() - startTime
    results['loopedInit'] = instantiationTime

    startTime = time.time()
    html = allProducts.toHtml()
    html += scripts.toHtml()
    generationTime = (time.time() - startTime)
    results['loopedToHtml'] = generationTime
    results['loopedToHtmlSize'] = len(html)
    results['loopedCreate'] = results['loopedInit'] + results['loopedToHtml']

def getNestedElementTime():
    startTime = time.time()
    rootElement = WebElement('root')
    element = rootElement
    element.tagName = "root"
    html = ""
    for x in xrange(900):
        doneSection()
        element = element.addChildElement(WebElement("element" + str(x)))
        element.tagName = 'tag' + str(x)
        html += element.toHtml()

    results['nestedNodeCreation'] = time.time() - startTime
    results['nestedNodeSize'] = len(html)

if __name__ == "__main__":
    sys.stdout.write("Benchmarking .")
    doneSection()
    getGenerationTimeForAllElementsLooped100Times()
    gc.collect()
    results['generationTimes'] = getSingleElementGenerationTimes()
    gc.collect()
    doneSection()
    getNestedElementTime()
    print "."

    print "######## Indvidual element generation times ########"
    results['generationTimes'].orderedKeys.sort()
    for generationTime, info in results['generationTimes'].iteritems():
        print "    Generating html for %s took %s seconds and produced %d len html" % (info[0], generationTime, info[1])
    print "    Total Time: %s" % results['createAllOnce']

    print "######## Looped creation time (%d elements) ########" %  len(Factory.products.keys() * 100)
    print "    Instantiating Elements: " + str(results['loopedInit'])
    print "    Generating Html: " + str(results['loopedToHtml'])
    print "    Html Size: " + str(results['loopedToHtmlSize'])
    print "    Total Time:" + str(results['loopedCreate'])

    print "######## Nested element generation #########"
    print "    Generating 900 nested elements took: " + str(generationTime)
    print "    Html Size: ", results['nestedNodeSize']
    results['nestedGeneration'] = generationTime

    with open(".test_WebElements_Benchmark.results", 'w') as resultFile:
        resultFile.write(pickle.dumps(results))
