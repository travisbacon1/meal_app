import unittest
from selenium import webdriver 
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class TestUserInteraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = 'http://127.0.0.1:5000'
        cls.chrome_options = Options()
        cls.chrome_options.add_argument("--headless")

    def setUp(self):
        self.driver = webdriver.Chrome(options=self.chrome_options)


    def tearDown(self):
        self.driver.quit()


    def test_add_meal(self):
        self.driver.get(self.url)
        self.driver.find_element(By.ID, 'Add Meal').click()
        self.assertEqual(self.driver.current_url, f'{self.url}/add')


    def test_edit_meal(self):
        self.driver.get(self.url)
        self.driver.find_element(By.ID, 'Edit Meal').click()
        self.assertEqual(self.driver.current_url, f'{self.url}/edit')


    def test_get_meal_info(self):
        self.driver.get(self.url)
        self.driver.find_element(By.ID, 'Get Meal Info').click()
        self.assertEqual(self.driver.current_url, f'{self.url}/find')


    def test_search_ingredients(self):
        self.driver.get(self.url)
        self.driver.find_element(By.ID, 'Search Ingredients').click()
        self.assertEqual(self.driver.current_url, f'{self.url}/search')


    def test_list_meals(self):
        self.driver.get(self.url)
        self.driver.find_element(By.ID, 'List Meals').click()
        self.assertEqual(self.driver.current_url, f'{self.url}/list_meals')


    def test_create_meal_plan(self):
        self.driver.get(self.url)
        self.driver.find_element(By.ID, 'Create Meal Plan').click()
        self.assertEqual(self.driver.current_url, f'{self.url}/create')


    def test_load_meal_plan(self):
        self.driver.get(self.url)
        self.driver.find_element(By.ID, 'Load Meal Plan').click()
        self.assertEqual(self.driver.current_url, f'{self.url}/load')


    def test_delete_meal_plan(self):
        self.driver.get(self.url)
        self.driver.find_element(By.ID, 'Delete Meal Plan').click()
        self.assertEqual(self.driver.current_url, f'{self.url}/delete')

if __name__ == '__main__':
    unittest.main()