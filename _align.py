from  itab import itab

def align(self, cols ):
	'align a list of strings by append space'
	widths = self[:, cols].each_cell('len(_)').each_col[ cols ].each( 'max(_)')
	self[: , cols] =  lambda _ , row,col: _.ljust(widths[col]) 
	return self

from functools import partial 
class String(str):

	def align_at(self, char,  count = 1): 
		def align_lines(strs):
			return itab(strs).tab_untab(char,  partial(align, cols = slice(count)) )
		return self.split_join(align_lines, sep ='\n')
	
	def split_join( self, func, sep = ' ', *args  ):
		r =  ( itab(self.split(sep, *args))
					._(func)
					.join_by(sep)
				)
		return String(r) 

 
