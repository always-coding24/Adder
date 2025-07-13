
import requests
from bs4 import BeautifulSoup
import time
import re
import sys
import signal

# --- Configuration ---
EMAIL = "imodumicheal519@gmail.com"
PASSWORD = "Aliumicheal23."
MAGIC_RECAPTCHA_TOKEN = "09ANMylNCxCsR-EALV_dP3Uu9rxSkQG-0xTH4zhiW(AwivWepExAlRqCrvuEUPLATuySMYLrpy9fmeab6yOPTYLcHu8ryQ2sf3mkJCsRhoVj6IOkQDcIdLm49TAGADj_M6K"

# --- API Endpoints ---
BASE_URL = "https://www.ivasms.com"
LOGIN_URL = f"{BASE_URL}/login"
TEST_NUMBERS_PAGE_URL = f"{BASE_URL}/portal/numbers/test"
TEST_NUMBERS_API_URL = f"{BASE_URL}/portal/numbers/test"
ADD_NUMBER_API_URL = f"{BASE_URL}/portal/numbers/termination/number/add"

def graceful_shutdown(signum, frame):
    print("\n\n[!] Shutdown signal detected. Exiting.")
    sys.exit(0)

def add_number_range(session, range_name):
  
    print(f"\n--- Attempting to add a number from range: '{range_name}' ---")
    try:
       
        page_response = session.get(TEST_NUMBERS_PAGE_URL)
        page_response.raise_for_status()
        soup = BeautifulSoup(page_response.text, 'html.parser')
        token_tag = soup.find('meta', {'name': 'csrf-token'})
        if not token_tag:
            raise Exception("Could not find CSRF token on the page.")
        csrf_token = token_tag['content']
        print(f"[+] Acquired fresh CSRF Token.")

        
        params = {
            'draw': '1', 'columns[0][data]': 'range', 'columns[1][data]': 'test_number',
            'columns[2][data]': 'term', 'columns[3][data]': 'P2P', 'columns[4][data]': 'A2P',
            'columns[5][data]': 'Limit_Range', 'columns[6][data]': 'limit_cli_a2p',
            'columns[7][data]': 'limit_did_a2p', 'columns[8][data]': 'limit_cli_did_a2p',
            'columns[9][data]': 'limit_cli_p2p', 'columns[10][data]': 'limit_did_p2p',
            'columns[11][data]': 'limit_cli_did_p2p', 'columns[12][data]': 'updated_at',
            'columns[13][data]': 'action', 'columns[13][searchable]': 'false', 'columns[13][orderable]': 'false',
            'order[0][column]': '1', 'order[0][dir]': 'asc', 'start': '0', 'length': '50',
            'search[value]': range_name, '_': int(time.time() * 1000),
        }
        search_headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': TEST_NUMBERS_PAGE_URL, 'X-CSRF-TOKEN': csrf_token,
            'X-Requested-With': 'XMLHttpRequest', 'User-Agent': session.headers['User-Agent']
        }
        search_response = session.get(TEST_NUMBERS_API_URL, params=params, headers=search_headers)
        search_response.raise_for_status()
        search_data = search_response.json()

        if not search_data.get('data'):
            print(f"[!] Search failed. No numbers found for range '{range_name}'. It might be unavailable.")
            return False

        
        first_result = search_data['data'][0]
        termination_id = first_result.get('id')
        number_to_add = first_result.get('test_number')

        if not termination_id or not number_to_add:
            print(f"[!] Could not extract 'id' or 'test_number' from search results for '{range_name}'.")
            return False
        print(f"[+] Found Target. ID: {termination_id}, Number: {number_to_add}")

        
        print(f"--- Sending 'Add' request for {number_to_add} ---")
        add_payload = {'_token': csrf_token, 'id': termination_id}
        add_headers = search_headers.copy()
        add_headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'

        add_response = session.post(ADD_NUMBER_API_URL, data=add_payload, headers=add_headers)
        add_response.raise_for_status()
        add_data = add_response.json()

        if "done" in add_data.get("message", "").lower():
            print(f"\n[SUCCESS] Server confirmed '{number_to_add}' from range '{range_name}' has been added.")
            return True
        else:
            error_message = add_data.get("message", "Unknown error from server.")
            print(f"[!] Add action FAILED: {error_message}")
            return False

    except Exception as e:
        print(f"[!!!] CRITICAL ERROR during add process: {e}")
        return False

def main():
    
    signal.signal(signal.SIGINT, graceful_shutdown)

    print("="*60)
    print("--- IsraelDev Number Adder ---")
    print("="*60)

    if "PASTE_YOUR_NEW_FRESH_TOKEN_HERE" in MAGIC_RECAPTCHA_TOKEN:
        print("\n[!!!] FATAL ERROR: You must update the 'MAGIC_RECAPTCHA_TOKEN' variable.")
        return

    try:
        with requests.Session() as session:
            session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})

            print("\n[*] Step 1: Authenticating...")
            response = session.get(LOGIN_URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            csrf_token_login = soup.find('input', {'name': '_token'})['value']
            
            login_payload = {
                '_token': csrf_token_login, 'email': EMAIL, 'password': PASSWORD,
                'g-recaptcha-response': MAGIC_RECAPTCHA_TOKEN,
            }
            login_response = session.post(LOGIN_URL, data=login_payload, headers={'Referer': LOGIN_URL})

            if "login" not in login_response.url and "Logout" in login_response.text:
                print("[SUCCESS] Authentication complete!")
                
                # --- Interactive Loop ---
                while True:
                    range_to_add = input("\nEnter the number range you want to add (or type 'exit' to quit): ").strip()
                    if range_to_add.lower() == 'exit':
                        break
                    if not range_to_add:
                        print("[!] Range name cannot be empty.")
                        continue
                    
                    add_number_range(session, range_to_add)

            else:
                print("\n[!!!] AUTHENTICATION FAILED. Check token/credentials.")

    except Exception as e:
        print(f"[!!!] A critical error occurred during startup: {e}")

    print("\n[*] Bot has finished.")

if __name__ == "__main__":
    main()
