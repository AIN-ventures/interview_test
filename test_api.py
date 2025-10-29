#!/usr/bin/env python3
"""
Comprehensive API test script with error monitoring
"""
import requests
import time
import json

def test_api_endpoints():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Pitch Deck Analyzer API")
    print("=" * 50)
    
    # Test 1: Check if API is running
    print("\n1. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
            print("   ✅ API is running")
        else:
            print("   ❌ API not responding correctly")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Test 2: Check deals endpoint
    print("\n2. Testing deals list endpoint...")
    try:
        response = requests.get(f"{base_url}/api/deals/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Deals endpoint working")
        else:
            print("   ❌ Deals endpoint error")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Test file upload
    print("\n3. Testing file upload...")
    
    # Create a minimal valid PDF
    pdf_content = b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
>>
endobj
4 0 obj
<<
/Length 44
>>
stream
BT
/F1 12 Tf
72 720 Td
(Test Pitch Deck) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000204 00000 n 
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
296
%%EOF"""
    
    try:
        files = {
            'pitch_deck': ('test_pitch.pdf', pdf_content, 'application/pdf')
        }
        
        print("   Uploading test PDF...")
        response = requests.post(f"{base_url}/api/deals/", files=files)
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 201:
            result = response.json()
            print("   ✅ Upload successful!")
            print(f"   Deal ID: {result.get('id')}")
            print(f"   Task ID: {result.get('task_id')}")
            
            # Monitor processing
            deal_id = result.get('id')
            if deal_id:
                print(f"\n4. Monitoring processing for deal {deal_id}...")
                for i in range(10):  # Check for up to 10 seconds
                    time.sleep(1)
                    try:
                        status_response = requests.get(f"{base_url}/api/deals/{deal_id}/status/")
                        if status_response.status_code == 200:
                            status_data = status_response.json()
                            current_status = status_data.get('status')
                            print(f"   Status check {i+1}: {current_status}")
                            
                            if current_status in ['completed', 'failed']:
                                if current_status == 'failed':
                                    print(f"   ❌ Processing failed: {status_data.get('error_message')}")
                                else:
                                    print("   ✅ Processing completed!")
                                break
                        else:
                            print(f"   Status check failed: {status_response.status_code}")
                    except Exception as e:
                        print(f"   Status check error: {e}")
                        
        elif response.status_code == 400:
            print("   ❌ Validation error (400)")
            try:
                error_data = response.json()
                print(f"   Errors: {error_data}")
            except:
                pass
        elif response.status_code == 500:
            print("   ❌ Server error (500)")
            print("   This is likely the OpenAI initialization error!")
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Upload error: {e}")

if __name__ == "__main__":
    test_api_endpoints()
