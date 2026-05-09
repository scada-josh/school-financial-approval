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
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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
            
            # Project Tracking endpoints
            elif path == '/api/tracking/projects':
                year = query.get('year', [None])[0]
                projects = sheets_client.get_all_tracking_projects(year)
                self._send_json({'success': True, 'data': projects})
            
            elif path == '/api/tracking/years':
                years = sheets_client.get_budget_years()
                self._send_json({'success': True, 'data': years})
            
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
    print(f"")
    print(f"  Project Tracking:")
    print(f"   GET    /api/tracking/projects              - List all projects")
    print(f"   GET    /api/tracking/projects?year=2568    - Filter by budget year")
    print(f"   POST   /api/tracking/projects              - Add new project")
    print(f"   PUT    /api/tracking/projects/{{id}}         - Update project")
    print(f"   DELETE /api/tracking/projects/{{id}}         - Delete project")
    print(f"   GET    /api/tracking/years                 - List budget years")
    print(f"")
    print(f"Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
        server.shutdown()


if __name__ == '__main__':
    run_server()
