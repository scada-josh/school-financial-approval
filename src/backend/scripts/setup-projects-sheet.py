#!/usr/bin/env python3
"""
Create Projects Sheet in Google Spreadsheet
============================================
สร้าง Sheet ใหม่ชื่อ "Projects" สำหรับเก็บข้อมูลโครงการ
พร้อมข้อมูลตัวอย่าง
"""

from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime

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

def create_projects_sheet(service):
    """สร้าง Sheet Projects ใหม่"""
    print("📝 กำลังสร้าง Sheet Projects...")
    
    spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    existing_sheets = [s['properties']['title'] for s in spreadsheet['sheets']]
    
    if 'Projects' in existing_sheets:
        print("ℹ️ Sheet 'Projects' มีอยู่แล้ว จะอัปเดตข้อมูล")
        # หา sheet id
        for sheet in spreadsheet['sheets']:
            if sheet['properties']['title'] == 'Projects':
                return sheet['properties']['sheetId']
    
    # สร้าง sheet ใหม่
    body = {
        'requests': [{
            'addSheet': {
                'properties': {
                    'title': 'Projects',
                    'gridProperties': {
                        'rowCount': 1000,
                        'columnCount': 15
                    }
                }
            }
        }]
    }
    
    response = service.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body=body
    ).execute()
    
    sheet_id = response['replies'][0]['addSheet']['properties']['sheetId']
    print(f"✅ สร้าง Sheet 'Projects' สำเร็จ (ID: {sheet_id})")
    return sheet_id

def write_projects_data(service, sheet_id):
    """เขียนข้อมูลลง Sheet Projects"""
    print("\n💾 กำลังเขียนข้อมูลโครงการ...")
    
    # ข้อมูล Header + ตัวอย่างข้อมูล
    data = [
        # Header Row
        ['ID', 'ชื่อโครงการ', 'ประเภทโครงการ', 'คำอธิบายโครงการ', 'ปีงบประมาณ', 
         'หัวหน้าหน่วยงาน', 'หัวหน้าฝ่ายงบประมาณ', 'ผู้อำนวยการโรงเรียน', 
         'หมายเหตุ', 'วันที่สร้าง', 'วันที่แก้ไขล่าสุด'],
        # Sample Data
        ['P001', 'ระบบจัดการห้องสมุดอัจฉริยะ', 'IT / Digital Transformation', 
         'พัฒนาระบบห้องสมุดดิจิทัล พร้อม AI ช่วยค้นหาหนังสือ', 'ปีงบประมาณ 2568',
         'Approve', 'Approve', 'Not Started',
         'รอการอนุมัติจากผู้อำนวยการ', '2025-01-15', '2025-03-20'],
        ['P002', 'ก่อสร้างอาคารเรียนเพิ่มเติม', 'ก่อสร้าง', 
         'ก่อสร้างอาคารเรียน 3 ชั้น จำนวน 8 ห้องเรียน', 'ปีงบประมาณ 2568',
         'Approve', 'Approve', 'Approve',
         'อนุมัติเรียบร้อยแล้ว', '2025-02-01', '2025-03-15'],
        ['P003', 'จัดซื้อคอมพิวเตอร์สำหรับห้องปฏิบัติการ', 'จัดซื้อจัดจ้างทั่วไป', 
         'จัดซื้อคอมพิวเตอร์ 50 เครื่อง พร้อมอุปกรณ์ต่อพ่วง', 'ปีงบประมาณ 2568',
         'Reject', 'Not Started', 'Not Started',
         'หัวหน้าหน่วยงานไม่อนุมัติ เนื่องจากงบประมาณไม่เพียงพอ', '2025-02-20', '2025-02-25'],
        ['P004', 'ระบบรักษาความปลอดภัย (CCTV)', 'Cybersecurity', 
         'ติดตั้งกล้องวงจรปิดทั่วโรงเรียน พร้อมระบบ AI ตรวจจับ', 'ปีงบประมาณ 2569',
         'Not Started', 'Not Started', 'Not Started',
         'อยู่ระหว่างจัดทำ TOR', '2025-03-01', '2025-03-01'],
        ['P005', 'พัฒนาระบบ AI ช่วยตรวจการบ้าน', 'AI / Big Data', 
         'ระบบวิเคราะห์คำตอบนักเรียน พร้อมให้คะแนนอัตโนมัติ', 'ปีงบประมาณ 2569',
         'Approve', 'Not Started', 'Not Started',
         'รอการพิจารณาจากฝ่ายงบประมาณ', '2025-03-10', '2025-03-10'],
        ['P006', 'จ้างที่ปรึกษาด้านการศึกษา', 'จ้างที่ปรึกษา', 
         'จ้างที่ปรึกษาพัฒนาหลักสูตร STEM', 'ปีงบประมาณ 2568',
         'Approve', 'Approve', 'Reject',
         'ผู้อำนวยการไม่อนุมัติ ขอให้ปรับแผนใหม่', '2025-01-20', '2025-02-28'],
        ['P007', 'ระบบ Data Center โรงเรียน', 'Cloud / Data Center', 
         'สร้าง Data Center ภายในโรงเรียน พร้อมระบบสำรองข้อมูล', 'ปีงบประมาณ 2569',
         'Not Started', 'Not Started', 'Not Started',
         'อยู่ระหว่างศึกษาความเป็นไปได้', '2025-03-15', '2025-03-15'],
        ['P008', 'โครงการ Smart Classroom', 'Smart City / IoT', 
         'ติดตั้งอุปกรณ์ IoT ในห้องเรียน 10 ห้อง', 'ปีงบประมาณ 2568',
         'Approve', 'Reject', 'Not Started',
         'ฝ่ายงบประมาณไม่อนุมัติ เนื่องจากซ้ำซ้อนกับโครงการอื่น', '2025-02-10', '2025-02-20'],
    ]
    
    body = {'values': data}
    
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range='Projects!A1',
        valueInputOption='RAW',
        body=body
    ).execute()
    
    print(f"✅ เขียนข้อมูลสำเร็จ: {result.get('updatedCells', 'N/A')} cells")
    
    # Format sheet
    format_projects_sheet(service, sheet_id)

def format_projects_sheet(service, sheet_id):
    """จัดรูปแบบ Sheet"""
    print("\n🎨 กำลังจัดรูปแบบ Sheet...")
    
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
                        'endColumnIndex': 11
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
            # Status columns formatting (F, G, H = columns 5, 6, 7)
            {
                'repeatCell': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': 1,
                        'endRowIndex': 20,
                        'startColumnIndex': 5,
                        'endColumnIndex': 8
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
                        'endIndex': 11
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
            },
            # ID column width
            {
                'updateDimensionProperties': {
                    'range': {
                        'sheetId': sheet_id,
                        'dimension': 'COLUMNS',
                        'startIndex': 0,
                        'endIndex': 1
                    },
                    'properties': {
                        'pixelSize': 80
                    },
                    'fields': 'pixelSize'
                }
            },
            # Project name column width
            {
                'updateDimensionProperties': {
                    'range': {
                        'sheetId': sheet_id,
                        'dimension': 'COLUMNS',
                        'startIndex': 1,
                        'endIndex': 2
                    },
                    'properties': {
                        'pixelSize': 300
                    },
                    'fields': 'pixelSize'
                }
            },
            # Description column width
            {
                'updateDimensionProperties': {
                    'range': {
                        'sheetId': sheet_id,
                        'dimension': 'COLUMNS',
                        'startIndex': 3,
                        'endIndex': 4
                    },
                    'properties': {
                        'pixelSize': 400
                    },
                    'fields': 'pixelSize'
                }
            }
        ]
    }
    
    service.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body=format_requests
    ).execute()
    
    print("✅ จัดรูปแบบ Sheet สำเร็จ")

def create_project_types_dropdown(service, sheet_id):
    """สร้าง Data Validation สำหรับประเภทโครงการ"""
    print("\n📋 กำลังสร้าง Dropdown ประเภทโครงการ...")
    
    # อ่านรายการประเภทโครงการจาก TOR_Config
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='TOR_Config!A2:A20'
        ).execute()
        
        values = result.get('values', [])
        project_types = [v[0] for v in values if v and v[0]]
        
        print(f"   พบประเภทโครงการ: {len(project_types)} รายการ")
        
        # สร้าง Data Validation
        validation_request = {
            'requests': [{
                'setDataValidation': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': 1,
                        'endRowIndex': 1000,
                        'startColumnIndex': 2,  # Column C (ประเภทโครงการ)
                        'endColumnIndex': 3
                    },
                    'rule': {
                        'condition': {
                            'type': 'ONE_OF_LIST',
                            'values': [{'userEnteredValue': pt} for pt in project_types]
                        },
                        'inputMessage': 'เลือกประเภทโครงการ',
                        'strict': True,
                        'showCustomUi': True
                    }
                }
            }]
        }
        
        service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body=validation_request
        ).execute()
        
        print("✅ สร้าง Dropdown สำเร็จ")
        
    except Exception as e:
        print(f"⚠️ ไม่สามารถสร้าง Dropdown ได้: {e}")

def create_budget_year_dropdown(service, sheet_id):
    """สร้าง Data Validation สำหรับปีงบประมาณ"""
    print("\n📅 กำลังสร้าง Dropdown ปีงบประมาณ...")
    
    budget_years = ['ปีงบประมาณ 2567', 'ปีงบประมาณ 2568', 'ปีงบประมาณ 2569', 
                    'ปีงบประมาณ 2570', 'ปีงบประมาณ 2571', 'ปีงบประมาณ 2572']
    
    validation_request = {
        'requests': [{
            'setDataValidation': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': 1000,
                    'startColumnIndex': 4,  # Column E (ปีงบประมาณ)
                    'endColumnIndex': 5
                },
                'rule': {
                    'condition': {
                        'type': 'ONE_OF_LIST',
                        'values': [{'userEnteredValue': year} for year in budget_years]
                    },
                    'inputMessage': 'เลือกปีงบประมาณ',
                    'strict': True,
                    'showCustomUi': True
                }
            }
        }]
    }
    
    service.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body=validation_request
    ).execute()
    
    print("✅ สร้าง Dropdown ปีงบประมาณสำเร็จ")

def create_status_dropdown(service, sheet_id):
    """สร้าง Data Validation สำหรับสถานะ"""
    print("\n✅ กำลังสร้าง Dropdown สถานะ...")
    
    statuses = ['Not Started', 'Approve', 'Reject']
    
    # Apply to columns F, G, H (status columns)
    for col_index in [5, 6, 7]:
        validation_request = {
            'requests': [{
                'setDataValidation': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': 1,
                        'endRowIndex': 1000,
                        'startColumnIndex': col_index,
                        'endColumnIndex': col_index + 1
                    },
                    'rule': {
                        'condition': {
                            'type': 'ONE_OF_LIST',
                            'values': [{'userEnteredValue': status} for status in statuses]
                        },
                        'inputMessage': 'เลือกสถานะ',
                        'strict': True,
                        'showCustomUi': True
                    }
                }
            }]
        }
        
        service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body=validation_request
        ).execute()
    
    print("✅ สร้าง Dropdown สถานะสำเร็จ")

def main():
    print("=" * 60)
    print("School Financial Approval - Create Projects Sheet")
    print("=" * 60)
    print()
    
    try:
        service = get_service()
        print("✅ เชื่อมต่อ Google Sheets API สำเร็จ\n")
        
        # 1. Create sheet
        sheet_id = create_projects_sheet(service)
        
        # 2. Write data
        write_projects_data(service, sheet_id)
        
        # 3. Create dropdowns
        create_project_types_dropdown(service, sheet_id)
        create_budget_year_dropdown(service, sheet_id)
        create_status_dropdown(service, sheet_id)
        
        # Summary
        print("\n" + "=" * 60)
        print("✅ SETUP COMPLETE")
        print("=" * 60)
        print()
        print("📊 Sheet: Projects")
        print("   - 11 คอลัมน์")
        print("   - 8 โครงการตัวอย่าง")
        print("   - Dropdown: ประเภทโครงการ, ปีงบประมาณ, สถานะ")
        print()
        print("🔗 URL:")
        print(f"   https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid={sheet_id}")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
