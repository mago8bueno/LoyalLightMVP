#!/usr/bin/env python3
"""
LoyalLight MVP Backend API Testing Suite

Comprehensive testing of the refactored FastAPI backend with modular architecture.
Tests all API endpoints and validates the integration between components.
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional


class LoyalLightAPITester:
    """Comprehensive API testing class for LoyalLight MVP backend."""
    
    def __init__(self, base_url: str = "https://fadeb4d3-2d92-4c85-8904-145f357d2e3f.preview.emergentagent.com"):
        """
        Initialize the API tester.
        
        Args:
            base_url: Base URL for the API (using public endpoint)
        """
        self.base_url = base_url
        self.api_base = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []
        
        # Test session for connection reuse
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'LoyalLight-API-Tester/1.0'
        })
    
    def log_test_result(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test result for reporting."""
        result = {
            'test_name': test_name,
            'success': success,
            'details': details,
            'response_data': response_data,
            'timestamp': datetime.utcnow().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} | {test_name}")
        if details:
            print(f"      Details: {details}")
        if not success and response_data:
            print(f"      Response: {response_data}")
        print()
    
    def run_test(self, test_name: str, method: str, endpoint: str, 
                 expected_status: int, data: Optional[Dict] = None,
                 validate_response: Optional[callable] = None) -> tuple[bool, Any]:
        """
        Run a single API test.
        
        Args:
            test_name: Descriptive name for the test
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (without /api prefix)
            expected_status: Expected HTTP status code
            data: Request payload for POST requests
            validate_response: Optional function to validate response content
            
        Returns:
            Tuple of (success, response_data)
        """
        url = f"{self.api_base}/{endpoint.lstrip('/')}"
        self.tests_run += 1
        
        try:
            # Make the request
            if method.upper() == 'GET':
                response = self.session.get(url, timeout=10)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            # Check status code
            status_ok = response.status_code == expected_status
            
            # Parse response
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                response_data = response.text
            
            # Validate response content if validator provided
            content_ok = True
            validation_details = ""
            
            if validate_response and status_ok:
                try:
                    content_ok = validate_response(response_data)
                    if not content_ok:
                        validation_details = "Response content validation failed"
                except Exception as e:
                    content_ok = False
                    validation_details = f"Validation error: {str(e)}"
            
            # Overall success
            success = status_ok and content_ok
            
            if success:
                self.tests_passed += 1
                details = f"Status: {response.status_code}"
            else:
                if not status_ok:
                    details = f"Expected status {expected_status}, got {response.status_code}"
                else:
                    details = validation_details
            
            self.log_test_result(test_name, success, details, response_data if not success else None)
            return success, response_data
            
        except requests.exceptions.RequestException as e:
            details = f"Request failed: {str(e)}"
            self.log_test_result(test_name, False, details)
            return False, None
        except Exception as e:
            details = f"Unexpected error: {str(e)}"
            self.log_test_result(test_name, False, details)
            return False, None
    
    def validate_hello_world_response(self, response_data: Any) -> bool:
        """Validate the hello world endpoint response."""
        return (
            isinstance(response_data, dict) and
            'message' in response_data and
            response_data['message'] == 'Hello World'
        )
    
    def validate_status_check_creation(self, response_data: Any) -> bool:
        """Validate status check creation response."""
        if not isinstance(response_data, dict):
            return False
        
        required_fields = ['id', 'client_name', 'timestamp']
        return all(field in response_data for field in required_fields)
    
    def validate_status_check_list(self, response_data: Any) -> bool:
        """Validate status check list response."""
        if not isinstance(response_data, list):
            return False
        
        # If list is not empty, validate first item structure
        if response_data:
            first_item = response_data[0]
            required_fields = ['id', 'client_name', 'timestamp']
            return all(field in first_item for field in required_fields)
        
        return True  # Empty list is valid
    
    def test_health_check(self) -> bool:
        """Test the root health check endpoint."""
        success, _ = self.run_test(
            test_name="Health Check (GET /api/)",
            method="GET",
            endpoint="/",
            expected_status=200,
            validate_response=self.validate_hello_world_response
        )
        return success
    
    def test_create_status_check(self, client_name: str) -> tuple[bool, Optional[str]]:
        """
        Test creating a status check.
        
        Returns:
            Tuple of (success, status_check_id)
        """
        success, response_data = self.run_test(
            test_name=f"Create Status Check (POST /api/status) - Client: {client_name}",
            method="POST",
            endpoint="/status",
            expected_status=200,
            data={"client_name": client_name},
            validate_response=self.validate_status_check_creation
        )
        
        status_check_id = None
        if success and response_data:
            status_check_id = response_data.get('id')
        
        return success, status_check_id
    
    def test_get_status_checks(self) -> bool:
        """Test retrieving all status checks."""
        success, _ = self.run_test(
            test_name="Get Status Checks (GET /api/status)",
            method="GET",
            endpoint="/status",
            expected_status=200,
            validate_response=self.validate_status_check_list
        )
        return success
    
    def test_invalid_requests(self) -> bool:
        """Test various invalid request scenarios."""
        tests_passed = 0
        total_tests = 0
        
        # Test 1: POST to status with missing client_name
        total_tests += 1
        success, _ = self.run_test(
            test_name="Invalid Request - Missing client_name",
            method="POST",
            endpoint="/status",
            expected_status=422,  # Validation error
            data={}
        )
        if success:
            tests_passed += 1
        
        # Test 2: POST to status with empty client_name
        total_tests += 1
        success, _ = self.run_test(
            test_name="Invalid Request - Empty client_name",
            method="POST",
            endpoint="/status",
            expected_status=422,  # Validation error
            data={"client_name": ""}
        )
        if success:
            tests_passed += 1
        
        # Test 3: GET to non-existent endpoint
        total_tests += 1
        success, _ = self.run_test(
            test_name="Invalid Request - Non-existent endpoint",
            method="GET",
            endpoint="/nonexistent",
            expected_status=404
        )
        if success:
            tests_passed += 1
        
        return tests_passed == total_tests
    
    def run_comprehensive_test_suite(self) -> bool:
        """Run the complete test suite."""
        print("🚀 Starting LoyalLight MVP Backend API Test Suite")
        print(f"📍 Testing against: {self.base_url}")
        print("=" * 60)
        print()
        
        all_tests_passed = True
        
        # Test 1: Health Check
        print("📋 Testing Basic Connectivity...")
        health_ok = self.test_health_check()
        all_tests_passed &= health_ok
        
        if not health_ok:
            print("❌ Health check failed - stopping further tests")
            return False
        
        # Test 2: Create Status Checks
        print("📋 Testing Status Check Creation...")
        test_client_names = [
            "Test Client Alpha",
            "Test Client Beta", 
            "Acme Corporation",
            "Test Client with Special Chars !@#"
        ]
        
        created_ids = []
        for client_name in test_client_names:
            success, status_id = self.test_create_status_check(client_name)
            all_tests_passed &= success
            if status_id:
                created_ids.append(status_id)
        
        # Test 3: Retrieve Status Checks
        print("📋 Testing Status Check Retrieval...")
        retrieval_ok = self.test_get_status_checks()
        all_tests_passed &= retrieval_ok
        
        # Test 4: Invalid Requests
        print("📋 Testing Error Handling...")
        error_handling_ok = self.test_invalid_requests()
        all_tests_passed &= error_handling_ok
        
        return all_tests_passed
    
    def print_summary(self):
        """Print test execution summary."""
        print("=" * 60)
        print("📊 TEST EXECUTION SUMMARY")
        print("=" * 60)
        print(f"Total Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%" if self.tests_run > 0 else "0%")
        print()
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL TESTS PASSED! Backend API is working correctly.")
        else:
            print("⚠️  Some tests failed. Check the details above.")
            print("\nFailed Tests:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test_name']}: {result['details']}")
        
        print()


def main():
    """Main test execution function."""
    print("LoyalLight MVP Backend API Testing Suite")
    print("Testing the refactored modular FastAPI backend")
    print()
    
    # Initialize tester with public endpoint
    tester = LoyalLightAPITester()
    
    try:
        # Run comprehensive test suite
        all_passed = tester.run_comprehensive_test_suite()
        
        # Print summary
        tester.print_summary()
        
        # Return appropriate exit code
        return 0 if all_passed else 1
        
    except KeyboardInterrupt:
        print("\n⚠️  Test execution interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {e}")
        return 1
    finally:
        # Close session
        tester.session.close()


if __name__ == "__main__":
    sys.exit(main())