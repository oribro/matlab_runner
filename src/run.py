from core import GUI
from subprocess import check_output


"""
This script serves as a utillity for running a matlab file
according to the user demand, served by an interactive GUI.
The GUI performs the following functionality:

Input: Folder found on the computer.

The program will query the user for a matching directory and file until found.

Output: Matlab file to run on success.
"""

# TODO: Set size of GUI window
g = GUI(100, 100)
g.start()
output_file = g.get_chosen_file()
g.end()

# TODO: Optimize the searching part. Using 'WHERE' takes much time, and
# there should be an easier way to do this.
# Also it could be nice to add to the GUI friendly messages that tell
# the user what is being executed by the program while he waits.
# search_matlab_command = r"WHERE /R C:\Program Files matlab.exe"
# search_matlab_command = r"WHERE /R D:\Matlab matlab.exe"
# matlab_command = check_output(
#     search_matlab_command,
#     shell=True
# ).decode().strip().split('\r\n')[0]

# This command should do the trick. Need to verify it on more machines.
matlab_command = "matlab.exe"

# Run the chosen matlab file from the shell using python.
run_command = (
    r'"{}" -nosplash -nodesktop -r "try, run('.format(matlab_command) +
    r"'{}'".format(output_file)+
    '), catch, end"'
)
check_output(run_command, shell=True)

