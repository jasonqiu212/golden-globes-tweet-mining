"""This file provides operations to merge related results and decide on final results."""

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
        if vote > 5:
            final_results.append(host)
    return final_results


def merge_through_voting_most(preliminary_results):
    """
    Merge preliminarily extracted list of results into a result with highest vote.

    Args:
        preliminary_results: List of preliminarily extracted results.
    Returns:
        String representing result with highest vote.
    """
    votes = {}
    for preliminary_result in preliminary_results:
        votes[preliminary_result] = votes.get(preliminary_result, 0) + 1
    most_voted, most_votes = '', -1
    for host, vote in votes.items():
        if vote > most_votes:
            most_votes = vote
            most_voted = host
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
    final_nominees = []
    return final_nominees


def merge_award_results(preliminary_award_results):
    final_award_results = {}
    for award_name in preliminary_award_results.key():
        final_award_results[award_name] = {}
        final_award_results[award_name]['presenters'] = merge_through_voting(
            preliminary_award_results[award_name]['presenters'])
        final_award_results[award_name]['winner'] = merge_through_voting_most(
            preliminary_award_results[award_name]['winners'])
        final_award_results[award_name]['nominees'] = merge_nominees(
            preliminary_award_results[award_name]['nominees'], final_award_results[award_name]['winner'])
    return final_award_results


def merge(preliminary_results):
    final_results = {}
    final_results['hosts'] = merge_through_voting(preliminary_results['hosts'])
    final_results['awards'] = merge_awards(preliminary_results['awards'])
    final_results['award_results'] = merge_award_results(
        preliminary_results['award_results'])
    return final_results
