# CS 337: Tweet Mining & The Golden Globes

Team members:

- Jason Qiu
- Jiayi Xu
- Mingyu Jin

## Overview

This project mines and extracts information from tweets about motion picture award ceremonies.

The sample dataset given in this repository are tweets from the [70th Golden Globe Awards](https://www.goldenglobes.com/winners-nominees/2013) in 2013.

The extracted information includes:

- Host(s) for the ceremony
- Award names
- Award presenters, given official award names
- Award nominees, given official award names
- Award winners, given official award names

We also extracted the following additional information:

- #BestDressed celebrity through a popular vote on the number of mentions

## Getting Started

1. Clone this repository.

```
$ git clone git@github.com:jasonqiu212/golden-globes-tweet-mining.git
$ cd golden-globes-tweet-mining
```

2. Install the required Python packages from `requirements.txt`.

```
$ python3 install -r requirements.txt
```

3. Download the `spacy` package `en_core_web_sm`.

```
$ python3 -m spacy download en_core_web_sm
```

4. If you need to change the file names containing the tweets and answers, change the corresponding constants under the `main` function in `gg_api.py`.

```
YEAR = 2013
TWEETS_FILE_NAME = 'gg{}.json'.format(YEAR)
ANSWER_FILE_NAME = 'gg{}answers.json'.format(YEAR)
```

> If you wish to run the extraction on a smaller set of tweets, we created a small representative dataset called `gg2013-subset.json`. To use this smaller dataset, replace `TWEETS_FILE_NAME` with `'gg2013-subset.json'`.

5. Extracting information from tweets takes a long time. Thus, we included a time limit for running the extraction. If you wish change the time limit for extracting information, change the corresponding constant under the `main` function in `gg_api.py`. The current time limit is 15 minutes, or 900 seconds.

```
TIME_LIMIT = 900
```

6. Extract the information from the tweets.

```
$ python3 gg_api.py
```

7. A file called `gg{YEAR}results.json` containing the results in a JSON format will be generated in the root directory. A file called `gg{YEAR}results_humanreadable.txt` containing the results in a human readable format will also be generated.

Congratulations! You have successfully mined and extracted information from tweets about award ceremonies.

## Acknowledgements

- Python libraries used: [spaCy](https://spacy.io/), [ftfy](https://ftfy.readthedocs.io/en/latest/#), [langdetect](https://pypi.org/project/langdetect/), [unidecode](https://pypi.org/project/Unidecode/), [editdistance](https://pypi.org/project/editdistance/), [cinemagoer](https://cinemagoer.github.io/), [nltk](https://www.nltk.org/)
