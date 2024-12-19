Prerequisites

Python 3.13 or higher
A Telegram account
A Telegram Bot Token (obtained from @BotFather)

Installation

Clone the repository:

bashCopygit clone git@github.com:YOUR_USERNAME/crypto-price-bot.git
cd crypto-price-bot

Create and activate virtual environment:

bashCopypython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

bashCopypip install -r requirements.txt

Copy .env.example to .env and add your Telegram Bot Token:

bashCopycp .env.example .env
# Edit .env file with your token
Usage

Start the bot:

bashCopypython src/bot.py

In Telegram, send these commands to your bot:


/start - Initialize the bot
/startupdate - Begin receiving hourly updates
/stopupdate - Stop receiving updates

Development

Create a new branch for each feature
Write tests for new functionality
Update documentation as needed

License
MIT License
Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.