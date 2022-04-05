# CAP4630_Project3
Authors: Hailey Francis, Jacob McGee, Edward Hage

# Requirements and Relevent Information
- On startup, the files "attributes.txt", "constraints.txt", "penalty.txt", "possible.txt" and "qualitative.txt" must be in the same directory as the source code.
- We are expecting "attributes.txt", "constraints.txt", "penalty.txt", "possible.txt" and "qualitative.txt" to be formatted correctly with respect to one another with all "Update with File Info" buttons: there is no error-checking implementing for validating if the file is useable. See Documentation for proper formatting.
- The Optimize and Omni-Optimize buttons may take a while to calculate. A pop-up window will appear with that warning, but it needs to be closed for the computation to actually begin.
- This program does not support the deletion of individual attributes, constraints, and preferences. If you would like to restart, click the "Reset" button to clear the data in all lists as well as the associated files.

# Build Instructions
- Make sure main.py, inputs.py, preferenceLogic.py, and all text files are in the same directory. For Windows users, this includes the included clingo.exe executable.
- Run "python main.py" in command line to open the User Interface.