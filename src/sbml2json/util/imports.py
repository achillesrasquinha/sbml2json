<<<<<<< HEAD
=======
from sbml2json.exceptions import DependencyNotFoundError

>>>>>>> template/master
class HandlerRegistry(dict):
    def __missing__(self, name):
        if '.' not in name:
            handler = __import__(name)
        else:
            module_name, handler_name = name.rsplit('.', 1)

            module  = __import__(module_name, {}, {}, [handler_name])
            handler = getattr(module, handler_name)

        self[name] = handler

        return handler

_HANDLER_REGISTRY = HandlerRegistry()

def import_handler(name):
    handler = _HANDLER_REGISTRY[name]
<<<<<<< HEAD
    return handler
=======
    return handler

def import_or_raise(package, name = None):
    name = name or package

    try:
        import_handler(package)
    except ImportError:
        raise DependencyNotFoundError((
            "Unable to import {package} for resolving dependencies. "
            "sbml2json requires {package} to be installed. "
            "Please install {package} by executing 'pip install {name}'."
        ).format(package = package, name = name))
>>>>>>> template/master
