from collections import Counter
from datetime import datetime, timedelta
import spacy

nlp = spacy.load("en_core_web_sm")

# to use this function:
# tweets is origin tweets(处理过冗余文字), persons和awards是我们已经通过extract 方法找到的所有的tweets中提及的可能的人物和奖项，他们之间的联系(who win what)还没被建立起来.
# extract persons 和 awards 需要在main中完成，我这会儿正在写.


def get_most_mentioned(tweets, persons, awards, window_size_seconds):

    sorted_tweets = sorted(tweets, key=lambda x: x["timestamp_ms"])

    start_time = datetime.fromtimestamp(
        sorted_tweets[0]["timestamp_ms"] / 1000)
    end_time = start_time + timedelta(seconds=window_size_seconds)

    results = []

    for i in range(len(sorted_tweets)):
        current_time = datetime.fromtimestamp(
            sorted_tweets[i]["timestamp_ms"] / 1000)

        # If the tweet we are parsing right not is not in the time window, we need to update the time window.
        if current_time > end_time:
            start_time = end_time
            end_time = start_time + timedelta(seconds=window_size_seconds)

        # 统计当前时间窗口内的人名和奖项提及频率
        person_counter = Counter()
        award_counter = Counter()
        while i < len(sorted_tweets) and datetime.fromtimestamp(sorted_tweets[i]["timestamp_ms"] / 1000) <= end_time:
            tweet_text = sorted_tweets[i]["text"]
            for person in persons:
                if person in tweet_text:
                    person_counter[person] += 1
            for award in awards:
                if award in tweet_text:
                    award_counter[award] += 1
            i += 1

        # 获取当前时间窗口内最常提及的人名和奖项
        most_common_person = person_counter.most_common(1)
        most_common_award = award_counter.most_common(1)

        results.append({
            "time_window": (start_time, end_time),
            "most_common_person": most_common_person,
            "most_common_award": most_common_award
        })

    return results


def find_relevant_tweets(tweets, keywords):
    # 过滤出包含关键词的推文, 关键词（win，won，got，etc,在main中定义keywords）
    relevant_tweets = []
    for tweet in tweets:
        if any(keyword.lower() in tweet["text"].lower() for keyword in keywords):
            relevant_tweets.append(tweet)
            # list of tweets
    return relevant_tweets


def extract_hosts(tweets):
    """
    Extracts potential hosts from tweets.

    Args:
        tweets: List of tweets to extract from.
    Returns:
        List of potential hosts.
    """
    return []


def extract_awards(tweets):
    """
    Extracts potential awards from tweets.

    Args:
        tweets: List of tweets to extract from.
    Returns:
        List of potential awards.
    """
    awards = []
    # if phrase contains 'best' + AWARD_CATEGORIES + AWARD_QUALIFIERS, add into result
    # if phrase contains PERSON_NAME + 'award', add into result
    return awards


def extract_using_award_names(tweets, award_names):
    """
    Extracts potential presenters, nominees, and winners from tweets based on official award names.

    Args:
        tweets: List of tweets to extract from.
        award_names: List of official award names.
    Returns:
        Dicionary of official award names mapped to potential presenters, nominees, and winners.
    """
    return {}


def extract_person(tweet):
    doc = nlp(tweet["text"])
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    persons = [ent for ent in entities if ent[1] == 'PERSON']
    return persons


def extract_award(tweet):
    doc = nlp(tweet["text"])
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    awards = [ent for ent in entities if ent[1]
              == 'WORK_OF_ART' or ent[1] == 'EVENT']
    return awards


def dextract_all(tweet):
    persons = []
    awards = []
    for tweets in tweet:
        persons.append(extract_person(tweets))
        awards.append(extract_award(tweets))
    return persons, awards


def extract_nomination_info(sentence):
    matcher = spacy.Matcher(nlp.vocab)

    # 定义匹配模式
    person_pattern = [{"ENT_TYPE": "PERSON"}]
    award_pattern = [{"LOWER": "best"}, {"POS": "NOUN", "OP": "?"}]
    nominate_pattern = [{"LEMMA": "nominate"}]
    optional_words_pattern = [
        {"POS": "VERB", "OP": "*"}, {"LOWER": "to", "OP": "?"}]

    matcher.add("PERSON", [person_pattern])
    matcher.add("AWARD", [award_pattern])
    matcher.add("NOMINATE", [nominate_pattern])

    doc = nlp(sentence)

    matches = matcher(doc)
    persons = [doc[start:end].text for match_id, start,
               end in matches if nlp.vocab.strings[match_id] == "PERSON"]
    awards = [doc[start:end].text for match_id, start,
              end in matches if nlp.vocab.strings[match_id] == "AWARD"]

    if any(token.lemma_ == "nominate" for token in doc):
        return [(person, award) for person in persons for award in awards]
    return []


def extract(tweets, award_names):
    """
    Extracts hosts, award names, presenters, nominees, and
    winners from tweets.

    Args:
        tweets: List of tweets to extract from.
        award_names: List of official award names.
    Returns:
        Dictionary of preliminary results extracted from tweets.
    """
    preliminary_results = {}
    preliminary_results['hosts'] = extract_hosts(tweets)
    preliminary_results['awards'] = extract_awards(tweets)
    preliminary_results['award_results'] = extract_using_award_names(
        tweets, award_names)
    return preliminary_results
