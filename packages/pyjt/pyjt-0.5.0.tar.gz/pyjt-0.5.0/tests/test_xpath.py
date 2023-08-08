from lxml import etree

import logging


def test_simple_xpath(helloworld, java, javax):
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
