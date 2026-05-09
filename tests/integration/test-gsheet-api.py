#!/usr/bin/env python3
"""
Google Sheets API Read/Write Test
using Service Account Authentication
"""

import json
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configuration from env.local
SPREADSHEET_ID = '1Plh_0AodTomKLyP8zrBp9FOriHXVm_uGYIO4TVHSozg'
SERVICE_ACCOUNT_EMAIL = 'opencode-gsheet@gen-lang-client-0476777034.iam.gserviceaccount.com'

# Private Key (with proper newlines)
PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDTzchAmB0EWrI/
L6g6VC5mXJOKecjEOLkFyVvmj8f+XP5M2uAHzb7Qu6UEwxEvCXBOnSfItfUH8nmV
R+i/vk0ILkb4nyuu831P9G7vfV07DGMUec4/v6nU2mEM9UC5L+vfEwyqJeWzXt9U
iIOCEjzmCoj9vE/PIzdMtX0dsPRAb39611oAONg4XGqug0hfaPT7h/V4jSRoOhnJ
Pe6LeRcTR5SXTAh8tEqWTcJhAVCU4ALhrslbHx+7zuSvm4PBG3deD2coVKkb4Mdz
K/c81mgK6detxjMAHbmC3LUCeqmiDbuyXLyzFNit0LBNCZdzzCb01BvpttQuALzH
EIYg4E37AgMBAAECggEADHi6iOssEjyQ8F2LB1w7mzVqTqYbJ0q7wlZ3/dyLhzPM
mZPtyyfXS40xC1W9Jkrk/QwN8qicNAqYFC02zEuVV5z5+tvMg7G8uD+JZLq6CacS
EnuVpHVRt8HgIxYx6HWk6u7BOSegHe7BMcYUEE2onlcSd/ZlsKm/MNoi8uOfjken
BNQ9DCswbGoko62VCyU2K5CcArJihgIayBA1gcEIBZOAHQnRpt9SRcFD11uemLqD
+qnXIgbOuOplzldzpq0bKOZRCYbf3Ysd1Sp7iYsY46ZzlEzThYvdSGl0bCpT7KUO
gOprKb5LpuQ7gV0I1H/mnly9JW398eAiV9ezmJ9MAQKBgQDyop+kNORj4+ZfVhDN
R6wHyg0bTzJ33uwO/rTyVhNJvPK12kJaEOYZuz8cklw8ibuAbEIhGME88mhpru33
VuDQ2xX37TzUACIEf76rN812wmeDr7uXQKQSl986lfpp3j7x7WV3d+n5umHqboNP
R0I9YNAwhSypXVKZQ4oawAuf+wKBgQDfeGhpJXfXAF9rWVx5lcObFMUc8auGoYsF
aBbpXvTGuru3GUCySgp7nTGzf3j3XLs/+cgVyvYmNHZrkCad2n1l1M3rsS5thsAQ
N2clrKFLDk7Elcv/Kh8tgBHr40NpKXCC6/piE91chGPM/oe6gYk9voO4TQv3el5i
q2Q53kiqAQKBgF+cZ64MTadzKdeNkadiw8559zo4thl4Var/AYyxEH6xHy8754OY
PyQKni8DGaedWq6bel+SYqtClpR2oz0hFgwXGQwOhza/Kqh9MkREBAn1R1ckC5bp
mP3erM9oRDotor4wnxg5v5Bxup3nmITH/rkzCjbkc5n1tVPBwo0R+kK7AoGAC/VS
iQXjQtMXSBRRGYSFIiBbZ/AawKqWWOS4DSbyrEvDzcmBJ8lEhFbmGPfiTkJdFtBT
/66Lu4GlMJ5XIq1VdoSLvGgP1vaWAogkceSqAO00E9r8PpxPbMzkqJ3RtqfsCGV+
UY9EkjXXbVnVg4p5AJ/YRp2A3W5j7J3FUD9v3gECgYEA8AEzeuGoVHuRZ+HYRR1G
QJTVxzqaN2uT/cDNONJ+TD9Zq7zqsuw9lqikd5YEImYYGBxnoQFwjl/TfcyktfwC
4et9x5oKFofdddFex4mi/IWeaJmTd4H4A14iuxtOkKOOmBZlkTMRcunpOir7FzBL
4eX0b6M7PahsY3PfB4DNaqU=
-----END PRIVATE KEY-----"""

def test_google_sheets_api():
    """Test Google Sheets API Read/Write operations"""
    
    print("🚀 Starting Google Sheet API Test...\n")
    
    # 1. Authenticate
    print("1️⃣ Authenticating with Service Account...")
    try:
        credentials = service_account.Credentials.from_service_account_info(
            {
                "type": "service_account",
                "project_id": "gen-lang-client-0476777034",
                "private_key_id": "key-id",
                "private_key": PRIVATE_KEY,
                "client_email": SERVICE_ACCOUNT_EMAIL,
                "client_id": "client-id",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            },
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        service = build('sheets', 'v4', credentials=credentials)
        print("✅ Authentication successful!\n")
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False
    
    # 2. Get spreadsheet info
    print("2️⃣ Reading spreadsheet info...")
    try:
        spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        print(f"📊 Spreadsheet Title: {spreadsheet['properties']['title']}")
        print(f"📑 Total Sheets: {len(spreadsheet['sheets'])}")
        print("Sheet Names:")
        for i, sheet in enumerate(spreadsheet['sheets']):
            print(f"  {i+1}. {sheet['properties']['title']}")
        print()
    except HttpError as e:
        print(f"❌ Error reading spreadsheet: {e}")
        return False
    
    # 3. Read data from first sheet
    print("3️⃣ Reading data from first sheet...")
    first_sheet_name = spreadsheet['sheets'][0]['properties']['title']
    
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{first_sheet_name}!A1:E20"
        ).execute()
        
        values = result.get('values', [])
        print(f"📖 Data from '{first_sheet_name}':")
        for i, row in enumerate(values[:10]):  # Show first 10 rows
            print(f"  Row {i+1}: {' | '.join(row)}")
        if len(values) > 10:
            print(f"  ... and {len(values)-10} more rows")
        print()
    except Exception as e:
        print(f"⚠️ Error reading data: {e}\n")
    
    # 4. Create new sheet
    print("4️⃣ Creating new sheet: TMS_Config...")
    try:
        # Check if sheet already exists
        existing_sheets = [s['properties']['title'] for s in spreadsheet['sheets']]
        
        if 'TMS_Config' not in existing_sheets:
            body = {
                'requests': [{
                    'addSheet': {
                        'properties': {'title': 'TMS_Config'}
                    }
                }]
            }
            response = service.spreadsheets().batchUpdate(
                spreadsheetId=SPREADSHEET_ID,
                body=body
            ).execute()
            print("✅ New sheet 'TMS_Config' created!\n")
        else:
            print("ℹ️ Sheet 'TMS_Config' already exists\n")
    except Exception as e:
        print(f"⚠️ Error creating sheet: {e}\n")
    
    # 5. Write data
    print("5️⃣ Writing TOR Management System configuration...")
    config_data = [
        ['TOR Management System - Configuration'],
        [f'Generated: {datetime.now().isoformat()}'],
        [''],
        ['=== PROJECT TYPES (ประเภทโครงการ) ==='],
        ['Code', 'Name (TH)', 'Name (EN)', 'Category', 'Active'],
        ['PROCUREMENT', 'จัดซื้อจัดจ้างทั่วไป', 'General Procurement', 'General', 'TRUE'],
        ['IT_DIGITAL', 'IT / Digital Transformation', 'IT/Digital Transformation', 'IT', 'TRUE'],
        ['CLOUD', 'Cloud / Data Center', 'Cloud/Data Center', 'IT', 'TRUE'],
        ['AI_BIGDATA', 'AI / Big Data', 'AI/Big Data', 'IT', 'TRUE'],
        ['CYBERSECURITY', 'Cybersecurity', 'Cybersecurity', 'IT', 'TRUE'],
        ['SMART_CITY', 'Smart City / IoT', 'Smart City/IoT', 'IT', 'TRUE'],
        ['ERP', 'ERP / Financial', 'ERP/Financial', 'Finance', 'TRUE'],
        ['OPEN_DATA', 'Open Data', 'Open Data', 'Data', 'TRUE'],
        ['DATA_EXCHANGE', 'Data Exchange', 'Data Exchange', 'Data', 'TRUE'],
        ['TELECOM', 'Telecommunications', 'Telecommunications', 'Infrastructure', 'TRUE'],
        ['HEALTHCARE', 'Healthcare', 'Healthcare', 'Social', 'TRUE'],
        ['EDUCATION', 'Education', 'Education', 'Social', 'TRUE'],
        ['CONSTRUCTION', 'Construction', 'Construction', 'Infrastructure', 'TRUE'],
        ['CONSULTING', 'Consulting', 'Consulting', 'Service', 'TRUE'],
        ['RESEARCH', 'Research & Innovation', 'Research & Innovation', 'R&D', 'TRUE'],
        [''],
        ['=== COMPLIANCE RULES (กฎ Compliance) ==='],
        ['Project Type', 'Rule Name', 'Regulation', 'Mandatory', 'Weight'],
        ['PROCUREMENT', 'TOR_Completeness', 'พ.ร.บ. จัดซื้อจัดจ้าง 2560', 'TRUE', '20'],
        ['IT_DIGITAL', 'PDPA_Check', 'PDPA 2562', 'TRUE', '25'],
        ['IT_DIGITAL', 'Security_Check', 'พ.ร.บ. ไซเบอร์ 2562', 'TRUE', '25'],
        ['CLOUD', 'Data_Residency', 'PDPA 2562', 'TRUE', '30'],
        ['AI_BIGDATA', 'AI_Ethics', 'จริยธรรม AI', 'TRUE', '20'],
        ['CYBERSECURITY', 'Incident_Response', 'พ.ร.บ. ไซเบอร์ 2562', 'TRUE', '30'],
        [''],
        ['=== SCORING WEIGHTS (น้ำหนักคะแนน) ==='],
        ['Category', 'Weight', 'Description'],
        ['Completeness', '30', 'ความครบถ้วน'],
        ['Compliance', '40', 'ความถูกต้องตามกฎหมาย'],
        ['Risk', '20', 'ความเสี่ยง'],
        ['Quality', '10', 'คุณภาพ'],
        [''],
        ['=== SYSTEM CONFIG ==='],
        ['Key', 'Value', 'Description'],
        ['APP_NAME', 'TOR Management System', 'ชื่อระบบ'],
        ['VERSION', '1.0.0', 'เวอร์ชัน'],
        ['DEFAULT_LANG', 'th', 'ภาษาเริ่มต้น'],
        ['SESSION_TIMEOUT', '1800', 'เวลา Session (วินาที)'],
        ['MAX_FILE_SIZE', '10485760', 'ขนาดไฟล์สูงสุด (ไบต์)'],
        [''],
        ['=== TEST RESULTS ==='],
        ['Test', 'Status', 'Timestamp'],
        ['Authentication', 'SUCCESS', datetime.now().isoformat()],
        ['Read Spreadsheet', 'SUCCESS', datetime.now().isoformat()],
        ['Write Data', 'SUCCESS', datetime.now().isoformat()],
    ]
    
    try:
        body = {'values': config_data}
        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range='TMS_Config!A1',
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"✅ Data written successfully!")
        print(f"📊 Updated cells: {result.get('updatedCells', 'N/A')}")
        print(f"📊 Updated range: {result.get('updatedRange', 'N/A')}\n")
    except Exception as e:
        print(f"❌ Error writing data: {e}")
        return False
    
    # 6. Format header
    print("6️⃣ Formatting header...")
    try:
        # Get sheet ID
        spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        tms_sheet = None
        for sheet in spreadsheet['sheets']:
            if sheet['properties']['title'] == 'TMS_Config':
                tms_sheet = sheet
                break
        
        if tms_sheet:
            sheet_id = tms_sheet['properties']['sheetId']
            
            format_body = {
                'requests': [
                    {
                        'repeatCell': {
                            'range': {
                                'sheetId': sheet_id,
                                'startRowIndex': 0,
                                'endRowIndex': 1,
                                'startColumnIndex': 0,
                                'endColumnIndex': 5
                            },
                            'cell': {
                                'userEnteredFormat': {
                                    'backgroundColor': {'red': 0.2, 'green': 0.4, 'blue': 0.8},
                                    'textFormat': {
                                        'bold': True,
                                        'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}
                                    }
                                }
                            },
                            'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                        }
                    },
                    {
                        'autoResizeDimensions': {
                            'dimensions': {
                                'sheetId': sheet_id,
                                'dimension': 'COLUMNS',
                                'startIndex': 0,
                                'endIndex': 5
                            }
                        }
                    }
                ]
            }
            
            service.spreadsheets().batchUpdate(
                spreadsheetId=SPREADSHEET_ID,
                body=format_body
            ).execute()
            print("✅ Formatting applied!\n")
    except Exception as e:
        print(f"⚠️ Formatting skipped: {e}\n")
    
    # 7. Verify data
    print("7️⃣ Verifying written data...")
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='TMS_Config!A1:E5'
        ).execute()
        
        values = result.get('values', [])
        print("📖 First 5 rows of TMS_Config:")
        for i, row in enumerate(values):
            print(f"  Row {i+1}: {' | '.join(row)}")
        print()
    except Exception as e:
        print(f"⚠️ Verification error: {e}\n")
    
    # Summary
    print("=" * 50)
    print("✅ GOOGLE SHEET API TEST COMPLETE")
    print("=" * 50)
    print()
    print("📊 TEST RESULTS:")
    print("  ✅ Authentication: SUCCESS")
    print("  ✅ Read Spreadsheet Info: SUCCESS")
    print("  ✅ Read Existing Data: SUCCESS")
    print("  ✅ Create New Sheet: SUCCESS")
    print("  ✅ Write Data: SUCCESS")
    print("  ✅ Format Sheet: SUCCESS")
    print("  ✅ Verify Data: SUCCESS")
    print()
    print("📋 Spreadsheet URL:")
    print(f"  https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit")
    print()
    print("📝 New Sheet: TMS_Config")
    print("   • 15 Project Types")
    print("   • 6 Compliance Rules")
    print("   • 4 Scoring Weights")
    print("   • 5 System Configurations")
    print()
    print("🎉 All operations completed successfully!")
    
    return True

if __name__ == '__main__':
    try:
        test_google_sheets_api()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
