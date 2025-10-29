#!/usr/bin/env python3
"""
Test script to upload a pitch deck to the API endpoint
"""
import requests
import os

def test_upload():
    # Create a simple test PDF content
    test_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n>>\nendobj\nxref\n0 4\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \ntrailer\n<<\n/Size 4\n/Root 1 0 R\n>>\nstartxref\n174\n%%EOF"
    
    # Write test PDF file
    with open('test_pitch.pdf', 'wb') as f:
        f.write(test_content)
    
    # Upload to API
    url = 'http://localhost:8000/api/deals/'
    
    try:
        with open('test_pitch.pdf', 'rb') as f:
            files = {'pitch_deck': ('test_pitch.pdf', f, 'application/pdf')}
            response = requests.post(url, files=files)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 201:
            print("✅ Upload successful!")
            return response.json()
        else:
            print("❌ Upload failed!")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        # Clean up
        if os.path.exists('test_pitch.pdf'):
            os.remove('test_pitch.pdf')

if __name__ == "__main__":
    test_upload()
