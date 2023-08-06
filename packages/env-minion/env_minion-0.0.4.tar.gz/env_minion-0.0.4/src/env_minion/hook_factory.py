import os
import subprocess
import shutil
import pkg_resources;

hook_templates = {
    "pre-push": "./pre-push.txt"
}

def create_hook(hook_type):
    dest_dirpath = os.path.join(os.getcwd(), ".git/hooks")
    if not os.path.exists(dest_dirpath):
        print("Command should be run in the root directory of the git repository")
        return

    source_file = pkg_resources.resource_filename(__name__, hook_templates[hook_type])
    destination_file = os.path.join(dest_dirpath, hook_type)
    
    try:
        with open(source_file, 'r') as source:
            try:
                with open(destination_file, 'w') as destination:
                    shutil.copyfileobj(source, destination)
                    command = f"chmod +x {destination_file}"
                    subprocess.run(command, shell=True, check=True)

                    print("Successfully made hook file an executable")
                    print(f"Hook file '{destination_file}' successfully populated.")
            except FileNotFoundError:
                print("Error: destination file not found.")
            except Exception as e:
                print(f"An error occurred: {e}")

    except FileNotFoundError:
        print("Error: Source file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def create_all_hooks():
    for hook_type in hook_templates:
        create_hook(hook_type)

create_all_hooks()
