# flake8: noqa: F401
import os
import importlib
import jpype
import jpype.imports

def start(classpath=None):
    """ Start the pyjt JVM.

        Needs to be called before using pyjt.

        :param classpath:   If set, use this classpath for the JVM, otherwise
                            use CLASSPATH environment variable.
    """
    cp = os.environ.get('CLASSPATH', '') if classpath is None else classpath
    jpype.startJVM(jpype.getDefaultJVMPath(), f"-Djava.class.path={cp}")

def stop():
    jpype.shutdownJVM()



def run(app, args=[""]):
    """ Run the main function of **app**.

        This helper function will start the **app** by invoking it's
        "main" function.

        Note:

            You can as well start your application manually, assuming
            your application is in MyApplication.java, the could would look
            like:

                import MyApplication
                MyApplication.main()
    """
    module = importlib.import_module(app)
    module.main(args)

def shutdown():
    """ Shuts down pyjt and the JVM. """
    jpype.shutdownJVM()

from .Proxy import Proxy
from .Robot import Robot
from .Frame import Frame, FrameFinder
from .Fixture import Fixture, FillMode
from .Errors import ElementNotFoundError
from .ComponentFinder import Locator
from .Inspector import Inspector
from .Errors import ElementNotFoundError
