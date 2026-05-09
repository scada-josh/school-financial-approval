#!/usr/bin/env python3
"""
TOR Management System - Google Sheet Setup
=============================================
สร้างระบบจัดการ TOR ใน Google Sheet โดยใช้ข้อมูลจาก TOR Matrix

Features:
- อ่านข้อมูล TOR Matrix (หัวข้อ TOR ตามประเภทโครงการ)
- สร้าง Sheet ใหม่สำหรับจัดการ Configuration
- เก็บข้อมูลหัวข้อ TOR ที่ใช้/ไม่ใช้ ตามประเภทโครงการ
"""

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime
import json

# Configuration
SPREADSHEET_ID = '1Plh_0AodTomKLyP8zrBp9FOriHXVm_uGYIO4TVHSozg'
SERVICE_ACCOUNT_EMAIL = 'opencode-gsheet@gen-lang-client-0476777034.iam.gserviceaccount.com'
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

def get_service():
    """สร้าง Google Sheets service"""
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
    return build('sheets', 'v4', credentials=credentials)

def read_tor_matrix(service):
    """อ่านข้อมูลจาก TOR Matrix"""
    print("📖 กำลังอ่านข้อมูล TOR Matrix...")
    
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='TOR Matrix!A1:AC20'
    ).execute()
    
    values = result.get('values', [])
    
    if not values:
        print("❌ ไม่พบข้อมูลใน TOR Matrix")
        return None
    
    headers = values[0]
    data_rows = values[1:]
    
    print(f"✅ อ่านข้อมูลสำเร็จ: {len(data_rows)} ประเภทโครงการ, {len(headers)} หัวข้อ")
    
    # แปลงเป็น dictionary
    tor_data = {
        'headers': headers,
        'project_types': []
    }
    
    for row in data_rows:
        if len(row) > 0 and row[0]:  # มีชื่อประเภทโครงการ
            project_type = {
                'name': row[0],
                'sections': {}
            }
            
            # อ่านสถานะของแต่ละหัวข้อ (✅ = ใช้, ว่าง = ไม่ใช้)
            for i in range(1, len(headers)):
                if i < len(row):
                    is_checked = row[i] == '✅'
                    project_type['sections'][headers[i]] = is_checked
                else:
                    project_type['sections'][headers[i]] = False
            
            tor_data['project_types'].append(project_type)
    
    return tor_data

def create_tor_config_sheet(service):
    """สร้าง Sheet ใหม่สำหรับจัดการ TOR Configuration"""
    print("\n📝 กำลังสร้าง Sheet TOR_Config...")
    
    # ตรวจสอบว่ามี Sheet อยู่แล้วหรือไม่
    spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    existing_sheets = [s['properties']['title'] for s in spreadsheet['sheets']]
    
    if 'TOR_Config' in existing_sheets:
        print("ℹ️ Sheet 'TOR_Config' มีอยู่แล้ว จะอัปเดตข้อมูล")
        return True
    
    # สร้าง Sheet ใหม่
    body = {
        'requests': [{
            'addSheet': {
                'properties': {
                    'title': 'TOR_Config',
                    'gridProperties': {
                        'rowCount': 1000,
                        'columnCount': 30
                    }
                }
            }
        }]
    }
    
    try:
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body=body
        ).execute()
        print("✅ สร้าง Sheet 'TOR_Config' สำเร็จ")
        return True
    except Exception as e:
        print(f"❌ ไม่สามารถสร้าง Sheet ได้: {e}")
        return False

def write_tor_config(service, tor_data):
    """เขียนข้อมูล TOR Configuration ลง Sheet"""
    print("\n💾 กำลังเขียนข้อมูลลง TOR_Config...")
    
    # เตรียมข้อมูลสำหรับเขียน
    config_data = []
    
    # Header แถวที่ 1
    header_row = ['ประเภทโครงการ'] + tor_data['headers'][1:]  # ไม่เอา 'ประเภทโครงการ' ซ้ำ
    config_data.append(header_row)
    
    # ข้อมูลแต่ละประเภทโครงการ
    for project in tor_data['project_types']:
        row = [project['name']]
        for header in tor_data['headers'][1:]:
            is_enabled = project['sections'].get(header, False)
            row.append('✅' if is_enabled else '❌')
        config_data.append(row)
    
    # เขียนข้อมูล
    body = {
        'values': config_data
    }
    
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range='TOR_Config!A1',
        valueInputOption='RAW',
        body=body
    ).execute()
    
    print(f"✅ เขียนข้อมูลสำเร็จ: {result.get('updatedCells', 'N/A')} cells")
    
    # Format header
    format_sheet(service)
    
    return True

def format_sheet(service):
    """จัดรูปแบบ Sheet"""
    print("\n🎨 กำลังจัดรูปแบบ Sheet...")
    
    # หา Sheet ID
    spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    tor_config_sheet = None
    for sheet in spreadsheet['sheets']:
        if sheet['properties']['title'] == 'TOR_Config':
            tor_config_sheet = sheet
            break
    
    if not tor_config_sheet:
        print("❌ ไม่พบ Sheet TOR_Config")
        return
    
    sheet_id = tor_config_sheet['properties']['sheetId']
    
    # จัดรูปแบบ
    format_requests = {
        'requests': [
            # Header row formatting
            {
                'repeatCell': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': 0,
                        'endRowIndex': 1,
                        'startColumnIndex': 0,
                        'endColumnIndex': 29
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'backgroundColor': {'red': 0.2, 'green': 0.4, 'blue': 0.8},
                            'textFormat': {
                                'bold': True,
                                'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}
                            },
                            'horizontalAlignment': 'CENTER',
                            'verticalAlignment': 'MIDDLE'
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)'
                }
            },
            # Column A formatting (Project Type names)
            {
                'repeatCell': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': 1,
                        'endRowIndex': 20,
                        'startColumnIndex': 0,
                        'endColumnIndex': 1
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'textFormat': {
                                'bold': True
                            },
                            'horizontalAlignment': 'LEFT'
                        }
                    },
                    'fields': 'userEnteredFormat(textFormat,horizontalAlignment)'
                }
            },
            # Center align for checkmarks
            {
                'repeatCell': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': 1,
                        'endRowIndex': 20,
                        'startColumnIndex': 1,
                        'endColumnIndex': 29
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'horizontalAlignment': 'CENTER',
                            'verticalAlignment': 'MIDDLE'
                        }
                    },
                    'fields': 'userEnteredFormat(horizontalAlignment,verticalAlignment)'
                }
            },
            # Auto-resize columns
            {
                'autoResizeDimensions': {
                    'dimensions': {
                        'sheetId': sheet_id,
                        'dimension': 'COLUMNS',
                        'startIndex': 0,
                        'endIndex': 29
                    }
                }
            },
            # Freeze header row
            {
                'updateSheetProperties': {
                    'properties': {
                        'sheetId': sheet_id,
                        'gridProperties': {
                            'frozenRowCount': 1
                        }
                    },
                    'fields': 'gridProperties.frozenRowCount'
                }
            }
        ]
    }
    
    service.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body=format_requests
    ).execute()
    
    print("✅ จัดรูปแบบ Sheet สำเร็จ")

def create_metadata_sheet(service, tor_data):
    """สร้าง Sheet สำหรับ Metadata และสถิติ"""
    print("\n📊 กำลังสร้าง Sheet TOR_Metadata...")
    
    # ตรวจสอบว่ามี Sheet อยู่แล้วหรือไม่
    spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    existing_sheets = [s['properties']['title'] for s in spreadsheet['sheets']]
    
    if 'TOR_Metadata' not in existing_sheets:
        body = {
            'requests': [{
                'addSheet': {
                    'properties': {
                        'title': 'TOR_Metadata',
                        'gridProperties': {
                            'rowCount': 100,
                            'columnCount': 10
                        }
                    }
                }
            }]
        }
        
        service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body=body
        ).execute()
        print("✅ สร้าง Sheet 'TOR_Metadata' สำเร็จ")
    else:
        print("ℹ️ Sheet 'TOR_Metadata' มีอยู่แล้ว")
    
    # เตรียมข้อมูล Metadata
    metadata = [
        ['TOR Management System - Metadata'],
        [f'Generated: {datetime.now().isoformat()}'],
        [''],
        ['=== STATISTICS ==='],
        ['Total Project Types', str(len(tor_data['project_types']))],
        ['Total Sections', str(len(tor_data['headers']) - 1)],
        [''],
        ['=== PROJECT TYPE SUMMARY ==='],
        ['Project Type', 'Active Sections', 'Section Count']
    ]
    
    for project in tor_data['project_types']:
        active_count = sum(1 for v in project['sections'].values() if v)
        total_count = len(project['sections'])
        metadata.append([project['name'], str(active_count), str(total_count)])
    
    metadata.append([''])
    metadata.append(['=== SECTION USAGE ==='])
    metadata.append(['Section', 'Used By', 'Usage Count'])
    
    # นับจำนวนประเภทโครงการที่ใช้แต่ละ section
    section_usage = {}
    for header in tor_data['headers'][1:]:
        section_usage[header] = 0
        for project in tor_data['project_types']:
            if project['sections'].get(header, False):
                section_usage[header] += 1
    
    # เรียงตามจำนวนการใช้งาน
    sorted_sections = sorted(section_usage.items(), key=lambda x: x[1], reverse=True)
    
    for section, count in sorted_sections:
        usage_pct = (count / len(tor_data['project_types'])) * 100
        metadata.append([section, f'{count}/{len(tor_data["project_types"])}', f'{usage_pct:.1f}%'])
    
    # เขียนข้อมูล
    body = {
        'values': metadata
    }
    
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range='TOR_Metadata!A1',
        valueInputOption='RAW',
        body=body
    ).execute()
    
    print(f"✅ เขียน Metadata สำเร็จ: {result.get('updatedCells', 'N/A')} cells")
    
    # Format metadata sheet
    format_metadata_sheet(service)

def format_metadata_sheet(service):
    """จัดรูปแบบ Metadata Sheet"""
    spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    
    metadata_sheet = None
    for sheet in spreadsheet['sheets']:
        if sheet['properties']['title'] == 'TOR_Metadata':
            metadata_sheet = sheet
            break
    
    if not metadata_sheet:
        return
    
    sheet_id = metadata_sheet['properties']['sheetId']
    
    format_requests = {
        'requests': [
            {
                'repeatCell': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': 0,
                        'endRowIndex': 1
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'backgroundColor': {'red': 0.2, 'green': 0.4, 'blue': 0.8},
                            'textFormat': {
                                'bold': True,
                                'foregroundColor': {'red': 1, 'green': 1, 'blue': 1},
                                'fontSize': 14
                            }
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            },
            {
                'repeatCell': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': 3,
                        'endRowIndex': 4
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'backgroundColor': {'red': 0.1, 'green': 0.6, 'blue': 0.4},
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
                'repeatCell': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': 8,
                        'endRowIndex': 9
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'backgroundColor': {'red': 0.8, 'green': 0.5, 'blue': 0.1},
                            'textFormat': {
                                'bold': True,
                                'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}
                            }
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            }
        ]
    }
    
    service.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body=format_requests
    ).execute()

def create_changelog_sheet(service):
    """สร้าง Sheet สำหรับบันทึกการเปลี่ยนแปลง"""
    print("\n📝 กำลังสร้าง Sheet TOR_Changelog...")
    
    spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    existing_sheets = [s['properties']['title'] for s in spreadsheet['sheets']]
    
    if 'TOR_Changelog' not in existing_sheets:
        body = {
            'requests': [{
                'addSheet': {
                    'properties': {
                        'title': 'TOR_Changelog',
                        'gridProperties': {
                            'rowCount': 1000,
                            'columnCount': 10
                        }
                    }
                }
            }]
        }
        
        service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body=body
        ).execute()
        print("✅ สร้าง Sheet 'TOR_Changelog' สำเร็จ")
    else:
        print("ℹ️ Sheet 'TOR_Changelog' มีอยู่แล้ว")
    
    # เขียน Header
    changelog_header = [
        ['Timestamp', 'User', 'Action', 'Project Type', 'Section', 'Old Value', 'New Value', 'Notes']
    ]
    
    body = {
        'values': changelog_header
    }
    
    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range='TOR_Changelog!A1',
        valueInputOption='RAW',
        body=body
    ).execute()
    
    # Format
    spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    for sheet in spreadsheet['sheets']:
        if sheet['properties']['title'] == 'TOR_Changelog':
            sheet_id = sheet['properties']['sheetId']
            
            format_requests = {
                'requests': [
                    {
                        'repeatCell': {
                            'range': {
                                'sheetId': sheet_id,
                                'startRowIndex': 0,
                                'endRowIndex': 1
                            },
                            'cell': {
                                'userEnteredFormat': {
                                    'backgroundColor': {'red': 0.5, 'green': 0.2, 'blue': 0.2},
                                    'textFormat': {
                                        'bold': True,
                                        'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}
                                    }
                                }
                            },
                            'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                        }
                    }
                ]
            }
            
            service.spreadsheets().batchUpdate(
                spreadsheetId=SPREADSHEET_ID,
                body=format_requests
            ).execute()
            break

def main():
    """ฟังก์ชันหลัก"""
    print("=" * 60)
    print("TOR Management System - Google Sheet Setup")
    print("=" * 60)
    print()
    
    try:
        # 1. เชื่อมต่อ Google Sheets API
        print("🔐 กำลังเชื่อมต่อ Google Sheets API...")
        service = get_service()
        print("✅ เชื่อมต่อสำเร็จ\n")
        
        # 2. อ่านข้อมูลจาก TOR Matrix
        tor_data = read_tor_matrix(service)
        
        if not tor_data:
            print("❌ ไม่สามารถดำเนินการต่อได้")
            return
        
        # 3. แสดงสรุปข้อมูล
        print("\n📋 สรุปข้อมูล TOR Matrix:")
        print(f"   - จำนวนประเภทโครงการ: {len(tor_data['project_types'])}")
        print(f"   - จำนวนหัวข้อ TOR: {len(tor_data['headers']) - 1}")
        print(f"\n   ประเภทโครงการ:")
        for project in tor_data['project_types']:
            active_count = sum(1 for v in project['sections'].values() if v)
            print(f"     • {project['name']}: {active_count} หัวข้อ")
        
        # 4. สร้าง Sheet TOR_Config
        if create_tor_config_sheet(service):
            write_tor_config(service, tor_data)
        
        # 5. สร้าง Sheet TOR_Metadata
        create_metadata_sheet(service, tor_data)
        
        # 6. สร้าง Sheet TOR_Changelog
        create_changelog_sheet(service)
        
        # 7. สรุปผล
        print("\n" + "=" * 60)
        print("✅ SETUP COMPLETE")
        print("=" * 60)
        print()
        print("📊 Sheets ที่สร้าง/อัปเดต:")
        print("   1. TOR Matrix - ข้อมูลต้นฉบับ")
        print("   2. TOR_Config - ข้อมูล Configuration (✅/❌)")
        print("   3. TOR_Metadata - สถิติและสรุป")
        print("   4. TOR_Changelog - บันทึกการเปลี่ยนแปลง")
        print()
        print("🔗 URL:")
        print(f"   https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
