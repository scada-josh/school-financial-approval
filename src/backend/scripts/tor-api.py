#!/usr/bin/env python3
"""
School Financial Approval API Server
=====================================
Simple HTTP API for CRUD operations on Google Sheets
using Python built-in http.server

Sheets:
  - TOR_Config: ประเภทโครงการและหัวข้อ TOR
  - Projects: รายการโครงการและสถานะการอนุมัติ

Endpoints:
  # TOR Config
  GET    /api/tor/projects          - List all project types
  POST   /api/tor/projects          - Add new project type
  PUT    /api/tor/projects/{name}   - Update project type sections
  DELETE /api/tor/projects/{name}   - Delete project type
  GET    /api/tor/sections          - List all available sections

  # Projects (โครงการ)
  GET    /api/tracking/projects              - List all projects
  GET    /api/tracking/projects?year=2568    - Filter by budget year
  POST   /api/tracking/projects              - Add new project
  PUT    /api/tracking/projects/{id}         - Update project
  DELETE /api/tracking/projects/{id}         - Delete project
  GET    /api/tracking/years                 - List budget years
"""

import json
import urllib.parse
import urllib.request
import base64
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Upload configuration
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'uploads', 'documents')
os.makedirs(UPLOAD_DIR, exist_ok=True)

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

class GoogleSheetsClient:
    """Client for Google Sheets operations"""
    
    def __init__(self):
        self.service = self._get_service()
        self._tor_cache = None
        self._projects_cache = None
        self._settings_cache = None
    
    def _get_service(self):
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
    
    # ============ TOR Config Methods ============
    
    def get_tor_data(self):
        """Get all data from TOR_Config sheet"""
        if self._tor_cache is not None:
            return self._tor_cache
        
        result = self.service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='TOR_Config!A1:AC100'
        ).execute()
        
        self._tor_cache = result.get('values', [])
        return self._tor_cache
    
    def clear_tor_cache(self):
        self._tor_cache = None
    
    def get_all_tor_projects(self):
        """Get all project types with their sections"""
        data = self.get_tor_data()
        if not data or len(data) < 2:
            return []
        
        headers = data[0]
        projects = []
        
        for row in data[1:]:
            if not row or not row[0]:
                continue
            
            project = {'name': row[0], 'sections': {}}
            
            for i in range(1, len(headers)):
                if i < len(row):
                    project['sections'][headers[i]] = row[i] == '✅'
                else:
                    project['sections'][headers[i]] = False
            
            projects.append(project)
        
        return projects
    
    def get_all_sections(self):
        """Get list of all section names"""
        data = self.get_tor_data()
        if not data:
            return []
        return data[0][1:] if len(data[0]) > 1 else []
    
    def add_tor_project(self, name, sections=None):
        if not name:
            raise ValueError("Project name is required")
        
        projects = self.get_all_tor_projects()
        if any(p['name'] == name for p in projects):
            raise ValueError(f"Project '{name}' already exists")
        
        data = self.get_tor_data()
        headers = data[0] if data else []
        
        row = [name]
        for i in range(1, len(headers)):
            section_name = headers[i]
            if sections and section_name in sections:
                row.append('✅' if sections[section_name] else '❌')
            else:
                row.append('❌')
        
        self.service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range='TOR_Config!A1',
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body={'values': [row]}
        ).execute()
        
        self.clear_tor_cache()
        return {'name': name, 'sections': {h: False for h in headers[1:]}}
    
    def update_tor_project(self, name, sections):
        if not name:
            raise ValueError("Project name is required")
        
        data = self.get_tor_data()
        headers = data[0] if data else []
        
        row_index = None
        for i, row in enumerate(data[1:], start=2):
            if row and row[0] == name:
                row_index = i
                break
        
        if row_index is None:
            raise ValueError(f"Project '{name}' not found")
        
        row = [name]
        for i in range(1, len(headers)):
            section_name = headers[i]
            if section_name in sections:
                row.append('✅' if sections[section_name] else '❌')
            else:
                if i < len(data[row_index - 1]):
                    row.append(data[row_index - 1][i])
                else:
                    row.append('❌')
        
        self.service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f'TOR_Config!A{row_index}',
            valueInputOption='RAW',
            body={'values': [row]}
        ).execute()
        
        self.clear_tor_cache()
        return {'name': name, 'sections': sections}
    
    def delete_tor_project(self, name):
        if not name:
            raise ValueError("Project name is required")
        
        data = self.get_tor_data()
        
        row_index = None
        for i, row in enumerate(data[1:], start=2):
            if row and row[0] == name:
                row_index = i
                break
        
        if row_index is None:
            raise ValueError(f"Project '{name}' not found")
        
        spreadsheet = self.service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        sheet_id = None
        for sheet in spreadsheet['sheets']:
            if sheet['properties']['title'] == 'TOR_Config':
                sheet_id = sheet['properties']['sheetId']
                break
        
        if sheet_id is None:
            raise ValueError("Sheet not found")
        
        self.service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={
                'requests': [{
                    'deleteDimension': {
                        'range': {
                            'sheetId': sheet_id,
                            'dimension': 'ROWS',
                            'startIndex': row_index - 1,
                            'endIndex': row_index
                        }
                    }
                }]
            }
        ).execute()
        
        self.clear_tor_cache()
        return {'message': f"Project '{name}' deleted"}
    
    # ============ Projects Tracking Methods ============
    
    def get_projects_data(self):
        """Get all data from Projects sheet"""
        if self._projects_cache is not None:
            return self._projects_cache
        
        result = self.service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Projects!A1:K1000'
        ).execute()
        
        self._projects_cache = result.get('values', [])
        return self._projects_cache
    
    def clear_projects_cache(self):
        self._projects_cache = None
    
    def get_all_tracking_projects(self, year=None):
        """Get all tracking projects, optionally filter by year"""
        data = self.get_projects_data()
        if not data or len(data) < 2:
            return []
        
        headers = data[0]
        projects = []
        
        for row in data[1:]:
            if not row or not row[0]:
                continue
            
            project = {}
            for i, header in enumerate(headers):
                if i < len(row):
                    project[header] = row[i]
                else:
                    project[header] = ''
            
            # Filter by year if specified
            if year and project.get('ปีงบประมาณ') != year:
                continue
            
            projects.append(project)
        
        return projects
    
    def get_all_project_names(self):
        """Get list of all project names from Projects sheet"""
        data = self.get_projects_data()
        if not data or len(data) < 2:
            return []
        
        headers = data[0]
        name_col = None
        for i, h in enumerate(headers):
            if h == 'ชื่อโครงการ':
                name_col = i
                break
        
        if name_col is None:
            return []
        
        names = []
        for row in data[1:]:
            if len(row) > name_col and row[name_col]:
                names.append(row[name_col])
        
        return names
    
    def ensure_tor_submissions_sheet(self):
        """Ensure TOR_Submissions sheet exists, create if not"""
        try:
            spreadsheet = self.service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
            sheet_exists = False
            for sheet in spreadsheet['sheets']:
                if sheet['properties']['title'] == 'TOR_Submissions':
                    sheet_exists = True
                    break
            
            if not sheet_exists:
                # Create new sheet
                self.service.spreadsheets().batchUpdate(
                    spreadsheetId=SPREADSHEET_ID,
                    body={
                        'requests': [{
                            'addSheet': {
                                'properties': {
                                    'title': 'TOR_Submissions',
                                    'gridProperties': {
                                        'rowCount': 1000,
                                        'columnCount': 11
                                    }
                                }
                            }
                        }]
                    }
                ).execute()
                
                # Add headers
                headers = ['ID', 'วันที่ส่ง', 'ชื่อ', 'นามสกุล', 'อีเมล', 'ชื่อโครงการ', 'ชื่อไฟล์', 'สถานะ', 'เส้นทางไฟล์', 'Connectors', 'หมายเหตุ']
                self.service.spreadsheets().values().update(
                    spreadsheetId=SPREADSHEET_ID,
                    range='TOR_Submissions!A1',
                    valueInputOption='RAW',
                    body={'values': [headers]}
                ).execute()
        except Exception as e:
            print(f"Error ensuring TOR_Submissions sheet: {e}")
    
    def add_tor_submission(self, submission_data, submission_id=None):
        """Add a new TOR submission to the sheet"""
        self.ensure_tor_submissions_sheet()
        
        # Generate ID if not provided
        if submission_id is None:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=SPREADSHEET_ID,
                range='TOR_Submissions!A1:A1000'
            ).execute()
            
            values = result.get('values', [])
            max_num = 0
            for row in values[1:]:  # Skip header
                if row and row[0] and row[0].startswith('TOR'):
                    try:
                        num = int(row[0][3:])
                        max_num = max(max_num, num)
                    except:
                        pass
            
            submission_id = f"TOR{max_num + 1:03d}"
        
        row = [
            submission_id,
            submission_data.get('submittedAt', ''),
            submission_data.get('firstName', ''),
            submission_data.get('lastName', ''),
            submission_data.get('email', ''),
            submission_data.get('projectName', ''),
            submission_data.get('fileName', ''),
            submission_data.get('status', 'รอตรวจสอบ'),
            submission_data.get('filePath', ''),
            submission_data.get('channel', ''),
            submission_data.get('note', '')
        ]
        
        self.service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range='TOR_Submissions!A1',
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body={'values': [row]}
        ).execute()
        
        return submission_id
    
    def add_new_project_to_sheet(self, project_name, project_type='', project_description='', budget_year=''):
        """Add a new project to Projects sheet with full data"""
        data = self.get_projects_data()
        
        # Generate ID
        existing_ids = []
        for row in data[1:]:
            if row and row[0]:
                existing_ids.append(row[0])
        
        max_num = 0
        for pid in existing_ids:
            if pid.startswith('P'):
                try:
                    num = int(pid[1:])
                    max_num = max(max_num, num)
                except:
                    pass
        
        new_id = f"P{max_num + 1:03d}"
        
        now = datetime.now().strftime('%Y-%m-%d')
        # Columns: ID, ชื่อโครงการ, ประเภทโครงการ, คำอธิบายโครงการ, ปีงบประมาณ, หัวหน้าหน่วยงาน, หัวหน้าฝ่ายงบประมาณ, ผู้อำนวยการโรงเรียน, หมายเหตุ, วันที่สร้าง, วันที่แก้ไขล่าสุด
        row = [
            new_id, 
            project_name, 
            project_type, 
            project_description, 
            budget_year, 
            'Not Started', 
            'Not Started', 
            'Not Started', 
            '', 
            now, 
            now
        ]
        
        self.service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range='Projects!A1',
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body={'values': [row]}
        ).execute()
        
        self.clear_projects_cache()
        return new_id
    
    def get_budget_years(self):
        """Get list of unique budget years"""
        data = self.get_projects_data()
        if not data or len(data) < 2:
            return []
        
        # Find column index for ปีงบประมาณ
        headers = data[0]
        year_col = None
        for i, h in enumerate(headers):
            if h == 'ปีงบประมาณ':
                year_col = i
                break
        
        if year_col is None:
            return []
        
        years = set()
        for row in data[1:]:
            if len(row) > year_col and row[year_col]:
                years.add(row[year_col])
        
        return sorted(list(years))
    
    def add_tracking_project(self, project_data):
        """Add a new tracking project"""
        required_fields = ['ชื่อโครงการ', 'ประเภทโครงการ', 'ปีงบประมาณ']
        for field in required_fields:
            if not project_data.get(field):
                raise ValueError(f"'{field}' is required")
        
        # Generate ID
        data = self.get_projects_data()
        existing_ids = []
        for row in data[1:]:
            if row and row[0]:
                existing_ids.append(row[0])
        
        # Find next ID
        max_num = 0
        for pid in existing_ids:
            if pid.startswith('P'):
                try:
                    num = int(pid[1:])
                    max_num = max(max_num, num)
                except:
                    pass
        
        new_id = f"P{max_num + 1:03d}"
        
        # Build row
        now = datetime.now().strftime('%Y-%m-%d')
        row = [
            new_id,
            project_data.get('ชื่อโครงการ', ''),
            project_data.get('ประเภทโครงการ', ''),
            project_data.get('คำอธิบายโครงการ', ''),
            project_data.get('ปีงบประมาณ', ''),
            project_data.get('หัวหน้าหน่วยงาน', 'Not Started'),
            project_data.get('หัวหน้าฝ่ายงบประมาณ', 'Not Started'),
            project_data.get('ผู้อำนวยการโรงเรียน', 'Not Started'),
            project_data.get('หมายเหตุ', ''),
            now,
            now
        ]
        
        self.service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range='Projects!A1',
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body={'values': [row]}
        ).execute()
        
        self.clear_projects_cache()
        
        return {
            'id': new_id,
            'ชื่อโครงการ': project_data.get('ชื่อโครงการ'),
            'ประเภทโครงการ': project_data.get('ประเภทโครงการ'),
            'ปีงบประมาณ': project_data.get('ปีงบประมาณ')
        }
    
    def update_tracking_project(self, project_id, project_data):
        """Update a tracking project"""
        if not project_id:
            raise ValueError("Project ID is required")
        
        data = self.get_projects_data()
        
        row_index = None
        for i, row in enumerate(data[1:], start=2):
            if row and row[0] == project_id:
                row_index = i
                break
        
        if row_index is None:
            raise ValueError(f"Project '{project_id}' not found")
        
        # Build updated row
        headers = data[0]
        now = datetime.now().strftime('%Y-%m-%d')
        
        row = [project_id]
        for i in range(1, len(headers)):
            header = headers[i]
            if header in project_data:
                row.append(project_data[header])
            elif i < len(data[row_index - 1]):
                row.append(data[row_index - 1][i])
            else:
                row.append('')
        
        # Update last modified date
        if len(headers) > 10:  # Assuming column K is วันที่แก้ไขล่าสุด
            row[10] = now
        
        self.service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f'Projects!A{row_index}',
            valueInputOption='RAW',
            body={'values': [row]}
        ).execute()
        
        self.clear_projects_cache()
        return {'id': project_id, 'updated': True}
    
    def delete_tracking_project(self, project_id):
        """Delete a tracking project"""
        if not project_id:
            raise ValueError("Project ID is required")
        
        data = self.get_projects_data()
        
        row_index = None
        for i, row in enumerate(data[1:], start=2):
            if row and row[0] == project_id:
                row_index = i
                break
        
        if row_index is None:
            raise ValueError(f"Project '{project_id}' not found")
        
        spreadsheet = self.service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        sheet_id = None
        for sheet in spreadsheet['sheets']:
            if sheet['properties']['title'] == 'Projects':
                sheet_id = sheet['properties']['sheetId']
                break
        
        if sheet_id is None:
            raise ValueError("Sheet not found")
        
        self.service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={
                'requests': [{
                    'deleteDimension': {
                        'range': {
                            'sheetId': sheet_id,
                            'dimension': 'ROWS',
                            'startIndex': row_index - 1,
                            'endIndex': row_index
                        }
                    }
                }]
            }
        ).execute()
        
        self.clear_projects_cache()
        return {'message': f"Project '{project_id}' deleted"}
    
    # ============ Settings Methods ============
    
    def _ensure_settings_sheet(self):
        """Ensure Settings sheet exists"""
        try:
            spreadsheet = self.service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
            sheet_exists = any(sheet['properties']['title'] == 'Settings' for sheet in spreadsheet['sheets'])
            
            if not sheet_exists:
                # Create Settings sheet
                self.service.spreadsheets().batchUpdate(
                    spreadsheetId=SPREADSHEET_ID,
                    body={
                        'requests': [{
                            'addSheet': {
                                'properties': {
                                    'title': 'Settings',
                                    'gridProperties': {
                                        'rowCount': 100,
                                        'columnCount': 3
                                    }
                                }
                            }
                        }]
                    }
                ).execute()
                
                # Add headers
                self.service.spreadsheets().values().update(
                    spreadsheetId=SPREADSHEET_ID,
                    range='Settings!A1:C1',
                    valueInputOption='RAW',
                    body={'values': [['Category', 'Key', 'Value']]}
                ).execute()
                
                # Add default settings
                default_settings = [
                    ['General', 'APP_NAME', 'School Financial Approval Project'],
                    ['General', 'VERSION', '1.0.0'],
                    ['General', 'DEFAULT_LANG', 'th'],
                    ['Connectors', 'N8N_ENABLED', 'false'],
                    ['Connectors', 'N8N_WEBHOOK_URL', ''],
                    ['Connectors', 'N8N_API_KEY', ''],
                    ['Connectors', 'N8N_WORKFLOW_ID', ''],
                    ['Connectors', 'N8N_DESCRIPTION', 'n8n workflow automation connector']
                ]
                
                self.service.spreadsheets().values().append(
                    spreadsheetId=SPREADSHEET_ID,
                    range='Settings!A1',
                    valueInputOption='RAW',
                    insertDataOption='INSERT_ROWS',
                    body={'values': default_settings}
                ).execute()
        except Exception as e:
            print(f"Error ensuring settings sheet: {e}")
    
    def get_settings(self):
        """Get all settings from Settings sheet"""
        if self._settings_cache is not None:
            return self._settings_cache
        
        self._ensure_settings_sheet()
        
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=SPREADSHEET_ID,
                range='Settings!A1:C100'
            ).execute()
            
            data = result.get('values', [])
            if not data or len(data) < 2:
                return {}
            
            settings = {}
            for row in data[1:]:
                if len(row) >= 3:
                    category, key, value = row[0], row[1], row[2]
                    if category not in settings:
                        settings[category] = {}
                    settings[category][key] = value
            
            self._settings_cache = settings
            return settings
        except Exception as e:
            print(f"Error getting settings: {e}")
            return {}
    
    def clear_settings_cache(self):
        """Clear settings cache"""
        self._settings_cache = None
    
    def update_settings(self, settings_data):
        """Update settings in Settings sheet"""
        self._ensure_settings_sheet()
        
        # Get current data
        result = self.service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Settings!A1:C100'
        ).execute()
        
        data = result.get('values', [])
        if not data:
            raise ValueError("Settings sheet is empty")
        
        # Build update requests
        updates = []
        for i, row in enumerate(data[1:], start=2):
            if len(row) >= 2:
                category, key = row[0], row[1]
                if category in settings_data and key in settings_data[category]:
                    new_value = settings_data[category][key]
                    updates.append({
                        'range': f'Settings!C{i}',
                        'values': [[new_value]]
                    })
        
        if updates:
            self.service.spreadsheets().values().batchUpdate(
                spreadsheetId=SPREADSHEET_ID,
                body={'valueInputOption': 'RAW', 'data': updates}
            ).execute()
        
        self.clear_settings_cache()
        return {'message': 'Settings updated successfully'}


# Initialize client
sheets_client = GoogleSheetsClient()


class APIHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for School Financial Approval API"""
    
    def _set_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()
    
    def do_OPTIONS(self):
        self._set_headers()
    
    def _send_json(self, data, status=200):
        self._set_headers(status)
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def _read_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            body = self.rfile.read(content_length)
            return json.loads(body.decode('utf-8'))
        return {}
    
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query = urllib.parse.parse_qs(parsed_path.query)
        
        try:
            # TOR Config endpoints
            if path == '/api/tor/projects':
                projects = sheets_client.get_all_tor_projects()
                self._send_json({'success': True, 'data': projects})
            
            elif path == '/api/tor/sections':
                sections = sheets_client.get_all_sections()
                self._send_json({'success': True, 'data': sections})
            
            elif path == '/api/tor/project-names':
                names = sheets_client.get_all_project_names()
                self._send_json({'success': True, 'data': names})
            
            # Project Tracking endpoints
            elif path == '/api/tracking/projects':
                year = query.get('year', [None])[0]
                projects = sheets_client.get_all_tracking_projects(year)
                self._send_json({'success': True, 'data': projects})
            
            elif path == '/api/tracking/years':
                years = sheets_client.get_budget_years()
                self._send_json({'success': True, 'data': years})
            
            # Settings endpoints
            elif path == '/api/settings':
                settings = sheets_client.get_settings()
                self._send_json({'success': True, 'data': settings})
            
            else:
                self._send_json({'success': False, 'error': 'Not found'}, 404)
        
        except Exception as e:
            self._send_json({'success': False, 'error': str(e)}, 500)
    
    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        try:
            # TOR Config endpoints
            if path == '/api/tor/projects':
                body = self._read_body()
                name = body.get('name')
                sections = body.get('sections', {})
                result = sheets_client.add_tor_project(name, sections)
                self._send_json({'success': True, 'data': result}, 201)
            
            # TOR Submit endpoint
            elif path == '/api/tor/submit':
                body = self._read_body()
                first_name = body.get('firstName', '').strip()
                last_name = body.get('lastName', '').strip()
                email = body.get('email', '').strip()
                project_name = body.get('projectName', '').strip()
                is_new_project = body.get('isNewProject', False)
                project_type = body.get('projectType', '').strip()
                project_description = body.get('projectDescription', '').strip()
                budget_year = body.get('budgetYear', '').strip()
                file_name = body.get('fileName', '')
                file_data = body.get('fileData', '')
                
                if not first_name or not last_name or not email:
                    raise ValueError("First name, last name, and email are required")
                
                if not project_name:
                    raise ValueError("Project name is required")
                
                if is_new_project:
                    if not project_type:
                        raise ValueError("Project type is required for new projects")
                    if not budget_year:
                        raise ValueError("Budget year is required for new projects")
                
                if not file_name or not file_data:
                    raise ValueError("File is required")
                
                # If new project, add to Projects sheet with full details
                if is_new_project:
                    try:
                        sheets_client.add_new_project_to_sheet(
                            project_name, 
                            project_type=project_type,
                            project_description=project_description,
                            budget_year=budget_year
                        )
                    except Exception as e:
                        print(f"Warning: Could not add new project to sheet: {e}")
                
                # Generate unique filename
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                safe_name = ''.join(c if c.isalnum() or c in '._-' else '_' for c in file_name)
                unique_filename = f"{timestamp}_{safe_name}"
                file_path = os.path.join(UPLOAD_DIR, unique_filename)
                
                # Decode and save file
                file_bytes = base64.b64decode(file_data)
                with open(file_path, 'wb') as f:
                    f.write(file_bytes)
                
                # Check n8n settings
                n8n_enabled = False
                n8n_webhook_url = ''
                n8n_api_key = ''
                n8n_workflow_id = ''
                channel = ''
                webhook_status = 'ไม่ได้ส่ง'
                
                try:
                    settings = sheets_client.get_settings()
                    if 'Connectors' in settings:
                        n8n_enabled = settings['Connectors'].get('N8N_ENABLED', 'false').lower() == 'true'
                        n8n_webhook_url = settings['Connectors'].get('N8N_WEBHOOK_URL', '')
                        n8n_api_key = settings['Connectors'].get('N8N_API_KEY', '')
                        n8n_workflow_id = settings['Connectors'].get('N8N_WORKFLOW_ID', '')
                except Exception as e:
                    print(f"Warning: Could not load settings: {e}")
                
                # Send to n8n if enabled
                if n8n_enabled and n8n_webhook_url:
                    try:
                        webhook_payload = {
                            'event': 'tor_submitted',
                            'submission': {
                                'firstName': first_name,
                                'lastName': last_name,
                                'email': email,
                                'projectName': project_name,
                                'isNewProject': is_new_project,
                                'projectType': project_type,
                                'projectDescription': project_description,
                                'budgetYear': budget_year,
                                'fileName': file_name,
                                'submittedAt': datetime.now().isoformat()
                            }
                        }
                        
                        req = urllib.request.Request(
                            n8n_webhook_url,
                            data=json.dumps(webhook_payload).encode('utf-8'),
                            headers={
                                'Content-Type': 'application/json',
                                'X-N8N-API-KEY': n8n_api_key,
                                'X-Workflow-ID': n8n_workflow_id
                            },
                            method='POST'
                        )
                        
                        with urllib.request.urlopen(req, timeout=10) as response:
                            if response.status == 200:
                                webhook_status = 'ส่งสำเร็จ'
                                channel = 'n8n Workflow'
                            else:
                                webhook_status = f'ส่งไม่สำเร็จ (HTTP {response.status})'
                                channel = 'n8n Workflow'
                    except Exception as e:
                        webhook_status = f'ส่งไม่สำเร็จ: {str(e)}'
                        channel = 'n8n Workflow'
                
                # Save to Google Sheet TOR_Submissions
                submitted_at = datetime.now().isoformat()
                
                try:
                    # Generate submission ID once
                    submission_id = sheets_client.add_tor_submission({
                        'firstName': first_name,
                        'lastName': last_name,
                        'email': email,
                        'projectName': project_name,
                        'fileName': unique_filename,
                        'status': 'อัพโหลดสำเร็จ',
                        'note': 'ส่ง TOR ใหม่' if is_new_project else '',
                        'filePath': file_path,
                        'submittedAt': submitted_at,
                        'channel': 'Default'
                    })
                    
                    # Record 2: n8n connector (if enabled)
                    if n8n_enabled and channel:
                        sheets_client.add_tor_submission({
                            'firstName': first_name,
                            'lastName': last_name,
                            'email': email,
                            'projectName': project_name,
                            'fileName': unique_filename,
                            'status': webhook_status,
                            'note': 'ส่งผ่าน n8n Workflow',
                            'filePath': file_path,
                            'submittedAt': submitted_at,
                            'channel': channel
                        }, submission_id=submission_id)
                except Exception as e:
                    print(f"Warning: Could not save to sheet: {e}")
                    submission_id = None
                
                # Save metadata to JSON
                metadata = {
                    'firstName': first_name,
                    'lastName': last_name,
                    'email': email,
                    'projectName': project_name,
                    'isNewProject': is_new_project,
                    'projectType': project_type,
                    'projectDescription': project_description,
                    'budgetYear': budget_year,
                    'originalFileName': file_name,
                    'savedFileName': unique_filename,
                    'filePath': file_path,
                    'fileSize': len(file_bytes),
                    'submittedAt': submitted_at,
                    'submissionId': submission_id
                }
                
                metadata_path = os.path.join(UPLOAD_DIR, f"{timestamp}_{first_name}_{last_name}.json")
                with open(metadata_path, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, ensure_ascii=False, indent=2)
                
                self._send_json({
                    'success': True,
                    'data': {
                        'message': 'TOR submitted successfully',
                        'fileName': unique_filename,
                        'fileSize': len(file_bytes),
                        'projectName': project_name,
                        'submissionId': submission_id
                    }
                }, 201)
            
            # Project Tracking endpoints
            elif path == '/api/tracking/projects':
                body = self._read_body()
                result = sheets_client.add_tracking_project(body)
                self._send_json({'success': True, 'data': result}, 201)
            
            else:
                self._send_json({'success': False, 'error': 'Not found'}, 404)
        
        except ValueError as e:
            self._send_json({'success': False, 'error': str(e)}, 400)
        except Exception as e:
            self._send_json({'success': False, 'error': str(e)}, 500)
    
    def do_PUT(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        try:
            # TOR Config endpoints
            if path.startswith('/api/tor/projects/'):
                name = urllib.parse.unquote(path[len('/api/tor/projects/'):])
                body = self._read_body()
                sections = body.get('sections', {})
                result = sheets_client.update_tor_project(name, sections)
                self._send_json({'success': True, 'data': result})
            
            # Project Tracking endpoints
            elif path.startswith('/api/tracking/projects/'):
                project_id = urllib.parse.unquote(path[len('/api/tracking/projects/'):])
                body = self._read_body()
                result = sheets_client.update_tracking_project(project_id, body)
                self._send_json({'success': True, 'data': result})
            
            # Settings endpoints
            elif path == '/api/settings':
                body = self._read_body()
                result = sheets_client.update_settings(body)
                self._send_json({'success': True, 'data': result})
            
            else:
                self._send_json({'success': False, 'error': 'Not found'}, 404)
        
        except ValueError as e:
            self._send_json({'success': False, 'error': str(e)}, 400)
        except Exception as e:
            self._send_json({'success': False, 'error': str(e)}, 500)
    
    def do_DELETE(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        try:
            # TOR Config endpoints
            if path.startswith('/api/tor/projects/'):
                name = urllib.parse.unquote(path[len('/api/tor/projects/'):])
                result = sheets_client.delete_tor_project(name)
                self._send_json({'success': True, 'data': result})
            
            # Project Tracking endpoints
            elif path.startswith('/api/tracking/projects/'):
                project_id = urllib.parse.unquote(path[len('/api/tracking/projects/'):])
                result = sheets_client.delete_tracking_project(project_id)
                self._send_json({'success': True, 'data': result})
            
            else:
                self._send_json({'success': False, 'error': 'Not found'}, 404)
        
        except ValueError as e:
            self._send_json({'success': False, 'error': str(e)}, 400)
        except Exception as e:
            self._send_json({'success': False, 'error': str(e)}, 500)
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass


def run_server(port=8765):
    """Run the API server"""
    server = HTTPServer(('localhost', port), APIHandler)
    print(f"🚀 School Financial Approval API Server running at http://localhost:{port}")
    print(f"📋 Endpoints:")
    print(f"")
    print(f"  TOR Config:")
    print(f"   GET    /api/tor/projects          - List all project types")
    print(f"   POST   /api/tor/projects          - Add new project type")
    print(f"   PUT    /api/tor/projects/{{name}}   - Update project type")
    print(f"   DELETE /api/tor/projects/{{name}}   - Delete project type")
    print(f"   GET    /api/tor/sections          - List all sections")
    print(f"   POST   /api/tor/submit            - Submit TOR file")
    print(f"")
    print(f"  Project Tracking:")
    print(f"   GET    /api/tracking/projects              - List all projects")
    print(f"   GET    /api/tracking/projects?year=2568    - Filter by budget year")
    print(f"   POST   /api/tracking/projects              - Add new project")
    print(f"   PUT    /api/tracking/projects/{{id}}         - Update project")
    print(f"   DELETE /api/tracking/projects/{{id}}         - Delete project")
    print(f"   GET    /api/tracking/years                 - List budget years")
    print(f"")
    print(f"📁 Upload directory: {UPLOAD_DIR}")
    print(f"")
    print(f"Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
        server.shutdown()


if __name__ == '__main__':
    run_server()
