Recommended setup based on Windows & VS code:

If you haven't already, download and install VS code (https://code.visualstudio.com/download)

Set up python interpreter and local virtual environment (venv). Option 1:

Open VS code. In the bottom bar, on the right hand side, click on the interpreter option. This should direct you to download a verion of Python from the Microsoft store, do this if you haven't already. Otherwise choose a verion of Python from the available list. Option 2:
Alternatively navigate to thew View tab in teh tool bar and select Command pallette (CTRL+shift+c will also open this), search for Python: create environment...
Choose venv
Choose the recommended Python version (not this may not be the most recent version)
When the option to tick the box for install dependencies in .txt or similar, choose this option but note it may not work. then press ok
If dependencies have not been install thus far, navigate to the terminal and type 'pip install -r requirements.txt'. If you are in an exterior folder you might need to rewrite as e.g. 'pip install -r RamanProcessSpectras\requirements.txt'

If there are errors and not all packages were install in this step you may have to install some packages manually this is done in the terminal using 'pip install <package_name>' e.g. 'pip install pandas'
