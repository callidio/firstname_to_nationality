"""
Unit tests for firstname_to_nationality package.
"""

import unittest
from unittest.mock import patch, Mock
from firstname_to_nationality import predict_nationality, NationalityPredictor


class TestNationalityPredictor(unittest.TestCase):
    """Test cases for NationalityPredictor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.predictor = NationalityPredictor()
    
    def test_init_without_api_key(self):
        """Test initialization without API key"""
        predictor = NationalityPredictor()
        self.assertIsNone(predictor.api_key)
    
    def test_init_with_api_key(self):
        """Test initialization with API key"""
        predictor = NationalityPredictor(api_key="test_key")
        self.assertEqual(predictor.api_key, "test_key")
    
    @patch('firstname_to_nationality.predictor.requests.get')
    def test_predict_successful(self, mock_get):
        """Test successful prediction"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "country": [
                {"country_id": "US", "probability": 0.0453},
                {"country_id": "AU", "probability": 0.0382}
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.predictor.predict("Michael")
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["country_id"], "US")
        self.assertEqual(result[0]["probability"], 0.0453)
        self.assertEqual(result[1]["country_id"], "AU")
    
    @patch('firstname_to_nationality.predictor.requests.get')
    def test_predict_sorted_by_probability(self, mock_get):
        """Test that results are sorted by probability in descending order"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "country": [
                {"country_id": "AU", "probability": 0.0382},
                {"country_id": "US", "probability": 0.0453},
                {"country_id": "GB", "probability": 0.0250}
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.predictor.predict("Michael")
        
        # Check that results are sorted by probability
        self.assertEqual(result[0]["country_id"], "US")
        self.assertEqual(result[1]["country_id"], "AU")
        self.assertEqual(result[2]["country_id"], "GB")
    
    def test_predict_empty_name(self):
        """Test prediction with empty name"""
        with self.assertRaises(ValueError):
            self.predictor.predict("")
    
    def test_predict_invalid_name(self):
        """Test prediction with invalid name type"""
        with self.assertRaises(ValueError):
            self.predictor.predict(None)
        
        with self.assertRaises(ValueError):
            self.predictor.predict(123)
    
    @patch('firstname_to_nationality.predictor.requests.get')
    def test_predict_api_error(self, mock_get):
        """Test handling of API errors"""
        mock_get.side_effect = Exception("API Error")
        
        with self.assertRaises(Exception) as context:
            self.predictor.predict("Michael")
        
        self.assertIn("Error fetching nationality data", str(context.exception))
    
    @patch('firstname_to_nationality.predictor.requests.get')
    def test_get_most_probable_nationality(self, mock_get):
        """Test getting the most probable nationality"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "country": [
                {"country_id": "US", "probability": 0.0453},
                {"country_id": "AU", "probability": 0.0382}
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.predictor.get_most_probable_nationality("Michael")
        
        self.assertEqual(result["country_id"], "US")
        self.assertEqual(result["probability"], 0.0453)
    
    @patch('firstname_to_nationality.predictor.requests.get')
    def test_get_most_probable_nationality_empty_result(self, mock_get):
        """Test getting most probable nationality when no results"""
        mock_response = Mock()
        mock_response.json.return_value = {"country": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.predictor.get_most_probable_nationality("UnknownName")
        
        self.assertIsNone(result)
    
    @patch('firstname_to_nationality.predictor.requests.get')
    def test_predict_with_api_key(self, mock_get):
        """Test that API key is sent in request"""
        predictor = NationalityPredictor(api_key="test_api_key")
        mock_response = Mock()
        mock_response.json.return_value = {"country": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        predictor.predict("John")
        
        # Check that API key was included in the request
        call_args = mock_get.call_args
        self.assertIn("apikey", call_args[1]["params"])
        self.assertEqual(call_args[1]["params"]["apikey"], "test_api_key")


class TestPredictNationalityFunction(unittest.TestCase):
    """Test cases for predict_nationality convenience function"""
    
    @patch('firstname_to_nationality.predictor.requests.get')
    def test_predict_nationality_function(self, mock_get):
        """Test the convenience function"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "country": [
                {"country_id": "US", "probability": 0.0453}
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = predict_nationality("Michael")
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["country_id"], "US")
    
    @patch('firstname_to_nationality.predictor.requests.get')
    def test_predict_nationality_with_api_key(self, mock_get):
        """Test the convenience function with API key"""
        mock_response = Mock()
        mock_response.json.return_value = {"country": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        predict_nationality("John", api_key="test_key")
        
        # Check that API key was included in the request
        call_args = mock_get.call_args
        self.assertIn("apikey", call_args[1]["params"])
        self.assertEqual(call_args[1]["params"]["apikey"], "test_key")


if __name__ == '__main__':
    unittest.main()
