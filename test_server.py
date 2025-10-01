#!/usr/bin/env python3
"""
Check if PyFluff server is responding correctly.
"""

import requests
import json

def test_server():
    """Test PyFluff server endpoints."""
    base_url = "http://localhost:8080"
    
    print("=" * 60)
    print("PyFluff Server Test")
    print("=" * 60)
    
    # Test 1: Root endpoint
    print("\n1. Testing root endpoint (/)...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✓ Root endpoint OK")
        else:
            print(f"❌ Root returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot reach server: {e}")
        print("\nMake sure the server is running:")
        print("  python -m pyfluff.server")
        return
    
    # Test 2: API docs
    print("\n2. Testing API docs (/docs)...")
    try:
        response = requests.get(f"{base_url}/docs")
        if response.status_code == 200:
            print("✓ API docs OK")
        else:
            print(f"❌ Docs returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Error accessing docs: {e}")
    
    # Test 3: Status endpoint
    print("\n3. Testing status endpoint (/status)...")
    try:
        response = requests.get(f"{base_url}/status")
        if response.status_code == 200:
            status = response.json()
            print(f"✓ Status endpoint OK")
            print(f"  Connected: {status['connected']}")
            if status['connected']:
                print(f"  Device: {status.get('device_name', 'Unknown')}")
                print(f"  Address: {status.get('device_address', 'Unknown')}")
        else:
            print(f"❌ Status returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting status: {e}")
    
    # Test 4: Static files
    print("\n4. Testing static files...")
    for filename in ['app.js', 'style.css']:
        try:
            response = requests.get(f"{base_url}/static/{filename}")
            if response.status_code == 200:
                print(f"✓ {filename} loaded OK ({len(response.content)} bytes)")
            else:
                print(f"❌ {filename} returned status {response.status_code}")
        except Exception as e:
            print(f"❌ Error loading {filename}: {e}")
    
    # Test 5: Try connecting (if not already connected)
    print("\n5. Testing connection endpoint...")
    try:
        response = requests.post(f"{base_url}/connect")
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Connect endpoint OK: {result['message']}")
        elif response.status_code == 503:
            print("⚠️  Connect failed (no Furby found)")
            print("  This is expected if Furby is off or out of range")
        else:
            print(f"❌ Connect returned status {response.status_code}")
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"❌ Error testing connection: {e}")
    
    print("\n" + "=" * 60)
    print("Test complete!")
    print("=" * 60)
    print("\nIf all tests pass:")
    print("  - Server is running correctly")
    print("  - Static files are being served")
    print("  - API endpoints are accessible")
    print("\nNext step: Open http://localhost:8080 in your browser")

if __name__ == "__main__":
    test_server()
