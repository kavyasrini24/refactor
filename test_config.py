import unittest
import os
from config import get_dynamic_file_paths, extract_variables, search_in_xml, search_in_properties

class TestConfig(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Move up one directory to the project root
        cls.test_data_dir = os.path.join(cls.base_dir, 'test_data')
        cls.application_properties_file = os.path.join(cls.test_data_dir, 'application.properties')
        cls.environment_properties_file = os.path.join(cls.test_data_dir, 'environment.properties')
        cls.xml_file = os.path.join(cls.test_data_dir, 'test.xml')

    def test_get_dynamic_file_paths(self):
        paths = get_dynamic_file_paths()
        self.assertEqual(paths[0], self.application_properties_file)
        self.assertEqual(paths[1], self.environment_properties_file)

    def test_extract_variables(self):
        variables = extract_variables(self.application_properties_file)
        print(f"Extracted variables: {variables}")  # Debug line to print the extracted variables
        self.assertIn('variable_name', variables)

    def test_search_in_xml(self):
        variables = {'test_variable': set()}
        variables = search_in_xml(self.xml_file, variables)
        self.assertIn('test_value', variables['test_variable'])

    def test_search_in_properties(self):
        variables = {'env_variable': set()}
        variables = search_in_properties(self.environment_properties_file, variables)
        self.assertIn('env_value', variables['env_variable'])

if __name__ == '__main__':
    unittest.main()
