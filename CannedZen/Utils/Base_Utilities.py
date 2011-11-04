import os, shutil

def current_path(fle): return os.path.dirname(os.path.abspath(fle))

def default_app_path(fle, name): return os.path.join(current_path(fle), name)

def try_delete_path(pth):
    try:
        if(os.path.isdir(pth)): shutil.rmtree(pth)
        if(os.path.isfile(pth)): os.remove(pth)
        return True
    except: return False

class curry:
    def __init__(self, fun, *args, **kwargs):
        self.fun = fun
        self.pending = args[:]
        self.kwargs = kwargs.copy()

    def __call__(self, *args, **kwargs):
        if kwargs and self.kwargs:
            kw = self.kwargs.copy()
            kw.update(kwargs)
        else:
            kw = kwargs or self.kwargs

        return self.fun(*(self.pending + args), **kw)

class FilePermissionException(Exception): pass

class FileExistsException(Exception): pass

class UninstallingItemDNEException(Exception): pass

class IllegalInitializationException(Exception): pass

class MissingDependencyException(Exception): pass

# We could change the underlying implementation
# to Fabric One Day if we wanted to
def command(comm): os.system(comm)
