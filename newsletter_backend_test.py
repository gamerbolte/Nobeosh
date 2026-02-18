#!/usr/bin/env python3
"""
Newsletter System Backend API Tests
Tests all newsletter-related endpoints for GameShop Nepal
"""
import requests
import sys
import json
from datetime import datetime

class NewsletterAPITester:
    def __init__(self, base_url="https://ganguli-wata.preview.emergentagent.com"):
        self.base_url = base_url
        self.token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/api/{endpoint}"
        test_headers = {'Content-Type': 'application/json'}
        if self.token:
            test_headers['Authorization'] = f'Bearer {self.token}'
        if headers:
            test_headers.update(headers)

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {method} {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=test_headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=test_headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=test_headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=test_headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text}")
                self.failed_tests.append(f"{name}: Expected {expected_status}, got {response.status_code}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.failed_tests.append(f"{name}: {str(e)}")
            return False, {}

    def test_login(self):
        """Test admin login"""
        success, response = self.run_test(
            "Admin Login",
            "POST",
            "auth/login",
            200,
            data={"email": "gsnadmin", "password": "gsnadmin"}
        )
        if success and 'token' in response:
            self.token = response['token']
            print(f"   ✅ Token obtained: {self.token[:20]}...")
            return True
        return False

    def test_newsletter_templates(self):
        """Test getting newsletter templates"""
        success, response = self.run_test(
            "Get Newsletter Templates",
            "GET",
            "newsletter/templates",
            200
        )
        if success:
            templates = response
            print(f"   📧 Found {len(templates)} templates")
            
            # Check if we have the expected 5 templates
            expected_templates = ['new_product', 'sale_announcement', 'weekly_update', 'restock_alert', 'custom']
            found_templates = [t.get('id') for t in templates]
            
            for expected in expected_templates:
                if expected in found_templates:
                    print(f"   ✅ Template '{expected}' found")
                else:
                    print(f"   ❌ Template '{expected}' missing")
                    self.failed_tests.append(f"Missing template: {expected}")
                    return False
            
            # Check template structure
            for template in templates:
                required_fields = ['id', 'name', 'description', 'variables', 'subject']
                for field in required_fields:
                    if field not in template:
                        print(f"   ❌ Template missing field: {field}")
                        self.failed_tests.append(f"Template missing field: {field}")
                        return False
            
            return True
        return False

    def test_subscriber_counts(self):
        """Test getting subscriber counts"""
        success, response = self.run_test(
            "Get Subscriber Counts",
            "GET",
            "newsletter/subscribers/count",
            200
        )
        if success:
            print(f"   📊 Subscriber counts: {response}")
            
            # Check expected fields
            expected_fields = ['all', 'subscribed', 'recent_buyers']
            for field in expected_fields:
                if field in response:
                    print(f"   ✅ Count field '{field}': {response[field]}")
                else:
                    print(f"   ❌ Missing count field: {field}")
                    self.failed_tests.append(f"Missing subscriber count field: {field}")
                    return False
            return True
        return False

    def test_newsletter_preview(self):
        """Test newsletter preview API"""
        # Test with new_product template
        test_variables = {
            "product_name": "Test Gaming Headset",
            "product_description": "High-quality gaming headset with surround sound",
            "product_price": "5999",
            "product_image": "https://example.com/headset.jpg",
            "product_link": "https://gameshopnepal.com/products/gaming-headset"
        }
        
        success, response = self.run_test(
            "Newsletter Preview",
            "POST",
            "newsletter/preview",
            200,
            data={
                "template_id": "new_product",
                "variables": test_variables
            }
        )
        if success:
            # Check if response has subject and html
            if 'subject' in response and 'html' in response:
                print(f"   ✅ Preview generated - Subject: {response['subject'][:50]}...")
                print(f"   ✅ HTML content length: {len(response['html'])} chars")
                
                # Check if variables were replaced in subject
                if "Test Gaming Headset" in response['subject']:
                    print(f"   ✅ Variables properly replaced in subject")
                else:
                    print(f"   ❌ Variables not replaced in subject")
                    self.failed_tests.append("Variables not replaced in preview subject")
                    return False
                
                return True
            else:
                print(f"   ❌ Preview missing subject or html fields")
                self.failed_tests.append("Preview missing required fields")
                return False
        return False

    def test_newsletter_send_test(self):
        """Test sending test newsletter"""
        test_variables = {
            "product_name": "Test Product",
            "product_description": "Test description",
            "product_price": "1000",
            "product_image": "https://example.com/test.jpg",
            "product_link": "https://example.com"
        }
        
        success, response = self.run_test(
            "Send Test Newsletter",
            "POST",
            "newsletter/send-test",
            200,
            data={
                "template_id": "new_product",
                "variables": test_variables,
                "test_email": "gameshopnepal.buy@gmail.com"
            }
        )
        if success:
            # Check if response indicates success
            if 'sent' in response and response['sent'] > 0:
                print(f"   ✅ Test email sent successfully: {response['sent']} sent")
                return True
            else:
                print(f"   ❌ Test email not sent: {response}")
                self.failed_tests.append("Test email sending failed")
                return False
        return False

    def test_newsletter_campaigns_history(self):
        """Test getting newsletter campaigns history"""
        success, response = self.run_test(
            "Get Newsletter Campaigns",
            "GET",
            "newsletter/campaigns",
            200
        )
        if success:
            campaigns = response
            print(f"   📈 Found {len(campaigns)} campaigns in history")
            
            # Check campaign structure if any exist
            if campaigns:
                campaign = campaigns[0]
                expected_fields = ['id', 'template_id', 'subject', 'sent', 'failed', 'total_recipients', 'created_at']
                for field in expected_fields:
                    if field not in campaign:
                        print(f"   ❌ Campaign missing field: {field}")
                        self.failed_tests.append(f"Campaign missing field: {field}")
                        return False
                print(f"   ✅ Campaign structure is valid")
            
            return True
        return False

def main():
    print("🚀 Starting Newsletter System Backend Tests")
    print("=" * 60)
    
    tester = NewsletterAPITester()
    
    # Test sequence - focus on newsletter functionality
    tests = [
        ("Admin Login", tester.test_login),
        ("Newsletter Templates", tester.test_newsletter_templates),
        ("Subscriber Counts", tester.test_subscriber_counts),
        ("Newsletter Preview", tester.test_newsletter_preview),
        ("Send Test Newsletter", tester.test_newsletter_send_test),
        ("Newsletter Campaigns History", tester.test_newsletter_campaigns_history),
    ]
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            test_func()
        except Exception as e:
            print(f"❌ Test '{test_name}' crashed: {str(e)}")
            tester.failed_tests.append(f"{test_name}: Crashed - {str(e)}")
    
    # Print final results
    print(f"\n{'='*60}")
    print(f"📊 FINAL RESULTS")
    print(f"{'='*60}")
    print(f"Tests Run: {tester.tests_run}")
    print(f"Tests Passed: {tester.tests_passed}")
    print(f"Tests Failed: {tester.tests_run - tester.tests_passed}")
    print(f"Success Rate: {(tester.tests_passed/tester.tests_run*100):.1f}%" if tester.tests_run > 0 else "0%")
    
    if tester.failed_tests:
        print(f"\n❌ FAILED TESTS:")
        for i, failure in enumerate(tester.failed_tests, 1):
            print(f"   {i}. {failure}")
    else:
        print(f"\n🎉 ALL TESTS PASSED!")
    
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())