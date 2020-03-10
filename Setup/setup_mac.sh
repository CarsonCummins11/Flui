/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
export PATH="/usr/local/opt/python/libexec/bin:$PATH"
brew install python
pip install -r requirements.txt
brew tap mongodb/brew
brew install mongodb-community@4.2
brew services start mongodb-community@4.2
python dbsetup.py
python3 -m flask run