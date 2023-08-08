from pyjt import ElementNotFoundError
from lxml import etree
from tools import assert_raises

import logging


def test_miss(helloworld, java, javax):
    xpath = "//JLabel[contains(@text, 'XName')]"
    assert_raises(ElementNotFoundError, lambda: helloworld.find_by_xpath(xpath))


def test_simple_xpath(helloworld, java, javax):
    xpath = "//JLabel[contains(@text, 'Name')]"
    label = helloworld.find_by_xpath(xpath)
    assert label.getText() == "Name:"
    xpath = "//JLabel[contains(@text, 'Name')]"
    label = helloworld.find_by_xpath(xpath)
    assert label.getText() == "Name:"


def test_advanced_xpath(helloworld, java, javax):
    xpath = "//Container[//JLabel[contains(@text, 'Name')]]/JTextField"
    logging.warning(etree.tostring(helloworld.etree()))
    tf = helloworld.find_by_xpath(xpath)
    tf.fill("xpath")
    xpath = "//Container[//JLabel[contains(@text, 'Name')]]/JTextField[@text='xpath']"
    tf = helloworld.find_by_xpath(xpath)
    assert tf is not None
