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
        self.__buffer = [self.NULL_CHAR for x in range(0,size)]
        self.__gapstart = 0
        self.__gapend = size - 1  
    
    def cursor_can_move_forward(self):
        return self.__gapend + 1 < len(self.__buffer)

    def cursor_can_move_backward(self):
        return self.__gapstart - 1 >= 0
        
    def get_cursor_position(self):
        return self.__gapstart
    
    def move_cursor_forward(self, distance = 1):        
        for i in range(0, distance):#@UnusedVariable 
            self._move_cursor_forward_by_one()
    
    def _move_cursor_forward_by_one(self):
        if self.cursor_can_move_forward():
            new_gapend = self.__gapend + 1
            self.__buffer[self.__gapstart] = self.__buffer[new_gapend]
            self.__gapstart += 1
            self.__gapend += 1
        else:
            raise CursorOutOfBoundsException("Cursor already at end of buffer")
    
    def move_cursor_backward(self, distance = 1):
        for i in range(0, distance):#@UnusedVariable
            self._move_cursor_backward_by_one()
    
    def _move_cursor_backward_by_one(self):
        if self.cursor_can_move_backward():
            new_gapstart = self.__gapstart - 1
            self.__buffer[self.__gapend] = self.__buffer[new_gapstart]
            self.__gapend -= 1
            self.__gapstart = new_gapstart
        else:
            raise CursorOutOfBoundsException("Cursor already at start of buffer")
        
    def get_text(self):
        bob = []
        for idx, char in enumerate(self.__buffer):
            if idx not in range(self.__gapstart, self.__gapend + 1) and char != self.NULL_CHAR:
                bob.append(char)
        
        return ''.join(bob)
    
    def insert(self, text):
        for character in text:
            self._insert_single_character(character)
    
    def _insert_single_character(self, character):
        if not self._has_gap_space_left():
            self._increase_buffer_size()
        self.__buffer[self.__gapstart] = character
        self.__gapstart += 1
        
    def _increase_buffer_size(self):
        increase_size = len(self.__buffer)
        extension_list = [ self.NULL_CHAR for x in range(0, increase_size) ]
        j = -1
        elements_transferred = 0

        for idx in range(len(self.__buffer) - 1, self.__gapend, -1):
            extension_list[j] = self.__buffer[idx]
            j -= 1
            elements_transferred += 1
        
        self.__gapend = len(self.__buffer) + len(extension_list) + j
        self.__buffer.extend(extension_list)

    def _has_gap_space_left(self):
        return self.__gapstart <= self.__gapend
    
    def delete(self):
        if self._can_delete():
            self.__gapstart -= 1

    def _can_delete(self):
        return self.__gapstart != 0
