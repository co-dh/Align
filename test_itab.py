from itab import * 

@ignore_extra_args
def __f0(): return 0 
@ignore_extra_args
def __f1(x): return x 
@ignore_extra_args
def __f2(x,y): return (x+y)
assert __f0(3,2,3) == 0 
assert __f1(0,1,2) == 0
assert __f2('a','b',1) == 'ab'


assert sel(slice(None, 0, None))('col', 0) == False 

def test1():
	i = itab([[1,2,3,4,5],[11,12,13,14,15]])	
	assert i[0] == [1,2,3,4,5]
	assert i[0,0] == [[1]]

	def even_idx(val, i) : return i%2 == 0 
	assert i[even_idx , : ] == [[1,2,3,4,5]]
	assert i[ even_idx  , '_%2 == 0'] == [[2,4]]
	
	assert i[even_idx]  == [[1,2,3,4,5]]
	assert i[:, 1:3] == [[2,3], [12,13]]

	from copy import deepcopy as D 
	i[:,:] = '_*3 '
	assert i == [[3, 6, 9, 12, 15], [33, 36, 39, 42, 45]]

	def even(x): return x %2 == 0 

	i[ even_idx , even] = '_/2'
	assert i == [[3, 3, 9, 6, 15], [33, 36, 39, 42, 45]]

	d = [[1,2,3], [11,12,13]]
	i = itab(D(d))  
	i[0] = 'sum(_)'
	assert i == ['sum(_)' , [11,12,13]]

	i = itab(D(d))  
	i.each('sum(_)', selector = 1)
	assert i == [[1,2,3] ,36]

	i = itab(D(d))  
	i.each('sum(_)')
	assert i == [6 ,36]

	i = itab(D(d))  
	i.each( 'sum(_)' , selector =  even_idx)
	assert i == [6 ,[11,12,13]]

	assert itab([])[1,1]  == []
	assert itab([[]])[1,2] == []
	# i.each_row[0]  this will assert
	i = itab([[1,2,3,4,5],[11,12,13,14,15]])	
	assert i.each_col[:] == [[1, 11], [2, 12], [3, 13], [4, 14], [5, 15]]
	assert i.each_col[even_idx ] == [[1, 11], [3, 13], [5, 15]]
	assert i[:, even] ==[[2,4],[12,14]] # select all even elements
	assert itab([[1,2,3]])[ : , :0]  == [[]]

test1()

from _align import String 
	
_t1 = '''1 colon: 123
12 : what ? two : colons? 
aaa
  
    indented : part2 : part3 : part4 '''
  
_t2 = itab(_t1.split('\n') )    
assert _t2 == _t2.copy().tab_untab(':', None)
assert String(_t1).align_at(':', 2) == '''1 colon      : 123        
12           : what ? two : colons? 
aaa          
             
    indented : part2      : part3 : part4 '''
  
ss = '''
	def each_cell(self, f): self[:,:] = f; return self
	def copy (self): return copy.copy(self)
'''
res = String(ss).align_at('(').align_at(')').align_at('return')  
expected  = '''
	def each_cell(self, f): self[:,:] = f; return self
	def copy     (self   ):                return copy.copy(self)
'''

assert res.strip() == expected.strip()

s = '''
		v = self.view
		reg = v.sel()[0]

		begin = reg.begin()
		row, col = v.rowcol(reg.end())

		char = v.substr(reg.end() - 1)
		reg = v.line(reg)
'''
print String(s).align_at('=')
