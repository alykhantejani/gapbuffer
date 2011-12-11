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
   
    def test_cursor_position_with_new_buffer_is_zero(self):
        self.assertEqual(0,self.gapbuffer.get_cursor_position())
    
    def test_cursor_cant_be_moved_forward_with_empty_buffer(self):
        self.assertFalse(self.gapbuffer.cursor_can_move_forward())
    
    def test_cursor_cant_be_moved_backward_with_empty_buffer(self):
        self.assertFalse(self.gapbuffer.cursor_can_move_backward())
    
    def test_cursor_cant_be_moved_forward_once_with_emtpy_buffer(self):
        self.assertRaises(CursorOutOfBoundsException, self.gapbuffer.move_cursor_forward)
        self.assertRaises(CursorOutOfBoundsException, self.gapbuffer.move_cursor_forward, 1)

    def test_cursor_cant_be_moved_forward_an_arbitrary_amount_with_empty_buffer(self):
        #3 and 5 are arbitrary constants here
        self.assertRaises(CursorOutOfBoundsException, self.gapbuffer.move_cursor_forward, 3)
        self.assertRaises(CursorOutOfBoundsException, self.gapbuffer.move_cursor_forward, 5)
    
    def test_cursor_cant_be_moved_backward_once_with_empty_buffer(self):
        self.assertRaises(CursorOutOfBoundsException, self.gapbuffer.move_cursor_backward)
        self.assertRaises(CursorOutOfBoundsException, self.gapbuffer.move_cursor_backward, 1)

    def test_cursor_cant_be_moved_backward_an_arbitrary_amount_with_empty_buffer(self):
        self.assertRaises(CursorOutOfBoundsException, self.gapbuffer.move_cursor_backward, 3)
        self.assertRaises(CursorOutOfBoundsException, self.gapbuffer.move_cursor_backward, 5)

    def test_cursor_can_be_moved_backwards_after_insert(self):
        self.gapbuffer.insert('a')
        self.assertTrue(self.gapbuffer.cursor_can_move_backward())
    
    def test_moving_cursor_backwards_after_insert(self):
        self.gapbuffer.insert('a')
        self.assertEqual(1, self.gapbuffer.get_cursor_position())
        self.gapbuffer.move_cursor_backward()
        self.assertEqual(0, self.gapbuffer.get_cursor_position())
        
    def test_moving_cursor_backwards_more_than_one_position_after_insert(self):
        self.gapbuffer.insert("abc")
        self.assertEqual(3, self.gapbuffer.get_cursor_position())
        self.gapbuffer.move_cursor_backward(2)
        self.assertEqual(1, self.gapbuffer.get_cursor_position())
        self.gapbuffer.move_cursor_backward(1)
        self.assertEqual(0, self.gapbuffer.get_cursor_position())
    
    def test_cursor_cant_be_moved_forward_after_only_inserts(self):
        self.gapbuffer = GapBuffer(4)
        self.gapbuffer.insert('a')
        self.assertFalse(self.gapbuffer.cursor_can_move_forward())

    def test_cursor_cant_be_moved_forward_after_only_inserts_in_incorrectly_sized_buffer(self):
        self.gapbuffer = GapBuffer(2)
        self.gapbuffer.insert("abc")
        self.assertFalse(self.gapbuffer.cursor_can_move_forward())

    def test_moving_cursor_forward_once_after_insert_and_moving_backward(self):
        self.gapbuffer.insert('a')
        self.gapbuffer.move_cursor_backward()
        self.gapbuffer.move_cursor_forward()
        self.assertEqual(1, self.gapbuffer.get_cursor_position())
    
    def test_moving_cursor_forwards_more_than_one_position_after_inserts_and_moving_backwards(self):
        self.gapbuffer.insert("abc")
        self.gapbuffer.move_cursor_backward(3)
        self.gapbuffer.move_cursor_forward(2)
        self.assertEqual(2, self.gapbuffer.get_cursor_position())
    
class TextTests(unittest.TestCase):
    def setUp(self):
        self.gapbuffer = GapBuffer()

    def tearDown(self):
        pass

    def test_empty_buffer_gives_empty_text(self):
        self.assertEqual("", self.gapbuffer.get_text())
    
    #all other text tests are covered in the other action tests

class DeleteTests(unittest.TestCase):

    def setUp(self):
        self.gapbuffer = GapBuffer()

    def test_deleting_single_character(self):
        self.gapbuffer.insert("a")
        self.gapbuffer.delete()
        self.assertEqual("", self.gapbuffer.get_text())

    def test_deleting_multiple_characters(self):
        self.gapbuffer.insert("abcd")
        self.gapbuffer.delete()
        self.gapbuffer.delete()
        self.assertEqual("ab", self.gapbuffer.get_text())

    def test_delete_after_moving_cursor(self):
        self.gapbuffer.insert("abcd")
        self.gapbuffer.move_cursor_backward(2)
        self.gapbuffer.delete()
        self.assertEqual("acd", self.gapbuffer.get_text())
      
    def test_cursor_has_correct_position_after_single_delete(self):
        self.gapbuffer.insert("abc")
        self.gapbuffer.delete()
        self.assertEqual(2, self.gapbuffer.get_cursor_position())

    def test_cursor_has_correct_position_after_multiple_delete(self): 
        self.gapbuffer.insert("abc")
        self.gapbuffer.delete()
        self.gapbuffer.delete()
        self.assertEqual(1, self.gapbuffer.get_cursor_position())

    def test_cursor_has_correct_position_after_being_moved_and_delete(self):
        self.gapbuffer.insert("abcd")
        self.gapbuffer.move_cursor_backward(2)
        self.gapbuffer.delete()
        self.assertEqual(1, self.gapbuffer.get_cursor_position())

class InsertTests(unittest.TestCase):
    
    def setUp(self):
        self.gapbuffer = GapBuffer()

    def tearDown(self):
        pass

    def test_insert_one_character(self):
        self.gapbuffer.insert('a')
        self.assertEqual("a", self.gapbuffer.get_text())

    def test_insert_one_characterAsString(self):
        self.gapbuffer.insert("a")
        self.assertEqual("a", self.gapbuffer.get_text())
    
    def test_insert_multiple_character(self):
        self.gapbuffer.insert('a')
        self.gapbuffer.insert('b')
        self.gapbuffer.insert('c')
        self.assertEqual("abc", self.gapbuffer.get_text()) 

    def test_insert_with_multi_character_string(self):
        self.gapbuffer.insert("abc")
        self.assertEqual("abc", self.gapbuffer.get_text())
    
    def test_insert_with_one_special_character(self):
        self.gapbuffer.insert('\n')
        self.assertEqual('\n', self.gapbuffer.get_text())
    
    def test_insert_With_multiple_special_characters(self):
        self.gapbuffer.insert('\t')
        self.gapbuffer.insert('\n')
        self.assertEqual("\t\n", self.gapbuffer.get_text())

    def test_insert_with_multiple_special_character_string(self):
        self.gapbuffer.insert("\t\n")
        self.assertEqual("\t\n", self.gapbuffer.get_text())
    
    def test_insert_on_correct_sized_buffer(self):
        self.gapbuffer = GapBuffer(6)
        self.gapbuffer.insert("hell\no")
        self.assertEqual("hell\no", self.gapbuffer.get_text())

    def test_inser_on_incorrectly_sized_buffer(self):
        self.gapbuffer = GapBuffer(2)
        self.gapbuffer.insert("hell\no")
        self.assertEqual("hell\no", self.gapbuffer.get_text())

    def testCursorHasCorrectPositionAfterInsert(self):
        self.assertEqual(0, self.gapbuffer.get_cursor_position())
        self.gapbuffer.insert('a')
        self.assertEqual(1, self.gapbuffer.get_cursor_position())
    
    def test_cursor_has_correct_position_after_multiple_inserts(self):
        self.assertEqual(0, self.gapbuffer.get_cursor_position())
        self.gapbuffer.insert('a')
        self.gapbuffer.insert('b')
        self.assertEqual(2, self.gapbuffer.get_cursor_position())

    def test_cursor_has_correct_position_after_insert_in_middle_of_buffer(self):
        self.gapbuffer.insert("abef")
        self.gapbuffer.move_cursor_backward(2)
        self.gapbuffer.insert("cd")
        self.assertEqual(4, self.gapbuffer.get_cursor_position())
    
    def test_cursor_has_correct_position_after_multi_character_string_insert(self):
        self.assertEqual(0, self.gapbuffer.get_cursor_position())
        self.gapbuffer.insert("abc")
        self.assertEqual(3, self.gapbuffer.get_cursor_position())

    def test_insert_in_middle_of_buffer_after_moving_cursor(self):
        self.gapbuffer.insert("acd")
        self.gapbuffer.move_cursor_backward(2)
        self.gapbuffer.insert('b')
        self.assertEqual("abcd", self.gapbuffer.get_text())
        
    def test_insert_at_start_of_buffer_after_moving_cursor(self):
        self.gapbuffer.insert("bcd")
        self.gapbuffer.move_cursor_backward(3)
        self.gapbuffer.insert('a')
        self.assertEqual("abcd", self.gapbuffer.get_text())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testInsert']
    unittest.main()
