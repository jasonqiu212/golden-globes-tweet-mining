from load_json import load_json
from preprocess import preprocess

import spacy
nlp = spacy.load("en_core_web_sm")


def find_relevant_tweets(tweets, keywords):
    # 过滤出包含关键词的推文, 关键词（win，won，got，etc,在main中定义keywords）
    relevant_tweets = []
    for tweet in tweets:
        if any(keyword.lower() in tweet["text"].lower() for keyword in keywords):
            relevant_tweets.append(tweet)
    return relevant_tweets
# keywords = ["award", "winner", "won", "receives", "recipient", "nominee", "nominated", "prize", "congratulations", "honored"]


def extract_award_info(tweet):
    # 使用spaCy进行实体识别和依存关系解析，这个是我google出来的方法，不知道是否允许使用，也是jmy之前提到的快速查询出句子中有用的entities的方法。
    doc = nlp(tweet["text"])
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    # 查找可能的获奖者和奖项
    persons = [ent for ent in entities if ent[1] == 'PERSON']
    awards = [ent for ent in entities if ent[1]
              == 'WORK_OF_ART' or ent[1] == 'EVENT']

    # 这里可以添加更多的逻辑来验证和精炼获奖者和奖项信息

    return persons, awards


def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    return hosts


def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    return awards


def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    return nominees


def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    return winners


def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    return presenters


def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    print("Pre-ceremony processing complete.")
    return


def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    tweets = load_json(2013)
    print(preprocess(tweets))

    # 新添加的关键词查找法
    keywords = ["award", "winner", "won", "receives", "recipient",
                "nominee", "nominated", "prize", "congratulations", "honored", "got"]
    relevant_tweets = find_relevant_tweets(tweets, keywords)

    for tweet in relevant_tweets:
        persons, awards = extract_award_info(tweet)
        print(f"Tweet: {tweet['text']}")
        print(f"Possible winners: {persons}")
        print(f"Possible awards: {awards}")
    return


if __name__ == '__main__':
    main()
