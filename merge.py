"""This file provides operations to merge related results and decide on final results."""

import editdistance


def merge_hosts(preliminary_hosts):
    """
    Merge preliminarily extracted hosts into final results.

    Args:
        preliminary_hosts: List of preliminarily extracted hosts.
    Returns:
        List of merged hosts.
    """
    host_votes = {}
    final_hosts = []
    for preliminary_host in preliminary_hosts:
        host_votes[preliminary_host] = host_votes.get(preliminary_host, 0) + 1
    for host, vote in host_votes.items():
        if vote > 5:
            final_hosts.append(host)
    return final_hosts


def merge_awards(preliminary_awards):
    """
    Merge preliminarily extracted awards into final results.

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


def merge(preliminary_results):
    final_results = {}
    final_results['hosts'] = merge_hosts(preliminary_results['hosts'])
    final_results['awards'] = merge_awards(preliminary_results['awards'])

    return final_results
