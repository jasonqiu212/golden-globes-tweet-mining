"""This file provides operations to merge related results and decide on final results."""

from queue import PriorityQueue

import editdistance


def merge_through_voting(preliminary_results):
    """
    Merge preliminarily extracted list of results into final results through voting.

    Args:
        preliminary_results: List of preliminarily extracted results.
    Returns:
        List of voted results.
    """
    votes = {}
    final_results = []
    for preliminary_result in preliminary_results:
        votes[preliminary_result] = votes.get(preliminary_result, 0) + 1
    for host, vote in votes.items():
        if vote > 7:
            final_results.append(host)
    return final_results


def merge_through_voting_highest_k_results(preliminary_results, k):
    """
    Merge preliminarily extracted list of results into list of k results with the highest votes.
    To prevent outliers, all voted results must have more than 1 vote.

    Args:
        preliminary_results: List of preliminarily extracted results.
    Returns:
        List of k results with the highest votes and more than 1 vote. List may have less than k
        elements if results do not have more than 1 vote.
    """
    votes = {}
    for preliminary_result in preliminary_results:
        votes[preliminary_result] = votes.get(preliminary_result, 0) + 1

    pq = PriorityQueue()
    most_voted = []
    for result, vote in votes.items():
        if vote <= 1:
            continue

        pq.put((-vote, result))
    for _ in range(k):
        if pq.qsize() == 0:
            break
        most_voted.append(pq.get()[1])
    return most_voted


def merge_awards(preliminary_awards):
    """
    Merge preliminarily extracted awards into final results using edit distance.

    Args:
        preliminary_awards: List of preliminarily extracted awards.
    Returns:
        List of merged awards.
    """
    final_awards = []
    for preliminary_award in preliminary_awards:
        if all(editdistance.eval(final_award, preliminary_award) >= 7 for final_award in final_awards):
            final_awards.append(preliminary_award)

    return final_awards


def merge_nominees(preliminary_nominees, final_winner):
    """
    Merge preliminarily extracted nominees into final results by removing winner from
    preliminary results and getting top 4 candidates.

    Args:
        preliminary_nominees: List of preliminarily extracted nominees.
        final_winner: String representing the final winner.
    Returns:
        List of merged awards.
    """
    while preliminary_nominees.count(final_winner) > 0:
        preliminary_nominees.remove(final_winner)
    return merge_through_voting_highest_k_results(preliminary_nominees, 4)


def merge_award_results(preliminary_award_results):
    final_award_results = {}
    for award_name in preliminary_award_results.keys():
        final_award_results[award_name] = {}

        merged_presenters_results = merge_through_voting_highest_k_results(
            preliminary_award_results[award_name]['presenters'], 2)
        final_award_results[award_name]['presenters'] = merged_presenters_results

        merged_winner_results = merge_through_voting_highest_k_results(
            preliminary_award_results[award_name]['winners'], 1)
        final_award_results[award_name]['winner'] = ''
        if merged_winner_results:
            final_award_results[award_name]['winner'] = merged_winner_results[0]

        final_award_results[award_name]['nominees'] = merge_nominees(
            preliminary_award_results[award_name]['nominees'], final_award_results[award_name]['winner'])

    return final_award_results


def merge(preliminary_results):
    final_results = {}
    final_results['hosts'] = merge_through_voting(preliminary_results['hosts'])
    print('5/9: Finished merging host results')

    final_results['awards'] = merge_awards(preliminary_results['awards'])
    print('6/9: Finished merging award results')

    final_results['award_results'] = merge_award_results(
        preliminary_results['award_results'])
    print('7/9: Finished merging presenters, winners, and nominees')

    return final_results
