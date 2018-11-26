This script serves as a utillity for running a matlab file
according to the user demand, served by an interactive GUI.
The GUI performs the following functionality:

Input: Folder found on the computer.

The program will query the user for a matching directory and file until found.

Output: Run the matlab file in Matlab.

##### Requirements #####

The program is currently designed to run on Windows 10.
The source was compiled by 'PyInstaller' into an executable 
'matlab_runner.exe' which is found under 'run' folder.

This makes the requirements for running the program very simple:
You only need to have a Matlab installation on your system. 

However if you'd like to run the program from source (the 'src' folder),
You should have Python 3.6 installed along with 'tkinter' library for the GUI.
