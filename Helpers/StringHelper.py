

class StringHelper(object):

     @staticmethod
     def insertChar(mystring, position, chartoinsert):
         longi = len(mystring)
         mystring   =  mystring[:position] + chartoinsert + mystring[position:] 
         return mystring  

