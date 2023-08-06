""" Inspect UI components """
import logging

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
        for child in component.getComponents():
            result['childs'].append(Inspector.inspect(child))
        return result


def _getTitle(component):
    if not hasattr(component, 'getText'):
        return "N/A"
    return str(component.getText())


def _getText(component):
    if not hasattr(component, 'getTitle'):
        return None
    return str(component.getTitle())
