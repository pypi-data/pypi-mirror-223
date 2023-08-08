""" Inspect UI components """

import logging
from lxml import etree

log = logging.getLogger(__name__)


class Inspector:
    """ Helper class for inspecting the component tree of a specific component.
    """
    @staticmethod
    def inspect(component):
        """ Inspects the component tree of a component.

            Args:
                component (Fixture):
                    The component to inspect.

            Returns:
                dict:
                    A dictionary with information of all sub-components
                    for this component.
        """
        result = {}
        result['name'] = str(component.getName())
        result['class'] = str(component.getClass())
        result['text'] = _getText(component)
        title = _getTitle(component)
        if title:
            result['title'] = title

        result['childs'] = []
        if not hasattr(component, 'getComponents'):
            return result
        for child in component.components():
            result['childs'].append(Inspector.inspect(child))
        return result

    @staticmethod
    def etree(component):
        return Inspector.etreemap(component)[0]

    @staticmethod
    def etreemap(component, mapping=None):
        if not mapping:
            mapping = {}
        _id = id(component)
        mapping[_id] = component
        element = etree.Element(str(component.getClass().getSimpleName()))
        text = _getText(component)
        if text is not None:
            element.set("text", text)
        element.set("name", str(component.getName()))
        title = _getTitle(component)
        if title is not None:
            element.set("title", str(title))
        element.set("_id", str(_id))

        for subelement in component.components():
            element.append(Inspector.etreemap(subelement, mapping)[0])
        return (element, mapping)


def _getTitle(component):
    if not hasattr(component, 'getTitle'):
        return None
    return str(component.getTitle())


def _getText(component):
    if not hasattr(component, 'getText'):
        return None
    return str(component.getText())
