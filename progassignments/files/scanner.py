#  
#   A scanner class for Python
#
#   written by John C. Lusth
#
#   Fine, old-world, made-by-hand craftsmanship!
#
#   Examples:
#    
#       from scanner import Scanner
#
#       s = Scanner("myFile");               # read from a file
#
#       s = Scanner("")                      # read from stdin
#
#       s = Scanner("")                      # to read from a string, create,
#       s.fromstring("now is the time")      # then set the input string
#
#       t = s.readtoken()       # read the next whitespace delimited token
#       c = s.readchar()        # read the next non-whitespace character
#       c = s.readrawchar()     # read the next character (whitespace or not)
#       b = s.readbool()        # read a Boolean value
#       i = s.readint()         # read an integer
#       r = s.readfloat()       # read a real number
#                               # does not read scientific notation, like 2e10
#       p = s.readstring()      # read a double-quote delimited string
#                               # the double quotes are left on the string
#       q = s.readline()        # read the rest of the current or the next line
#                               # if at the end of the current line
#
#  The read functions return an empty string if the read failed for any reason
#
#       s.setWhitespace(str) # sets what the scanner considers whitespace to
#                            # the characters in str
#

import sys

class Scanner:

    def __init__(self,fileName):
        if fileName == '':
            self.input = sys.stdin
        else:
            self.input = open(fileName,'r')#,encoding="utf-8")
        self.index = 0
        self.length = 0
        self.pushedBackList = []
        self.closed = False
        self.lineNumber = 0
        self.whitespace = ""

    # close current file and switch input to come from the given string

    def fromstring(self,line):
        self.close()
        self.index = 0
        self.store = line
        self.length = len(line)
        self.pushedBackList = []
        self.lineNumber = 1
        
    def setWhitespace(self,str):
        self.whitespace = str

    # readline works the same as regular python readline

    def readline(self):
        if self.index < self.length:
            result = self.store[self.index:]
        elif self.closed == False:
            result = self.input.readline()
            self.lineNumber += 1
        else:
            result =''

        self.index = 0
        self.length = 0

        return result

    # read and return the next character, even if it is whitespace

    def readrawchar(self):
        ch = self._getNextCharacter()
        return ch

    # read and return the next non-whitespace character

    def readchar(self):
        self._skipWhiteSpace()
        ch = self._getNextCharacter()
        return ch

    # read and return the next token

    def readtoken(self):
        self._skipWhiteSpace()
        return self._getToken()

    # read and return a string enclosed in quotes

    def readstring(self):
        self._skipWhiteSpace()
        return self._getString()
        
    # read and return an integer

    def readint(self):
        self._skipWhiteSpace()
        return self._getInteger()
        
    # read and return an float

    def readfloat(self):
        self._skipWhiteSpace()
        return self._getReal()

    # read and return a boolean

    def readbool(self):
        self._skipWhiteSpace()
        return self._getBoolean()
        
    def close(self):
        if self.closed == False:
            if self.input != sys.stdin:
                self.input.close()
            self.closed = True

    ############## private functions ####################

    def _getToken(self):
        ch = self._getNextCharacter()

        if ch == '': return ch

        str = ''
        while (ch != '' and not (self._isWhiteSpace(ch))):
            str += ch
            ch = self._getNextCharacter()

        self._pushBack(ch)

        return str

    def _getInteger(self):
        ch = self._getNextCharacter()

        if ch == '': return ch

        str = ''

        if (ch == '-'):
            str = str + ch
            ch = self._getNextCharacter()
            if (not(ch.isdigit())):
                self._pushBack('-')
                return ''
                
        while (ch != '' and ch.isdigit()):
            str += ch
            ch = self._getNextCharacter()

        self._pushBack(ch)

        return int(str)

    def _getReal(self):
        ch = self._getNextCharacter()

        if ch == '': return ch

        str = ''

        if (ch == '-'):
            str = str + ch
            ch = self._getNextCharacter()
            if (not(ch.isdigit()) and ch != '.'):
                self._pushBack(str)
                return ''

        if (ch == '.'):
            str = str + ch
            ch = self._getNextCharacter()
            if (not(ch.isdigit())):
                self._pushBack(str)
                return ''
                
        while (ch != '' and (ch.isdigit() or ch == '.')):
            str += ch
            ch = self._getNextCharacter()

        self._pushBack(ch)

        return float(str)
        
    def _getBoolean(self):
        ch = self._getNextCharacter()

        if ch == '': return ch

        if (ch == 'T'):
            ch = self._getNextCharacter()
            if (ch == 'r'):
                ch = self._getNextCharacter()
                if (ch == 'u'):
                    ch = self._getNextCharacter()
                    if (ch == 'e'):
                        return True
                    else:
                        self._pushBack("Tru" + ch);
                        return ''
                else:
                    self._pushBack("Tr" + ch);
                    return ''
            else:
                self._pushBack("T" + ch);
                return ''
        elif (ch == 'F'):
            ch = self._getNextCharacter()
            if (ch == 'a'):
                ch = self._getNextCharacter()
                if (ch == 'l'):
                    ch = self._getNextCharacter()
                    if (ch == 's'):
                        ch = self._getNextCharacter()
                        if (ch == 'e'):
                            return False
                        else:
                            self._pushBack("Fals" + ch);
                            return ''
                    else:
                        self._pushBack("Fal" + ch);
                        return ''
                else:
                    self._pushBack("Fa" + ch);
                    return ''
            else:
                self._pushBack("F" + ch);
                return ''
        else:
            self._pushBack(ch);
            return ''

    def _getString(self):
        delimiter = self._getNextCharacter() # should be some kind of quote

        if (delimiter == ''): return ''

        if (delimiter == chr(0x2018)):
            delimiter = chr(0x2019)
        elif (delimiter == chr(0x201C)):
            delimiter = chr(0x201D)
        elif (delimiter != '\'' and delimiter != '"'): return ''

        str = ''
        ch = self._getNextCharacter()
        while ch != '' and ch != delimiter:
            if ch == '\\':
                ch = self._getNextCharacter()
                if (ch == ''): return str
                elif (ch == 'n'): str += '\n'
                elif (ch == 't'): str += '\t'
                elif (ch == '\\'): str += '\\'
                else: str += ch
            else:
                str += ch

            ch = self._getNextCharacter()

        return delimiter + str + delimiter

    def _isWhiteSpace(self,ch):
        if (self.whitespace == ""):
            return ch.isspace()
        else:
            return ch in self.whitespace

    def _skipWhiteSpace(self):
        ch = self._getNextCharacter()
        while (ch != '' and self._isWhiteSpace(ch)):
            ch = self._getNextCharacter()
        self._pushBack(ch)

    def _getNextCharacter(self):
        if (self.pushedBackList != []):
            ch = self.pushedBackList[0];
            self.pushedBackList = self.pushedBackList[1:]
            return ch

        if self.index == self.length:
            if self.closed == False:
                self.store = self.input.readline()
                self.lineNumber += 1
            else:
                self.store = ''

            if self.store == '':
                return ''

            self.index = 0
            self.length = len(self.store)

        value = self.store[self.index]
        self.index += 1
        return value
            
    def _pushBack(self,ch):
        for i in ch[::-1]:
            self.pushedBackList = [i] + self.pushedBackList
