# Random Location TwitterBot

![GitHub repo size](https://img.shields.io/github/repo-size/victormedel/twitterbot)
![GitHub contributors](https://img.shields.io/github/contributors/victormedel/twitterbot)
![GitHub stars](https://img.shields.io/github/stars/victormedel/twitterbot?style=social)

The Random Location TwitterBot parses all Twitter trending words, provides three random words and attempts to generate a three word geo location address via the [what3words API](https://what3words.com).

This is a simple converation starter application that will allow Twitter users to potentially reach a different audience.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* Python 3.8+
* [Twitter Developer](https://developer.twitter.com/) API keys and tokens
* [what3words](https://developer.what3words.com/) API key
* [Google Cloud](https://cloud.google.com/apis) API key for Google Map Static API

## Installing The Random Location TwitterBot

To install the Random Location TwitterBot *locally*, follow these steps:

1. Configure all API keys and tokens as environment system variables using variable names found in config.py

2. Clone project locally

3. Install required Python packages

```
C:\twitter-bot>pip install -r requirements.txt
```

## Using The Random Location TwitterBot

To use the Random Location TwitterBot, localy, follow these steps:

1. Configure location and wait time in random_loc.py (optional)

```python
WAIT_SECONDS = 1800
LOCATION = "United States"
```

2. From the project directory run random_loc.py

```
C:\twitter-bot\bot>python random_loc.py
```

3. Ctrl+C to stop the bot


## Built With

* [Tweepy](https://www.tweepy.org/)
* [what3words](https://developer.what3words.com/tutorial/python)
* [geocoder](https://github.com/DenisCarriere/geocoder)

## Contributing to TwitterBot

To contribute to TwitterBot, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## Contact

If you want to contact me you can reach me at [medel.victor@gmail.com](mailto:medel.victor@gmail.com).

## License

This project uses the following license: [MIT License](LICENSE).

## Future Work

* Adding further capability and instructions on how to deploy to Amazon AWS
* Autoreply and like functionality