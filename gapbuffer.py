'''
Created on 4 Dec 2011

@author: aly
'''
from array import array

class CursorOutOfBoundsException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr("CursorOutOfBoundsException: " + self.value)

class GapBuffer(object):
    '''
    Implementation of a unicode gap buffer to efficiently store mutable strings
    '''
    NULL_CHAR = '\0'
    CHAR_TYPE = 'u'
    
    def __init__(self, size = 2):
        self.__buffer = array(self.CHAR_TYPE,self.NULL_CHAR * size)
        self.__gapstart = 0
        self.__gapend = size - 1  
    
    def cursorCanMoveForward(self):
        return self.__gapend + 1 < len(self.__buffer)

    def cursorCanMoveBackward(self):
        return self.__gapstart - 1 >= 0
        
    def getCursorPosition(self):
        return self.__gapstart
    
    def moveCursorForward(self, distance = 1):        
        for i in range(0, distance):#@UnusedVariable 
            self.__moveCursorForwardByOne()
    
    def __moveCursorForwardByOne(self):
        if self.cursorCanMoveForward():
            new_gapend = self.__gapend + 1
            self.__buffer[self.__gapstart] = self.__buffer[new_gapend]
            self.__gapstart += 1
            self.__gapend += 1
        else:
            raise CursorOutOfBoundsException("Cursor already at end of buffer")
    
    def moveCursorBackward(self, distance = 1):
        for i in range(0, distance):#@UnusedVariable
            self.__moveCursorBackwardByOne()
    
    def __moveCursorBackwardByOne(self):
        if self.cursorCanMoveBackward():
            new_gapstart = self.__gapstart - 1
            self.__buffer[self.__gapend] = self.__buffer[new_gapstart]
            self.__gapend -= 1
            self.__gapstart = new_gapstart
        else:
            raise CursorOutOfBoundsException("Cursor already at end of buffer")
        
    def getText(self):
        bob = []
        for idx, char in enumerate(self.__buffer):
            if idx not in range(self.__gapstart, self.__gapend + 1) and char != self.NULL_CHAR:
                bob.append(char)
        
        return ''.join(bob)
    
    def insert(self, text):
        for character in text:
            self.__insert_single_character(character)
    
    
    def __insert_single_character(self, character):
        if self.__has_gap_space_left():
            self.__increase_buffer_size()
        self.__buffer[self.__gapstart] = character
        self.__gapstart += 1
        
    def __increase_buffer_size(self):
        increase_size = len(self.__buffer)
        extension_array = array(self.CHAR_TYPE, self.NULL_CHAR * increase_size)
        j = -1
        elements_transferred = 0
        for i in range(len(self.__buffer) - 1, self.__gapend - 1, -1):
            extension_array[j] = self.__buffer[i]
            j -= 1
            elements_transferred += 1
        
        self.__gapend = len(self.__buffer) + len(extension_array) + j
        self.__buffer.extend(extension_array)

    def __has_gap_space_left(self):
        return self.__gapstart <= self.__gapend
    