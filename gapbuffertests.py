'''
Created on 4 Dec 2011

@author: aly
'''
import unittest
from gapbuffer import GapBuffer
from gapbuffer import CursorOutOfBoundsException
    
    
class CursorMovementTests(unittest.TestCase):
    
    def setUp(self):
        self.gapbuffer = GapBuffer()
   
    def testCursorPositionWithNewBufferIsZero(self):
        self.assertEqual(0,self.gapbuffer.getCursorPosition())
    
    def testCursorCantBeMovedForwardWithEmptyBuffer(self):
        self.assertFalse(self.gapbuffer.cursorCanMoveForward())
    
    def testCursorCantBeMovedBackwardWithEmptyBuffer(self):
        self.assertFalse(self.gapbuffer.cursorCanMoveBackward())
    
    def testCursorCantBeMovedForwardOnceWithEmtpyBuffer(self):
        self.assertRaises(CursorOutOfBoundsException, self.gapbuffer.moveCursorForward)
        self.assertRaises(CursorOutOfBoundsException, self.gapbuffer.moveCursorForward, 1)

    def testCursorCantBeMovedForwardAnArbitraryAmountWithEmptyBuffer(self):
        #3 and 5 are arbitrary constants here
        self.assertRaises(CursorOutOfBoundsException, self.gapbuffer.moveCursorForward, 3)
        self.assertRaises(CursorOutOfBoundsException, self.gapbuffer.moveCursorForward, 5)
    
    def testCursorCantBeMovedBackwardOnceWithEmptyBuffer(self):
        self.assertRaises(CursorOutOfBoundsException, self.gapbuffer.moveCursorBackward)
        self.assertRaises(CursorOutOfBoundsException, self.gapbuffer.moveCursorBackward, 1)

    def testCursorCantBeMovedBackwardAnArbitraryAmountWithEmptyBuffer(self):
        self.assertRaises(CursorOutOfBoundsException, self.gapbuffer.moveCursorBackward, 3)
        self.assertRaises(CursorOutOfBoundsException, self.gapbuffer.moveCursorBackward, 5)

    def testCursorCanBeMovedBackwardsAfterInsert(self):
        self.gapbuffer.insert('a')
        self.assertTrue(self.gapbuffer.cursorCanMoveBackward())
    
    def testMovingCursorBackwardsAfterInsert(self):
        self.gapbuffer.insert('a')
        self.assertEqual(1, self.gapbuffer.getCursorPosition())
        self.gapbuffer.moveCursorBackward()
        self.assertEqual(0, self.gapbuffer.getCursorPosition())
        
    def testMovingCursorBackwardsMoreThanOnePositionAfterInsert(self):
        self.gapbuffer.insert("abc")
        self.assertEqual(3, self.gapbuffer.getCursorPosition())
        self.gapbuffer.moveCursorBackward(2)
        self.assertEqual(1, self.gapbuffer.getCursorPosition())
        self.gapbuffer.moveCursorBackward(1)
        self.assertEqual(0, self.gapbuffer.getCursorPosition())
    
    def testCursorCantBeMovedForwardAfterOnlyInserts(self):
        self.gapbuffer = GapBuffer(4)
        self.gapbuffer.insert('a')
        self.assertFalse(self.gapbuffer.cursorCanMoveForward())

    def testCursorCantBeMovedForwardAfterOnlyInsertsInIncorrectlySizedBuffer(self):
        self.gapbuffer = GapBuffer(2)
        self.gapbuffer.insert("abc")
        self.assertFalse(self.gapbuffer.cursorCanMoveForward())

    def testMovingCursorForwardOnceAfterInsertAndMovingBackward(self):
        self.gapbuffer.insert('a')
        self.gapbuffer.moveCursorBackward()
        self.gapbuffer.moveCursorForward()
        self.assertEqual(1, self.gapbuffer.getCursorPosition())
    
    def testMovingCursorForwardsMoreThanOnePositionAfterInsertsAndMovingBackwards(self):
        self.gapbuffer.insert("abc")
        self.gapbuffer.moveCursorBackward(3)
        self.gapbuffer.moveCursorForward(2)
        self.assertEqual(2, self.gapbuffer.getCursorPosition())
    
class TextTests(unittest.TestCase):
    def setUp(self):
        self.gapbuffer = GapBuffer()

    def tearDown(self):
        pass

    def testEmptyBufferGivesEmptyText(self):
        self.assertEqual("", self.gapbuffer.getText())
    
    #all other text tests are covered in the other action tests

class InsertTests(unittest.TestCase):
    
    def setUp(self):
        self.gapbuffer = GapBuffer()

    def tearDown(self):
        pass

    def testInsertOneCharacter(self):
        self.gapbuffer.insert('a')
        self.assertEqual("a", self.gapbuffer.getText())

    def testInsertOneCharacterAsString(self):
        self.gapbuffer.insert("a")
        self.assertEqual("a", self.gapbuffer.getText())
    
    def testInsertMultipleCharacter(self):
        self.gapbuffer.insert('a')
        self.gapbuffer.insert('b')
        self.gapbuffer.insert('c')
        self.assertEqual("abc", self.gapbuffer.getText()) 

    def testInsertWithMultiCharacterString(self):
        self.gapbuffer.insert("abc")
        self.assertEqual("abc", self.gapbuffer.getText())
    
    def testInsertWithOneSpecialCharacter(self):
        self.gapbuffer.insert('\n')
        self.assertEqual('\n', self.gapbuffer.getText())
    
    def testInsertWithMultipleSpecialCharacters(self):
        self.gapbuffer.insert('\t')
        self.gapbuffer.insert('\n')
        self.assertEqual("\t\n", self.gapbuffer.getText())

    def testInsertWithMultiplseSpecialCharacterString(self):
        self.gapbuffer.insert("\t\n")
        self.assertEqual("\t\n", self.gapbuffer.getText())
    
    def testInsertOnCorrectlySizedBuffer(self):
        self.gapbuffer = GapBuffer(6)
        self.gapbuffer.insert("hell\no")
        self.assertEqual("hell\no", self.gapbuffer.getText())

    def testInsertOnIncorrectlySizedBuffer(self):
        self.gapbuffer = GapBuffer(2)
        self.gapbuffer.insert("hell\no")
        self.assertEqual("hell\no", self.gapbuffer.getText())

    def testCursorHasCorrectPositionAfterInsert(self):
        self.assertEqual(0, self.gapbuffer.getCursorPosition())
        self.gapbuffer.insert('a')
        self.assertEqual(1, self.gapbuffer.getCursorPosition())
    
    def testCursorHasCorrectPositionAfterMultipleInserts(self):
        self.assertEqual(0, self.gapbuffer.getCursorPosition())
        self.gapbuffer.insert('a')
        self.gapbuffer.insert('b')
        self.assertEqual(2, self.gapbuffer.getCursorPosition())
    
    def testCursorHasCorrectPositionAfterMultiCharacterStringInsert(self):
        self.assertEqual(0, self.gapbuffer.getCursorPosition())
        self.gapbuffer.insert("abc")
        self.assertEqual(3, self.gapbuffer.getCursorPosition())

    def testInsertInMiddleOfBufferAfterMovingCursor(self):
        self.gapbuffer.insert("acd")
        self.gapbuffer.moveCursorBackward(2)
        self.gapbuffer.insert('b')
        self.assertEqual("abcd", self.gapbuffer.getText())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testInsert']
    unittest.main()
