# Wordle Discord Bot 

## Motivation
For about a year and a half, myself and two other friends have had a group chat where we send in our daily wordle results. I originally started this project as a script that would look through the group chat,
detect a wordle-type picture, and determine the score. This way, we could get a good estimate of our overall statistics (ex: which one of us had the lowest average attempts to solve a wordle). Eventually, I expanded upon the
code and tied it to a discord bot, which theoretically would update a database everytime it would detect a wordle screenshot.

## About The Files
 - 'bot.py' : Tells the discord bot what to do on certain commands
 - 'data-reader.py' : A specific reader that takes in a discord attachment log and converts it to a .txt of the discord link to each attachment
 - 'detect-score.py' : The magic file that takes in a url, determines if it is a wordle game, then calculates the score.
 - 'detect-text.py' : Another magic file that takes in a url, determines if it is a wordle game, then detects the user guesses (NOT IMPLEMENTED YET)
 - 'main.py' : File to initialize the discord bot
 - 'mass_data_analysis.py' : Controller that takes in a .txt file of urls, runs 'detect-score,' then tallies the statistics into a results.txt file.

## Future
I am looking to expand the discord bot features so that it can determine the user guesses. At the moment, score is determined based on colors rather than the text, which isn't the greatest in terms of accuracy. Also, I think
it would be interesting to develop this feature from a statistic lens, as it would be nice to see a given user's most frequently guessed word and calculate it with other statistics. Also, currently the discord bot is not online as 
I have not set up a server that will keep the bot initialized. It will probably not be online until the set features I want implemented are completed.
