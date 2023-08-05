import unittest
from unittest.mock import patch, MagicMock
from text_block import TextBlocks
#from circles_text_block_local.text_block_microservice import TextBlocks
from datetime import datetime

class TestTexBlock(unittest.TestCase):
     
    def setUp(self):
        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor

        self.tester = TextBlocks(datetime.strptime("2023-07-20 12:34:56", "%Y-%m-%d %H:%M:%S"))
        self.text = '''Ian Golding  1st degree connection1st
            Global Customer Experience Specialist and Certified Customer Experience Professional (CCXP)
            Talks about #cx, #customercentric, #customerjourney, #customerexperience, and #customerjourneymanagementTalks about hashtag cx, hashtag customercentric, hashtag customerjourney, hashtag customerexperience, and hashtag customerjourneymanagement
            Cemantica
            Brunel University London
            Greater Cheshire West and Chester Area  Contact info
            https://ijgolding.com'''

    @patch('circles_text_block_local.text_block_microservice.db_connection')
    def test_process_text_block_valid_regex(self, mock_connection):
        self.mock_cursor = mock_connection.cursor()

        self.tester.process_text_block((6,))
        self.mock_cursor.execute.assert_any_call("SELECT text, text_block_type_id, profile_id FROM text_block.text_block_table WHERE id = '6'")
        self.mock_cursor.execute.assert_any_call("INSERT INTO email_address.email_address_table (email) VALUES ('ian@ijgolding.com')")
        self.mock_cursor.execute.assert_any_call('UPDATE text_block.text_block_table SET fields_extracted_json = "{"Email": ["ian@ijgolding.com"], "Phone Number": [], "Website": []}" WHERE id = 6')

    @patch('circles_text_block_local.text_block_microservice.db_connection')
    def test_process_text_block_invalid_regex(self, mock_connection):
        self.mock_cursor = mock_connection.cursor()

        self.tester.process_text_block((1,))
        self.mock_cursor.execute.assert_any_call("SELECT text, text_block_type_id, profile_id FROM text_block.text_block_table WHERE id = '1'")
        self.mock_cursor.execute.assert_any_call("UPDATE text_block.text_block_table SET fields_extracted_json = '{}' WHERE id = 1")

    @patch('circles_text_block_local.text_block_microservice.db_connection')
    def test_identify_text_block_type(self, mock_connection):
        self.mock_cursor = mock_connection.cursor()

        result = self.tester.identify_text_block_type(4, self.text)
        self.assertEqual(result, 9)

    @patch('circles_text_block_local.text_block_microservice.db_connection')
    def test_identify_text_block_type_none(self, mock_connection):
        self.mock_cursor = mock_connection.cursor()

        result = self.tester.identify_text_block_type(1, '''Nick Gelman, CPA  1st degree connection1st
            Director of Finance at Adept

            adept

            The College of Management Academic Studies
            Israel''')
        self.assertEqual(result, None)

    @patch('circles_text_block_local.text_block_microservice.db_connection')
    def test_update_text_block_type(self, mock_connection):
        self.mock_cursor = mock_connection.cursor()
        self.mock_cursor.execute("UPDATE text_block.text_block_table SET text_block_type_id = 4 WHERE id = 4")


        self.tester.identify_and_update_text_block_type(4, self.text)
        self.mock_cursor.execute.assert_any_call("UPDATE text_block.text_block_table SET text_block_type_id = 9 WHERE id = 4")

    @patch('circles_text_block_local.text_block_microservice.db_connection') 
    def test_update_logger_with_old_and_new_field_value(self, mock_connection):
        self.mock_cursor = mock_connection.cursor()

        self.tester.update_logger_with_old_and_new_field_value(38, "test_old", "test_new")

        self.mock_cursor.execute.assert_any_call("INSERT INTO logger.logger_table (field_id, field_value_old, field_value_new) VALUES (0, test_old, test_new)")
    
if __name__ == '__main__':
    unittest.main()
    