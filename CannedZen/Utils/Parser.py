import re

# << var_name:var_type|"local variable string" >>



template_regex = re.compile(r'\<\<\s*(?P<var_name>.*?):(?P<var_type>.*?)\s*\>\>')
WS = "    "

def get_variables(tb):
    return template_regex.findall(tb)
def process_textblock(tb, context):
    for key, val in context.items():
        tb = re.sub(r'\<\<\s*'+key+r':.*?(\|\w)?\s*\>\>', str(val), tb)
    return tb
def indent(s):
    ret = ""
    for line in s.splitlines():
        if line:
            ret += WS + line + '\n'
    return ret

class Processor(object):
    def __init__(self, **kwargs):
        pass
    
    @classmethod
    def _process(cls, *args):
        self = cls()
        return self.process(*args)
    
    def process(self, varname, template, hooks, local):
        ret = ""
        ret += self.start(varname, hooks, local)
        ret += self.processHooks(varname, hooks, local)
        ret += self.end(varname, hooks, local)
        return process_textblock(template, {varname: ret})
        
    def start(self, varname, hooks, local):
        return ""
    
    def processHooks(self, varname, hooks, local):
        return str(hooks[-1])
    
    def end(self, varname, hooks, local):
        return ""

class RawProcessor(Processor):
    def __init__(self, **kwargs):
        Processor.__init__(self, **kwargs)
    
    def processHooks(self, varname, hooks, local):
        ret = ""
        for hook in hooks:
            ret += "%s\n" % (str(hook))
        return ret

class InlineProcessor(Processor):
    def __init__(self, **kwargs):
        Processor.__init__(self, **kwargs)

    def processHooks(self, varname, hooks, local):
        ret = ""
        for hook in hooks:
            ret += "%s" % (str(hook))
        return ret

class TupleProcessor(Processor):
    def __init__(self, **kwargs):
        Processor.__init__(self, **kwargs)
    
    def processHooks(self, varname, hooks, local):
        return "(%s)" % ( ", ".join(str(hook) for hook in hooks) )

class VariableProcessor(Processor):
    def __init__(self, **kwargs):
        Processor.__init__(self, **kwargs)
        self.startline = ""
        self.endline = ""
    
    def start(self, varname, hooks, local):
        startline = local if local else self.startline
        return "%s = %s" % (varname, startline)
    
    def end(self, varname, hooks, local):
        return self.endline

class MultiLineVariableProcessor(VariableProcessor):
    def __init__(self, **kwargs):
        VariableProcessor.__init__(self, **kwargs)
        self.seperator = ""
        
    def processHooks(self, varname, hooks, local):
        indent
        ret = ""
        for hook in hooks:
            ret += "%s%s\n" % (str(hook), self.seperator)
        return indent(ret)
        
class VariableTupleProcessor(MultiLineVariableProcessor):
    def __init__(self, **kwargs):
        MultiLineVariableProcessor.__init__(self, **kwargs)
        self.startline = "("
        self.endline = ")"
        self.seperator = ","

class AppendProcessor(Processor):
    def __init__(self, **kwargs):
        Processor.__init__(self, **kwargs)
    
    def process(self, varname, template, hooks, local):
        ret = template
        for hook in hooks:
            ret += "\n\n%s" % (str(hook))
        return ret
    
class PrependProcessor(Processor):
    def __init__(self, **kwargs):
        Processor.__init__(self, **kwargs)
    
    def process(self, varname, template, hooks, local):
        ret = ""
        for hook in hooks:
            ret += "%s\n\n" % (str(hook))
        ret += template
        return ret

class ModelProcessor(Processor):
    def __init__(self, **kwargs):
        Processor.__init__(self, **kwargs)
    
    def process(self, varname, template, hooks, local):
        print hooks
        if isinstance(hooks, type([])):
            return process_textblock(template, {varname: hooks[0].name})
        else:
            return process_textblock(template, {varname: hooks.name})

def expand_dict(d):
    if isinstance(d, dict):
        ret = "{"
        for key, val in d.s.items():
            s = str(val)
            if isinstance(val, dict):
                s = expand_dict(val)
            elif isinstance(val, str):
                s = "'%s'" % (s)
            ret += "'%s': %s," % (key, s)
        ret += "}"
        return ret
    else:
        return str(d)
    
class DictProcessor(RawProcessor):
    def __init__(self, **kwargs):
        RawProcessor.__init__(self, **kwargs)
        
    def processHooks(self, varname, hooks, local):
        return expand_dict(hooks[-1])

class VariableDictProcessor(VariableProcessor):
    def __init__(self, **kwargs):
        VariableProcessor.__init__(self, **kwargs)
        
    def processHooks(self, varname, hooks, local):
        return expand_dict(hooks[-1])

class InternalTemplateProcessor(Processor):
    def __init__(self, **kwargs):
        Processor.__init__(self, **kwargs)
    
    def process(self, varname, template, hooks, local):

        pat = r"\<\<\s*%s:internaltemplate\s*\>\>(?P<template>.*)\<\<\s*internaltemplate:internaltemplate_end(\|\w)?\s*\>\>" % varname
        template_chunks = re.findall(pat, template, re.S)
        
        processor = TemplateParser()
        tem = template
        
        for chunk, t in template_chunks:
            returned = ""
            for hook in hooks:
                returned += processor.process(chunk, hook.context, autoresolve=False)
            tem = re.sub(r"\<\<\s*%s:internaltemplate\s*\>\>%s\<\<\s*internaltemplate:internaltemplate_end(\|\w)?\s*\>\>" % (varname, chunk), tem, returned, re.S)
        return tem

class TemplateParser(object):
    _NodeList = {
        'inline' : InlineProcessor,
        'raw': RawProcessor,
        'tuple': TupleProcessor,
        'vartuple': VariableTupleProcessor,
        'var': VariableProcessor,
        'vardict': VariableDictProcessor,
        'dict': DictProcessor,
        'model': ModelProcessor,
        'internaltemplate': InternalTemplateProcessor,
    }
    def __init__(self, reservedContext={}):
        self.reservedContext = reservedContext
        
    def process(self, tmpl, ctx, fileName="foo.bar", autoresolve=True, VERBOSE=False):
        template = process_textblock(tmpl, self.reservedContext)
        tV = get_variables(template)
        for varname, pieces in ctx.items():
            matched = False
            for inp, typ in tV:
                if varname == inp:
                    local =  typ.split('|')[-1].strip('\'\"') if len(typ.split('|')) > 1 else ""
                    typ = typ.split('|')[0]
                    proc = self._NodeList.get(typ, RawProcessor)
                    if varname in [x[0] for x in get_variables(template)]:
                        template = proc._process(varname, template, pieces, local)
                    matched = True
                    
            if not matched:
                if varname == '-':
                    template = AppendProcessor._process("", template, pieces, "")
                    matched = True
                elif varname == 'import' and fileName[-3] == ".py":
                    template = PrependProcessor._process("", template, pieces, "")
                    matched = True
                elif autoresolve:
                    if VERBOSE:
                        try:
                            print pieces[0].s
                        except:
                            pass
                        print "\n    *********************"
                        print "    *  Variable Unmatched:'%s'" % (varname)
                        print "    *     Attempting to Add Variable...."
                    template += "\n\n<< %s:var >>" % (varname)
                    if len(pieces) > 1:
                        template = TupleProcessor._process(varname, template, pieces, "")
                        if VERBOSE:
                            print "    *     *Interpretting %s as tuple" % (varname)
                    elif len(pieces) == 1:
                        template = VariableProcessor._process(varname, template, pieces, "")
                        if VERBOSE:
                            print "    *     *Interpretting %s as variable" % (varname)
                    if VERBOSE:
                        print "    *********************"
        remaining_variables = get_variables(template)
        if len(remaining_variables):
            if VERBOSE:
                print "\n    *********************"
                print "    *  Warning Detected Remaining Variables on Template:"
                for varName, value in remaining_variables:
                    print "    *  > %s" % (varName)
                if autoresolve:
                    print "    *  Removing Variables From Template"
                    for var, typ in remaining_variables:
                        template = process_textblock(template, {var: ""})
                print "    *********************"                

        return template

def quickTemplateStr(string, ctx):
    for key in ctx.keys(): ctx[key] = [ctx[key]]
    return TemplateParser({}).process(string, ctx, "")
