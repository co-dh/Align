from functools import partial 
from inspect import getargspec, isfunction
from lam import id_func, s2f                                                                                              
import copy ,re 

def ignore_extra_args(f):
	if isfunction(f):
		(args, varargs, keywords, defaults) = getargspec(f)
		n = len(args)
		return lambda *args : f( * args[:n])
	else:
		return f 

class ColSelector():
	def __init__(self, itab1):
		self.itab = itab1 
	def __getitem__(self, selector):
		return self.itab[ :, selector].unzip() 

class itab(list):
	' table (2D list)'

	def map(self, updater, selector = slice(None)):
		rsel = sel(selector)
		func = ignore_extra_args(s2f(updater))
		return itab( [ func(row,i) for i,row in enumerate(self)
						if rsel(row,i) ] )

	def each(self, updater, selector = slice(None)):
		rsel = sel(selector)
		func = ignore_extra_args(s2f(updater))
		for i, row in enumerate(self):
			if rsel(row, i):
				self[i] = func(row, i)
		return self

	def _each_col(self):
		return ColSelector(self) 
	each_col = property(_each_col)

	def each_cell(self, f): self[:,:] = f; return self 
	def copy   (self     ): return copy.copy(self)
	def deepcopy(self     ): return copy.deepcopy(self)
	def _      (self, f  ): return s2f(f)(self)
	def join_by(self, sep): return sep.join(self)
	def equal  (self, v  ): assert self == v, locals();   return self
	def sort   (self     ): list.sort(self); 	return self
	def reverse(self     ): list.reverse(self);	return self 	
	def uniq   (self     ): return itab(set(self))
	def concat (self     ): return itab(self.reduce(operator.add, []))
	def log    (self,s=''): print s,self; return self
	def zip    (self     ): return itab( zip(*self)) 
	def unzip  (self     ): 
		return itab([ itab([ row[col] for row in self ]) 
			for col in range(len(self[0])) ])

	def partial(self, f): return partial(f,self)

	def __getslice__(self,i ,j):
		return self.__getitem__(slice(i,j))

	def __setslice__(self,i ,j, val):
		return self.__getitem__(slice(i,j), val)

	def __getitem__(self, selectors):
		try:
			return list.__getitem__(self, selectors)
		except:
			if type(selectors) == tuple:
				assert len(selectors) == 2
				rows , cols = selectors 
				rsel = sel(rows)
				csel = sel(cols)
				ret = [ itab([ cell for j, cell in enumerate(row) if csel(cell, j)])
									for i, row in enumerate(self) if rsel(row,i)]
				return itab(ret)
			else:
				# return selected row 
				rsel = sel(selectors)
				return itab([ row for (i,row) in enumerate(self) if rsel(row,i)])

	def __setitem__(self, selectors, updater):
		try:
			list.__setitem__(self, selectors, updater)
		except:
			func = ignore_extra_args(s2f(updater))
			if type(selectors) == tuple:
				assert len(selectors) == 2
				rows , cols = selectors 
				rsel = sel(rows)
				csel = sel(cols)
				for i, row in enumerate(self):
					if rsel(row,i):
						for j, cell in enumerate(row):
						 	if csel(cell, j): 
								row[j] = func(cell, i, j)
			else:
				rsel = sel(selectors)
				# return selected row 
				for i, row in enumerate(self):
					if rsel(row, i):
						self[i] = func(row, i)

	def _tablize(self, sep):
		'''Given a list of strings, and a seperator char sep, 
		append seps to the end each string to make all strings has the same 
		number of sep. '''
		extras = self.map( lambda x : x.count(sep))
		max_sep = max(extras)
		extras.each( lambda x: sep * (max_sep - x))
		self.each( lambda row, i : (row + extras[i]).split(sep))
		return  extras

	def _untablize(self, extras, sep ):
		''' the converse of tablize.
		extras : e.g. [ ':', '', '::'], extra seperator that need to be 
			removed from the end of each str . 
		if str is 'abc: def  : :', extra is '::', then the 
		   last 2 :: need to be removed 
		'''
		extras.each( lambda e : re.escape(e).replace(sep, sep + ' *') + '$' )
		return self.each( lambda strs, i : re.sub(extras[i], '', sep.join(strs)))

	def tab_untab(self, sep, func):
		extras = self._tablize(sep )
		s2f(func)(self)

		self._untablize(extras, sep )
		return self

import sys
def sel(rows):
	if   type(rows) == int : return lambda val,i : i == rows 
	elif type(rows) == str : return ignore_extra_args(s2f(rows))	
	elif type(rows) == slice:
		def in_slice(val, i):
			start = rows.start or 0
			stop  = sys.maxint if rows.stop == None else rows.stop
			r =  start <= i < stop 
			#print i, rows, r 
			if rows.step:
				return r and ((i - rows.start)  % rows.step == 0)
			else:
				return r 
		return in_slice
	else 				   : return ignore_extra_args(rows)


