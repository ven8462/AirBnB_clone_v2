#!/usr/bin/python3
# Import necessary modules
from fabric.api import env, run, put
from os import path

# Set the hosts for the Fabric script
env.hosts = ['100.25.133.244', '100.26.132.163']
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


# Define the do_deploy function
def do_deploy(archive_path):
    """
    Upload the archive to the /tmp/ directory of the web server
    Uncompress the archive to the folder
    /data/web_static/releases/<archive filename without extension>
    on the web server
    Delete the archive from the web server
    Delete the symbolic link /data/web_static/current from the web server
    Create a new the symbolic link /data/web_static/current on the web server,
    linked to the new version of the code
    /data/web_static/releases/<archive filename without extension>
    True if all operations have been done correctly, otherwise returns False
    """
    # Check if the archive file exists
    if not path.exists(archive_path):
        return False

    # Extract the base name and directory name from the archive path
    file_name = path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_name)
    success = False
    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/{}".format(file_name))

        # Create the necessary directories on the web server
        run("mkdir -p {}".format(folder_path))

        # Uncompress the archive to the /data/web_static/releases/<archive file
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))

        # Delete the archive from the /tmp/ directory on the web server
        run("rm -rf /tmp/{}".format(file_name))

        # Move the files from the web_static directory to the
        #  /data/web_static/releases
        run("mv {}web_static/* {}".format(folder_path, folder_path))

        # Delete the web_static directory from the /data/web_static/releases/
        run("rm -rf {}web_static".format(folder_path))

        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current on the web server
        run("ln -s {} /data/web_static/current".format(folder_path))

        # Print a success message
        print('New version deployed!')

        # Set the success flag to True
        success = True
    except Exception:
        # Set the success flag to False if an error occurs
        success = False
    # Return the success flag
    return success
