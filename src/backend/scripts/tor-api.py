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
import mimetypes
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Base directory (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Upload configuration
UPLOAD_DIR = os.environ.get('UPLOAD_DIR', os.path.join(BASE_DIR, 'uploads', 'documents'))
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Configuration
SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID', '1Plh_0AodTomKLyP8zrBp9FOriHXVm_uGYIO4TVHSozg')
SERVICE_ACCOUNT_EMAIL = os.environ.get('GOOGLE_CLIENT_EMAIL', 'opencode-gsheet@gen-lang-client-0476777034.iam.gserviceaccount.com')
PRIVATE_KEY = os.environ.get('GOOGLE_PRIVATE_KEY')
        if not PRIVATE_KEY:
            # Service account JSON is preferred; this is a fallback
            PRIVATE_KEY = ''

# Validate that required credentials are available
if not os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON') and not os.environ.get('GOOGLE_PRIVATE_KEY'):
    print("⚠️  Warning: No Google credentials found in environment variables.")
    print("   Please set GOOGLE_SERVICE_ACCOUNT_JSON or GOOGLE_PRIVATE_KEY before running.")

class GoogleSheetsClient:
    """Client for Google Sheets operations"""
    
    def __init__(self):
        self.service = self._get_service()
        self._tor_cache = None
        self._projects_cache = None
        self._settings_cache = None
    
    def _get_service(self):
        # Try loading from GOOGLE_SERVICE_ACCOUNT_JSON env var first
        service_account_json = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON')
        if service_account_json:
            try:
                account_info = json.loads(service_account_json)
            except json.JSONDecodeError:
                raise ValueError("Invalid GOOGLE_SERVICE_ACCOUNT_JSON environment variable")
        else:
            # Fallback to individual env vars or hardcoded defaults
            account_info = {
                "type": "service_account",
                "project_id": os.environ.get('GOOGLE_PROJECT_ID', 'gen-lang-client-0476777034'),
                "private_key_id": os.environ.get('GOOGLE_PRIVATE_KEY_ID', 'key-id'),
                "private_key": PRIVATE_KEY,
                "client_email": SERVICE_ACCOUNT_EMAIL,
                "client_id": os.environ.get('GOOGLE_CLIENT_ID', 'client-id'),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        
        credentials = service_account.Credentials.from_service_account_info(
            account_info,
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
                    ['Connectors', 'N8N_DESCRIPTION', 'n8n workflow automation connector'],
                    ['Profiles', 'PROFILE_LIST', '["Default"]'],
                    ['Profiles', 'ACTIVE_PROFILE', 'Default'],
                    ['Profile_Default', 'N8N_ENABLED', 'false'],
                    ['Profile_Default', 'N8N_WEBHOOK_URL', ''],
                    ['Profile_Default', 'N8N_API_KEY', ''],
                    ['Profile_Default', 'N8N_WORKFLOW_ID', '']
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

    # ============ Profile Methods ============

    def get_profiles(self):
        """Get all profiles and active profile"""
        settings = self.get_settings()
        profiles = {
            'profiles': [],
            'active_profile': 'Default'
        }

        if 'Profiles' in settings:
            # Get profile list
            profile_list_str = settings['Profiles'].get('PROFILE_LIST', '[]')
            try:
                profiles['profiles'] = json.loads(profile_list_str)
            except:
                profiles['profiles'] = []

            # Get active profile
            profiles['active_profile'] = settings['Profiles'].get('ACTIVE_PROFILE', 'Default')

        # Ensure at least Default profile exists
        if not profiles['profiles']:
            profiles['profiles'] = ['Default']
            profiles['active_profile'] = 'Default'

        return profiles

    def get_profile(self, name):
        """Get profile config by name"""
        settings = self.get_settings()
        profile_key = f'Profile_{name}'

        if profile_key in settings:
            return settings[profile_key]

        # Return empty config if profile not found
        return {
            'N8N_ENABLED': 'false',
            'N8N_WEBHOOK_URL': '',
            'N8N_API_KEY': '',
            'N8N_WORKFLOW_ID': ''
        }

    def save_profile(self, name, config):
        """Save or update a profile"""
        self.clear_settings_cache()
        
        settings = self.get_settings()
        profiles_data = self.get_profiles()
        profiles = profiles_data['profiles']

        # Add profile to list if new
        if name not in profiles:
            profiles.append(name)

        # Update settings data
        if 'Profiles' not in settings:
            settings['Profiles'] = {}

        settings['Profiles']['PROFILE_LIST'] = json.dumps(profiles)

        # Save profile config
        profile_key = f'Profile_{name}'
        if profile_key not in settings:
            settings[profile_key] = {}

        for key, value in config.items():
            settings[profile_key][key] = value

        # Update all settings in sheet
        self._update_settings_from_dict(settings)
        self.clear_settings_cache()

        return {'name': name, 'config': config}

    def delete_profile(self, name):
        """Delete a profile"""
        if name == 'Default':
            raise ValueError("Cannot delete Default profile")

        # Clear cache to get fresh data
        self.clear_settings_cache()
        
        profiles_data = self.get_profiles()
        profiles = profiles_data['profiles']

        if name not in profiles:
            raise ValueError(f"Profile '{name}' not found")

        profiles.remove(name)

        settings = self.get_settings()
        settings['Profiles']['PROFILE_LIST'] = json.dumps(profiles)

        # Remove profile config
        profile_key = f'Profile_{name}'
        if profile_key in settings:
            del settings[profile_key]

        # Update active profile if deleted profile was active
        if profiles_data['active_profile'] == name:
            settings['Profiles']['ACTIVE_PROFILE'] = 'Default'

        self._update_settings_from_dict(settings)
        self.clear_settings_cache()

        return {'message': f"Profile '{name}' deleted"}

    def set_active_profile(self, name):
        """Set active profile"""
        profiles_data = self.get_profiles()

        if name not in profiles_data['profiles']:
            raise ValueError(f"Profile '{name}' not found")

        settings = self.get_settings()
        if 'Profiles' not in settings:
            settings['Profiles'] = {}

        settings['Profiles']['ACTIVE_PROFILE'] = name

        self._update_settings_from_dict(settings)
        self.clear_settings_cache()

        return {'active_profile': name}

    def _update_settings_from_dict(self, settings_dict):
        """Update settings sheet from dictionary - syncs exactly what's in the dict"""
        result = self.service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Settings!A1:C200'
        ).execute()

        data = result.get('values', [])
        if not data:
            raise ValueError("Settings sheet is empty")

        # Build a map of existing rows
        existing_rows = {}
        for i, row in enumerate(data[1:], start=2):
            if len(row) >= 2:
                key = f"{row[0]}:{row[1]}"
                existing_rows[key] = i

        # Build set of keys that should exist
        desired_keys = set()
        for category, items in settings_dict.items():
            for key in items.keys():
                desired_keys.add(f"{category}:{key}")

        # Find rows to delete (exist in sheet but not in desired dict)
        rows_to_delete = []
        for row_key, row_num in existing_rows.items():
            if row_key not in desired_keys:
                rows_to_delete.append(row_num)

        # Delete rows in reverse order to maintain indices
        if rows_to_delete:
            spreadsheet = self.service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
            sheet_id = None
            for sheet in spreadsheet['sheets']:
                if sheet['properties']['title'] == 'Settings':
                    sheet_id = sheet['properties']['sheetId']
                    break
            
            if sheet_id is not None:
                # Sort descending and merge consecutive rows
                rows_to_delete.sort(reverse=True)
                delete_requests = []
                for row_num in rows_to_delete:
                    delete_requests.append({
                        'deleteDimension': {
                            'range': {
                                'sheetId': sheet_id,
                                'dimension': 'ROWS',
                                'startIndex': row_num - 1,
                                'endIndex': row_num
                            }
                        }
                    })
                
                if delete_requests:
                    self.service.spreadsheets().batchUpdate(
                        spreadsheetId=SPREADSHEET_ID,
                        body={'requests': delete_requests}
                    ).execute()

        # Re-fetch data after deletion
        result = self.service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Settings!A1:C200'
        ).execute()
        data = result.get('values', [])

        # Rebuild existing_rows map
        existing_rows = {}
        for i, row in enumerate(data[1:], start=2):
            if len(row) >= 2:
                key = f"{row[0]}:{row[1]}"
                existing_rows[key] = i

        # Prepare updates and appends
        updates = []
        appends = []

        for category, items in settings_dict.items():
            for key, value in items.items():
                row_key = f"{category}:{key}"
                if row_key in existing_rows:
                    # Update existing row
                    row_num = existing_rows[row_key]
                    updates.append({
                        'range': f'Settings!C{row_num}',
                        'values': [[str(value)]]
                    })
                else:
                    # Append new row
                    appends.append([category, key, str(value)])

        # Execute updates
        if updates:
            self.service.spreadsheets().values().batchUpdate(
                spreadsheetId=SPREADSHEET_ID,
                body={'valueInputOption': 'RAW', 'data': updates}
            ).execute()

        # Execute appends
        if appends:
            self.service.spreadsheets().values().append(
                spreadsheetId=SPREADSHEET_ID,
                range='Settings!A1',
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body={'values': appends}
            ).execute()

    def rename_profile(self, old_name, new_name):
        """Rename a profile and its config"""
        if old_name == 'Default':
            raise ValueError("Cannot rename Default profile")
        
        if old_name == new_name:
            return {'message': f"Profile name unchanged"}
        
        self.clear_settings_cache()
        
        profiles_data = self.get_profiles()
        profiles = profiles_data['profiles']
        
        if old_name not in profiles:
            raise ValueError(f"Profile '{old_name}' not found")
        
        if new_name in profiles:
            raise ValueError(f"Profile '{new_name}' already exists")
        
        # Get old config
        old_config = self.get_profile(old_name)
        
        # Update profile list
        index = profiles.index(old_name)
        profiles[index] = new_name
        
        settings = self.get_settings()
        settings['Profiles']['PROFILE_LIST'] = json.dumps(profiles)
        
        # Update active profile if needed
        if profiles_data['active_profile'] == old_name:
            settings['Profiles']['ACTIVE_PROFILE'] = new_name
        
        # Remove old profile config from dict (will be deleted from sheet)
        old_key = f'Profile_{old_name}'
        if old_key in settings:
            del settings[old_key]
        
        # Add new profile config
        new_key = f'Profile_{new_name}'
        settings[new_key] = old_config
        
        # Update sheet
        self._update_settings_from_dict(settings)
        self.clear_settings_cache()
        
        return {'old_name': old_name, 'new_name': new_name}


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
    
    def _serve_static(self, path):
        """Serve static files from the project root"""
        # Security: prevent path traversal
        if '..' in path or '~' in path:
            self._send_json({'success': False, 'error': 'Not found'}, 404)
            return
        
        if path == '/' or path == '':
            filepath = os.path.join(BASE_DIR, 'index.html')
        else:
            clean_path = path.lstrip('/')
            filepath = os.path.join(BASE_DIR, clean_path)
        
        # Ensure path is within BASE_DIR
        real_filepath = os.path.realpath(filepath)
        real_base = os.path.realpath(BASE_DIR)
        if not real_filepath.startswith(real_base):
            self._send_json({'success': False, 'error': 'Not found'}, 404)
            return
        
        if not os.path.exists(filepath) or not os.path.isfile(filepath):
            self._send_json({'success': False, 'error': 'Not found'}, 404)
            return
        
        content_type, _ = mimetypes.guess_type(filepath)
        if content_type is None:
            content_type = 'application/octet-stream'
        
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'public, max-age=3600')
        self.end_headers()
        
        with open(filepath, 'rb') as f:
            self.wfile.write(f.read())

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query = urllib.parse.parse_qs(parsed_path.query)
        
        # Serve static files for non-API routes
        if not path.startswith('/api/'):
            self._serve_static(path)
            return
        
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

            # Profile endpoints
            elif path == '/api/profiles':
                profiles = sheets_client.get_profiles()
                self._send_json({'success': True, 'data': profiles})

            elif path.startswith('/api/profiles/'):
                path_parts = path.split('/')
                if len(path_parts) >= 4:
                    profile_name = urllib.parse.unquote(path_parts[3])
                    if profile_name:
                        profile_config = sheets_client.get_profile(profile_name)
                        self._send_json({'success': True, 'data': {'name': profile_name, 'config': profile_config}})
                    else:
                        self._send_json({'success': False, 'error': 'Profile name is required'}, 400)
                else:
                    self._send_json({'success': False, 'error': 'Invalid path'}, 400)

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
                
                # Check n8n settings from active profile
                n8n_enabled = False
                n8n_webhook_url = ''
                n8n_api_key = ''
                n8n_workflow_id = ''
                channel = ''
                webhook_status = 'ไม่ได้ส่ง'
                
                try:
                    profiles_data = sheets_client.get_profiles()
                    active_profile = profiles_data.get('active_profile', 'Default')
                    profile_config = sheets_client.get_profile(active_profile)
                    
                    n8n_enabled = profile_config.get('N8N_ENABLED', 'false').lower() == 'true'
                    n8n_webhook_url = profile_config.get('N8N_WEBHOOK_URL', '')
                    n8n_api_key = profile_config.get('N8N_API_KEY', '')
                    n8n_workflow_id = profile_config.get('N8N_WORKFLOW_ID', '')
                except Exception as e:
                    print(f"Warning: Could not load profile settings: {e}")
                
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

            # Profile endpoints
            elif path == '/api/profiles':
                body = self._read_body()
                name = body.get('name')
                config = body.get('config', {})
                if not name:
                    raise ValueError("Profile name is required")
                result = sheets_client.save_profile(name, config)
                self._send_json({'success': True, 'data': result}, 201)

            # Profile rename endpoint
            elif path == '/api/profiles/rename':
                body = self._read_body()
                old_name = body.get('old_name')
                new_name = body.get('new_name')
                if not old_name or not new_name:
                    raise ValueError("old_name and new_name are required")
                result = sheets_client.rename_profile(old_name, new_name)
                self._send_json({'success': True, 'data': result})

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

            # Profile endpoints
            elif path.startswith('/api/profiles/active/'):
                profile_name = urllib.parse.unquote(path[len('/api/profiles/active/'):])
                result = sheets_client.set_active_profile(profile_name)
                self._send_json({'success': True, 'data': result})

            elif path.startswith('/api/profiles/'):
                profile_name = urllib.parse.unquote(path[len('/api/profiles/'):])
                body = self._read_body()
                config = body.get('config', {})
                result = sheets_client.save_profile(profile_name, config)
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

            # Profile endpoints
            elif path.startswith('/api/profiles/'):
                profile_name = urllib.parse.unquote(path[len('/api/profiles/'):])
                result = sheets_client.delete_profile(profile_name)
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


def run_server(port=None):
    """Run the API server"""
    port = int(os.environ.get('PORT', port or 8765))
    host = os.environ.get('HOST', '0.0.0.0')
    server = HTTPServer((host, port), APIHandler)
    print(f"🚀 School Financial Approval API Server running at http://{host}:{port}")
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
    print(f"  Profiles:")
    print(f"   GET    /api/profiles                        - List all profiles")
    print(f"   GET    /api/profiles/{{name}}                  - Get profile config")
    print(f"   POST   /api/profiles                        - Create profile")
    print(f"   PUT    /api/profiles/{{name}}                  - Update profile")
    print(f"   PUT    /api/profiles/active/{{name}}           - Set active profile")
    print(f"   DELETE /api/profiles/{{name}}                  - Delete profile")
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
