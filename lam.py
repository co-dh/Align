import operator
from functools import partial 
                                                                                             
def lam1( str):
	body = 'lambda _: ' + str
	f = eval (body)
	f.__name__ = body
	return f

def id_func(x)	: return x
def _compose(funcs)	: 
	def compose2(f, g): 
		def c(x):		return g(f(x))
		c.__name__ = " [%s].[%s] " % (f.__name__, g.__name__)
		return c
	if len(funcs) == 0: return id_func
	return reduce(compose2, funcs)

def s2f(f):
	if type(f) == str:
		f = _compose( map(partial(lam1), f.split('|'))) 
	elif f == None:
		return id_func
	return f

