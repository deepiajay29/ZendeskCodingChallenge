import os
import json
import unittest
import DataParser_Map

class TestUserInput(unittest.TestCase):
    def test_UserId(self):
        """
        Test for UserId search 
        """
        testresult = {}
        testresult = DataParser_Map.advanceSearch("1","_id","1")
        #print(testresult)
        self.assertEqual(testresult[0]["_id"], 1, "User Id Failed")
        self.assertEqual(testresult[0]["Organisation_Name"][0], "Multron", "User Id Failed")
        
        testresult = DataParser_Map.advanceSearch("1","_id","999")
        #print(testresult)
        self.assertEqual(testresult, {}, "User Id match failed")
        
    def test_TicketId(self):
        """
        Test for TicketId search
        """
        testresult = {}
        testresult = DataParser_Map.search("2","_id","1a227508-9f39-427c-8f57-1b72f3fab87c")
        #print(testresult)
        self.assertEqual(testresult[0]["_id"], "1a227508-9f39-427c-8f57-1b72f3fab87c", "Ticket Id Not Found")
        
        testresult = DataParser_Map.search("2","_id","999")
        #print(testresult)
        self.assertEqual(testresult, {}, "Ticket Id match failed")
        
    def test_Organisation(self):
        """
        Test for Organisation search
        """
        testresult = {}
        testresult = DataParser_Map.search("3","_id","118")
        #print(testresult)
        self.assertEqual(testresult[0]["_id"], 118, "Org Id Not Found")
        
        testresult = DataParser_Map.search("3","_id","999")
        #print(testresult)
        self.assertEqual(testresult, {}, "Org Id match failed")
 
if __name__ == '__main__':
    DataParser_Map.createHashMap()
    unittest.main()