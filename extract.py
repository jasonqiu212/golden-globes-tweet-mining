import json
import re
import time

import editdistance
from imdb import Cinemagoer, IMDbError
import spacy

from keywords import AWARD_CATEGORIES, AWARD_CATEGORIES_CELEBRITY_TYPE, AWARD_CATEGORIES_PICTURE_TYPE, AWARD_QUALIFIERS, extract_keywords_from_award_names, NOMINEE_KEYWORDS, PRESENTER_KEYWORDS_PLURAL, PRESENTER_KEYWORDS_SINGULAR, WINNER_KEYWORDS
from preprocess import is_english, preprocess

ia = Cinemagoer()
nlp = spacy.load("en_core_web_sm")

# def get_most_mentioned(tweets, persons, awards, window_size_seconds):
# to use this function:
# tweets is origin tweets(处理过冗余文字), persons和awards是我们已经通过extract 方法找到的所有的tweets中提及的可能的人物和奖项，他们之间的联系(who win what)还没被建立起来.
# extract persons 和 awards 需要在main中完成，我这会儿正在写.

#     sorted_tweets = sorted(tweets, key=lambda x: x["timestamp_ms"])

#     start_time = datetime.fromtimestamp(
#         sorted_tweets[0]["timestamp_ms"] / 1000)
#     end_time = start_time + timedelta(seconds=window_size_seconds)

#     results = []

#     for i in range(len(sorted_tweets)):
#         current_time = datetime.fromtimestamp(
#             sorted_tweets[i]["timestamp_ms"] / 1000)

#         # If the tweet we are parsing right not is not in the time window, we need to update the time window.
#         if current_time > end_time:
#             start_time = end_time
#             end_time = start_time + timedelta(seconds=window_size_seconds)

#         # 统计当前时间窗口内的人名和奖项提及频率
#         person_counter = Counter()
#         award_counter = Counter()
#         while i < len(sorted_tweets) and datetime.fromtimestamp(sorted_tweets[i]["timestamp_ms"] / 1000) <= end_time:
#             tweet_text = sorted_tweets[i]["text"]
#             for person in persons:
#                 if person in tweet_text:
#                     person_counter[person] += 1
#             for award in awards:
#                 if award in tweet_text:
#                     award_counter[award] += 1
#             i += 1

#         # 获取当前时间窗口内最常提及的人名和奖项
#         most_common_person = person_counter.most_common(1)
#         most_common_award = award_counter.most_common(1)

#         results.append({
#             "time_window": (start_time, end_time),
#             "most_common_person": most_common_person,
#             "most_common_award": most_common_award
#         })

#     return results


# def find_relevant_tweets(tweets, keywords):
#     # 过滤出包含关键词的推文, 关键词（win，won，got，etc,在main中定义keywords）
#     relevant_tweets = []
#     for tweet in tweets:
#         if any(keyword.lower() in tweet["text"].lower() for keyword in keywords):
#             relevant_tweets.append(tweet)
#             # list of tweets
#     return relevant_tweets

# def extract_person(tweet):
#     doc = nlp(tweet["text"])
#     entities = [(ent.text, ent.label_) for ent in doc.ents]
#     persons = [ent for ent in entities if ent[1] == 'PERSON']
#     return persons


# def extract_award(tweet):
#     doc = nlp(tweet["text"])
#     entities = [(ent.text, ent.label_) for ent in doc.ents]
#     awards = [ent for ent in entities if ent[1]
#               == 'WORK_OF_ART' or ent[1] == 'EVENT']
#     return awards


# def dextract_all(tweet):
#     persons = []
#     awards = []
#     for tweets in tweet:
#         persons.append(extract_person(tweets))
#         awards.append(extract_award(tweets))
#     return persons, awards


# def extract_nomination_info(sentence):
#     matcher = spacy.Matcher(nlp.vocab)

#     # 定义匹配模式
#     person_pattern = [{"ENT_TYPE": "PERSON"}]
#     award_pattern = [{"LOWER": "best"}, {"POS": "NOUN", "OP": "?"}]
#     nominate_pattern = [{"LEMMA": "nominate"}]
#     optional_words_pattern = [
#         {"POS": "VERB", "OP": "*"}, {"LOWER": "to", "OP": "?"}]

#     matcher.add("PERSON", [person_pattern])
#     matcher.add("AWARD", [award_pattern])
#     matcher.add("NOMINATE", [nominate_pattern])

#     doc = nlp(sentence)

#     matches = matcher(doc)
#     persons = [doc[start:end].text for match_id, start,
#                end in matches if nlp.vocab.strings[match_id] == "PERSON"]
#     awards = [doc[start:end].text for match_id, start,
#               end in matches if nlp.vocab.strings[match_id] == "AWARD"]

#     if any(token.lemma_ == "nominate" for token in doc):
#         return [(person, award) for person in persons for award in awards]
#     return []


def get_celebrity_search_result(query):
    search_result = []
    try:
        search_result = ia.search_person(query)
    except IMDbError as e:
        print(e)
    return search_result


def get_picture_search_result(query):
    search_result = []
    try:
        search_result = ia.search_movie(query)
    except IMDbError as e:
        print(e)
    return search_result


def get_best_ceremony_entity(candidates, type):
    """
    Extract closest matching ceremony entity from list of candidates.

    Args:
        candidates: List of candidates.
        type: 'celebrity' or 'picture'.
    Returns:
        String representing extracted ceremony entity. None, if ceremony entity
        cannot be identified.
    """
    candidate_search_results = []
    for candidate in candidates:
        if type == 'celebrity':
            search_result = get_celebrity_search_result(candidate)
            if search_result:
                candidate_search_results.append(
                    search_result[0].get('name').lower())
            else:
                candidate_search_results.append(None)
        elif type == 'picture':
            search_result = get_picture_search_result(candidate)
            if search_result:
                candidate_search_results.append(
                    search_result[0].get('title').lower())
            else:
                candidate_search_results.append(None)

    best_name, least_edit_distance = '', 999999
    for i in range(len(candidates)):
        if candidate_search_results[i] == None:
            continue
        edit_distance = editdistance.eval(
            candidates[i], candidate_search_results[i])
        if edit_distance < least_edit_distance:
            best_name = candidate_search_results[i]
            least_edit_distance = edit_distance

    if least_edit_distance > 4:
        return None

    return best_name


def find_ceremony_entity_from_left_side_words(left_side_words, type):
    """
    Extract ceremony entity from list of words going from right to left.

    Args:
        left_side_words: List of words to search from.
        type: 'celebrity' or 'picture'.
    Returns:
        String representing extracted ceremony entity. None, if ceremony entity
        cannot be identified.
    """
    if type != 'celebrity' and type != 'picture':
        return None

    candidates = []
    for i in range(2 if type == 'celebrity' else 1, 5 if type == 'celebrity' else 8):
        if i > len(left_side_words):
            break
        candidates.append(
            " ".join(left_side_words[len(left_side_words) - i:]))

    return get_best_ceremony_entity(candidates, type)


def find_ceremony_entity_from_right_side_words(right_side_words, type):
    """
    Extract ceremony entity from list of words going from left to right.

    Args:
        right_side_words: List of words to search from.
        type: 'celebrity' or 'picture'.
    Returns:
        String representing extracted ceremony entity. None, if ceremony entity
        cannot be identified.
    """
    if type != 'celebrity' and type != 'picture':
        return None

    candidates = []
    for i in range(2 if type == 'celebrity' else 1, 5 if type == 'celebrity' else 8):
        if i >= len(right_side_words):
            break
        candidates.append(
            " ".join(right_side_words[:i]))

    return get_best_ceremony_entity(candidates, type)


def extract_hosts(tweet):
    """
    Extracts potential hosts from tweet using the following strategies:
    1. Find phrases in the format of 'hosted by ' + PERSON_NAME + ' and ' + PERSON_NAME
    2. Find phrases in the format of 'hosted by ' + PERSON_NAME
    3. Find phrases in the format of 'hosts ' + PERSON_NAME + ' and ' + PERSON_NAME
    4. Find phrases in the format of 'host ' + PERSON_NAME

    Args:
        tweets: List of tweets to extract from.
    Returns:
        List of potential hosts.
    """
    hosts = []
    if re.search("hosted by [\w\s]+ and [\w\s]+", tweet):
        hosted_by_split = tweet.split('hosted by ')
        right_side_words = hosted_by_split[1].split()

        and_split = ' '.join(right_side_words).split(' and ')

        left_candidate = and_split[0]
        search_result = get_celebrity_search_result(left_candidate)

        if search_result:
            left_candidate_search_result = search_result[0].get(
                'name').lower()

            if editdistance.eval(left_candidate, left_candidate_search_result) < 10:
                hosts.append(left_candidate_search_result)

        right_host_words = and_split[1].split()
        right_host_name = find_ceremony_entity_from_right_side_words(
            right_host_words, 'celebrity')
        if right_host_name:
            hosts.append(right_host_name)
    elif 'hosted by ' in tweet:
        hosted_by_split = tweet.split('hosted by ')
        right_side_words = hosted_by_split[1].split()

        host_name = find_ceremony_entity_from_right_side_words(
            right_side_words, 'celebrity')
        if host_name:
            hosts.append(host_name)
    elif re.search("hosts [\w\s]+ and [\w\s]+", tweet):
        hosts_split = tweet.split('hosts ')
        right_side_words = hosts_split[1].split()

        and_split = ' '.join(right_side_words).split(' and ')

        left_candidate = and_split[0]
        search_result = get_celebrity_search_result(left_candidate)
        if search_result:
            left_candidate_search_result = search_result[0].get(
                'name').lower()

            if editdistance.eval(left_candidate, left_candidate_search_result) < 10:
                hosts.append(left_candidate_search_result)

        right_host_words = and_split[1].split()
        right_host_name = find_ceremony_entity_from_right_side_words(
            right_host_words, 'celebrity')
        if right_host_name:
            hosts.append(right_host_name)
    elif 'host ' in tweet:
        hosted_by_split = tweet.split('host ')
        right_side_words = hosted_by_split[1].split()

        host_name = find_ceremony_entity_from_right_side_words(
            right_side_words, 'celebrity')
        if host_name:
            hosts.append(host_name)
    return hosts


def extract_award(tweet):
    """
    Extracts potential award from tweets using the following strategies:
    1. Find phrases in the format of PERSON_NAME + ' award'
    2. Find phrases in the format of 'best ' + AWARD_CATEGORY + AWARD_QUALIFIER

    Args:
        tweets: List of tweets to extract from.
    Returns:
        String representing potential award.
    """
    if ' award' in tweet:
        award_split = tweet.split(' award')
        left_side_words = award_split[0].split()

        celebrity_award_name = find_ceremony_entity_from_left_side_words(
            left_side_words, 'celebrity')
        if celebrity_award_name:
            return celebrity_award_name + ' award'

    if 'best ' in tweet:
        best_split = tweet.split('best ')
        right_side_words = best_split[1].split()

        matched_category_index = -1
        for award_category in AWARD_CATEGORIES:
            if award_category in right_side_words:
                matched_category_index = right_side_words.index(
                    award_category)
                break

        if matched_category_index == -1:
            return None

        matched_qualifier_index = -1
        for i in range(len(right_side_words) - 1, matched_category_index - 1, -1):
            if right_side_words[i] in AWARD_QUALIFIERS:
                matched_qualifier_index = i
                break

        award_end_index = matched_qualifier_index
        if matched_qualifier_index == -1:
            award_end_index = matched_category_index

        return 'best ' + ' '.join(right_side_words[:award_end_index + 1])
    return None


def extract_winner(tweet, matched_award_keywords):
    """
    Extracts winner from tweet.

    Args:
        tweet: Tweet to extract from.
        matched_award_keywords: List of must-have award keywords that the given tweet matched with.
    Returns:
        String representing extracted winner from tweet. None, if no winner is found.
    """
    matching_keyword = find_first_matching_keyword(tweet, WINNER_KEYWORDS)
    if matching_keyword:
        keyword_split = tweet.split(' ' + matching_keyword + ' ')
        left_side_words = keyword_split[0].split()

        winner_name = ''
        if any(k in AWARD_CATEGORIES_CELEBRITY_TYPE for k in matched_award_keywords):
            winner_name = find_ceremony_entity_from_left_side_words(
                left_side_words, 'celebrity')
        elif any(k in AWARD_CATEGORIES_PICTURE_TYPE for k in matched_award_keywords):
            winner_name = find_ceremony_entity_from_left_side_words(
                left_side_words, 'picture')

        if winner_name != '':
            return winner_name

    return None


def find_closest_matching_ceremony_entity(tweet, type):
    """
    Extract closest matching ceremony entity from tweet.

    Args:
        tweet: Tweet to search from.
        type: 'celebrity' or 'picture'.
    Returns:
        String representing extracted ceremony entity. None, if ceremony entity
        cannot be identified.
    """
    if type != 'celebrity' and type != 'picture':
        return None

    words = tweet.split()
    candidates = []
    for i in range(len(words)):
        for j in range(2 if type == 'celebrity' else 1, 5 if type == 'celebrity' else 8):
            if i + j >= len(words):
                break

            candidates.append(' '.join(words[i:i + j]))

    return get_best_ceremony_entity(candidates, type)


def extract_nominee(tweet, matched_award_keywords):
    """
    Extracts nominee from tweet.

    Args:
        tweet: Tweet to extract from.
        matched_award_keywords: List of must-have award keywords that the given tweet matched with.
    Returns:
        String representing extracted nominee from tweet. None, if no nominee is found.
    """
    nominee = None
    if any(k in AWARD_CATEGORIES_CELEBRITY_TYPE for k in matched_award_keywords):
        nominee = find_closest_matching_ceremony_entity(tweet, 'celebrity')
    elif any(k in AWARD_CATEGORIES_PICTURE_TYPE for k in matched_award_keywords):
        nominee = find_closest_matching_ceremony_entity(tweet, 'picture')
    return nominee


def find_first_matching_keyword(tweet, keywords):
    """
    Returns first matching keyword from set of keywords in tweet.

    Args:
        tweet: Tweet to search from.
        keywords: Set of keywords to match.
    Returns:
        String representing first matching keyword in tweet. None, if no matches.
    """
    for keyword in keywords:
        if keyword in tweet:
            return keyword
    return None


def extract_presenters(tweet, award_names):
    """
    Extracts presenters from tweet.

    Args:
        tweet: Tweet to extract from.
        award_names: List of official award names.
    Returns:
        List of extracted presenters from tweet. Empty list, if no presenters are found.
    """
    matching_keyword = find_first_matching_keyword(
        tweet, PRESENTER_KEYWORDS_PLURAL)
    if matching_keyword:
        keyword_split = tweet.split(' ' + matching_keyword + ' ')
        left_side_words = keyword_split[0].split()
        if 'and' in left_side_words:
            presenters = []
            and_split = ' '.join(left_side_words).split(' and ')

            right_candidate = and_split[1]
            search_result = get_celebrity_search_result(right_candidate)
            if search_result:
                right_candidate_search_result = search_result[0].get(
                    'name').lower()

                if editdistance.eval(right_candidate, right_candidate_search_result) < 10:
                    presenters.append(right_candidate_search_result)

            left_presenter_words = and_split[0].split()
            left_presenter_name = find_ceremony_entity_from_left_side_words(
                left_presenter_words, 'celebrity')
            if left_presenter_name:
                presenters.append(left_presenter_name)
            return presenters

    matching_keyword = find_first_matching_keyword(
        tweet, PRESENTER_KEYWORDS_SINGULAR)
    if matching_keyword:
        keyword_split = tweet.split(' ' + matching_keyword + ' ')
        left_side_words = keyword_split[0].split()
        presenter_name = find_ceremony_entity_from_left_side_words(
            left_side_words, 'celebrity')
        if presenter_name and presenter_name + ' award' not in award_names:
            return [presenter_name]
    return []


def extract_using_award_names(tweet, award_names, award_results):
    """
    Extracts potential presenters, nominees, and winners from tweet based on official award names.
    Adds extracted result into award_results.

    Args:
        tweet: Tweets to extract from.
        award_names: List of official award names.
        award_results: Dictionary of award results to add to.
    """
    awards_keywords = extract_keywords_from_award_names(award_names)

    if ' award' not in tweet and 'best ' not in tweet:
        return

    # Find mentioned award in tweet in following priority levels:
    # 1. For an award, if all must_have keywords and all qualifiers are in tweet
    # 2. For an award, if all must_have keywords and any qualifier is in tweet
    # 3. For an award, if all must_have keywords are in tweet
    has_award_keywords = False
    mentioned_award = ''
    for award, keywords in awards_keywords.items():
        must_have = keywords['must_have']
        qualifiers = keywords['qualifiers']

        if all(mh in tweet for mh in must_have) and all(q in tweet for q in qualifiers):
            has_award_keywords = True
            mentioned_award = award
            break

    if not has_award_keywords:
        for award, keywords in awards_keywords.items():
            must_have = keywords['must_have']
            qualifiers = keywords['qualifiers']

            if all(mh in tweet for mh in must_have) and any(q in tweet for q in qualifiers):
                has_award_keywords = True
                mentioned_award = award
                break

    if not has_award_keywords:
        for award, keywords in awards_keywords.items():
            must_have = keywords['must_have']
            qualifiers = keywords['qualifiers']

            if all(mh in tweet for mh in must_have):
                has_award_keywords = True
                mentioned_award = award
                break

    if not has_award_keywords:
        return

    candidate_winner = extract_winner(
        tweet, awards_keywords[mentioned_award]['must_have'])
    if candidate_winner:
        award_results[mentioned_award]['winners'].append(candidate_winner)
        return

    candidate_presenters = extract_presenters(tweet, award_names)
    if len(candidate_presenters) != 0:
        award_results[mentioned_award]['presenters'] += candidate_presenters
        return

    candidate_nominee = extract_nominee(
        tweet, awards_keywords[mentioned_award]['must_have'])
    if candidate_nominee:
        award_results[mentioned_award]['nominees'].append(
            candidate_nominee)
        return


def extract_best_dressed(tweet):
    """
    Extracts best dressed celebrity from tweet.

    Args:
        tweet: Tweet to extract from.
    Returns:
        String representing extracted best dressed celebrity from tweet. None, if no best dressed celebrity is found.
    """
    if 'best dressed' in tweet:
        return find_closest_matching_ceremony_entity(
            tweet, 'celebrity')
    return None


def extract(file_name, award_names, time_limit):
    """
    Extracts hosts, award names, presenters, nominees, and
    winners from tweets.

    Args:
        file_name: File name of data file containing tweets.
        award_names: List of official award names.
        time_limit: Time limit for extracting tweets in seconds.
    Returns:
        Dictionary of preliminary results extracted from tweets.
    """
    hosts = []
    awards = []
    award_results = {}
    best_dressed = []
    for award_name in award_names:
        award_results[award_name] = {
            'presenters': [], 'nominees': [], 'winners': []}

    start_time = time.time()
    with open(file_name) as f:
        tweets = json.load(f)

        count = 0
        for tweet in tweets:
            if time.time() - start_time >= time_limit:
                print('{} seconds time limit reached for extraction'.format(time_limit))
                break

            if count % 50 == 0:
                print('Parsed {} tweets'.format(count))
            count += 1

            t = preprocess(tweet['text'])
            if not is_english(t):
                continue

            if len(hosts) < 30:
                extracted_hosts = extract_hosts(t)
                if len(extracted_hosts) > 0:
                    hosts += extract_hosts(t)
                    continue

            extracted_best_dressed = extract_best_dressed(t)
            if extracted_best_dressed:
                best_dressed.append(extracted_best_dressed)
                continue

            extracted_award = extract_award(t)
            if extracted_award:
                awards.append(extracted_award)

            extract_using_award_names(t, award_names, award_results)

    preliminary_results = {'hosts': hosts,
                           'awards': awards, 'award_results': award_results, 'best_dressed': best_dressed}
    print(preliminary_results)
    print('1/6: Finished extracting information from tweets')
    return preliminary_results
