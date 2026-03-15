import requests
import json
import csv
import time

BASE = 'https://lf-public.deq.utah.gov/WebLink/'
FOLDER_ID = 49703
REPO = 'Public'
OUT_CSV = 'weblink_49703_title_docdate_deq.csv'

HEADERS = {
    'Content-Type': 'application/json',
    'X-Lf-Suppress-Login-Redirect': '1',
}

LIST_URL = BASE + 'FolderListingService.aspx/GetFolderListing2'
IDS_URL = BASE + 'FolderListingService.aspx/GetFolderListingIds'
META_URL = BASE + 'FolderListingService.aspx/GetMetaData'


def get_session():
    session = requests.Session()
    session.get(BASE, timeout=30)
    return session


def fetch_listing_page(session, start, end, get_new):
    payload = {
        'repoName': REPO,
        'folderId': FOLDER_ID,
        'getNewListing': get_new,
        'start': start,
        'end': end,
        'sortColumn': None,
        'sortAscending': True,
    }
    resp = session.post(LIST_URL, data=json.dumps(payload), headers=HEADERS, timeout=60)
    resp.raise_for_status()
    return resp.json()['data']


def fetch_entry_ids(session):
    payload = {
        'repoName': REPO,
        'folderId': FOLDER_ID,
        'sortColumn': None,
        'sortAscending': True,
    }
    resp = session.post(IDS_URL, data=json.dumps(payload), headers=HEADERS, timeout=60)
    resp.raise_for_status()
    return resp.json()['data']


def fetch_metadata(session, entry_id):
    payload = {'repoName': REPO, 'entryId': entry_id}
    resp = session.post(META_URL, data=json.dumps(payload), headers=HEADERS, timeout=60)
    if resp.status_code != 200:
        return None
    return resp.json().get('data')


def extract_fields(meta):
    title = ''
    doc_date = ''
    deq_number = ''
    entry_name = ''
    if not meta:
        return entry_name, title, doc_date, deq_number
    path = meta.get('path') or ''
    if path:
        entry_name = path.split('\\')[-1]
    for f in meta.get('fInfo', []):
        field_name = f.get('name')
        vals = f.get('values') or []
        if not vals:
            continue
        if field_name == 'Title':
            title = vals[0]
        elif field_name == 'Document Date':
            doc_date = vals[0]
        elif field_name == 'DEQ Number':
            deq_number = vals[0]
    return entry_name, title, doc_date, deq_number


def main():
    session = get_session()
    entry_ids = fetch_entry_ids(session)
    rows = []
    for entry_id in entry_ids:
        meta = fetch_metadata(session, entry_id)
        name, title, doc_date, deq_number = extract_fields(meta)
        rows.append({
            'Name': name,
            'DEQ Number': deq_number,
            'Title': title,
            'Document Date': doc_date,
        })
        time.sleep(0.1)

    with open(OUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Name', 'DEQ Number', 'Title', 'Document Date'])
        writer.writeheader()
        writer.writerows(rows)

    print(f'Total entries: {len(entry_ids)}')
    print(f'Documents written: {len(rows)}')
    print(f'Wrote {len(rows)} rows to {OUT_CSV}')


if __name__ == '__main__':
    main()
