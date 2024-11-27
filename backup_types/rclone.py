import os
import subprocess

class RcloneBackup():
    def __init__(self):
        pass

    def backup(self, source, destination):
        rclone_command = f"rclone copy '{source}' '{destination}' --progress"
        os.system(rclone_command)

    def current_content(self, remote):
        """ Get the listing of a remote mount using rclone. """
        result = subprocess.run(['rclone', 'lsf', remote], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            files = result.stdout.splitlines()
            return [file[:-1] if file.endswith('/') else file for file in files]
        else:
            return None