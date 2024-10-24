This is a Discord bot implementing tabletop rules inspired by Disco Elysium

# Installation

Make sure [Python 3](https://www.python.org/downloads/) and [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) is installed

Windows: Open PowerShell
macOS/Linux: Open a Terminal

Clone the repository
`git clone https://github.com/mrredcon/ballroom.git`
cd into it
`cd ballroom`

Setup a virtualenv
Windows: `py -3 -m virtualenv venv`
macOS/Linux: `python3 -m virtualenv venv`

Activate the virtualenv
Windows: `.\venv\Scripts\activate.ps1`
macOS/Linux: `source venv/bin/activate`

Install dependencies
All Platforms: `pip install -r requirements.txt`

# Setup
Create a bot account through this link: https://discord.com/developers/applications
Copy the token

Windows: `BALLROOM_TOKEN="token_goes_here" py ballroom.py`
macOS/Linux: `BALLROOM_TOKEN="token_goes_here" ./ballroom.py`