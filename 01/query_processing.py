""" Module containing query processing functions. """
import preprocessing
from collections import defaultdict


def process_query(index, text):
    conj_groups, not_group = _parse_query(text)

    # represent each group as a term: tf vector
    for group_idx, group in enumerate(conj_groups):
        group_vec = {}
        for t in group:
            try:
                group_vec[t] += 1
            except KeyError:
                group_vec[t] = 1
        conj_groups[group_idx] = group_vec

    # compute the scores for each conjunctive group
    group_scores = []
    for group_vec in conj_groups:
        # score the docs that contain all terms in the conjunctive group
        partial_scores = _compute_scores(index, group_vec)
        if len(partial_scores) > 0:
            group_scores.append(partial_scores)

    # compute the overall scores ("merging" the group scores)
    overall_scores = _compute_overall_scores(group_scores)

    # remove from the result docs containing terms in the not-group
    result = _remove_docs_with_not_terms(index, overall_scores, not_group)

    return result


def _parse_query(text):
    """Parses the query, partitioning terms into conjunctive groups and a not-group.

    A query has the form "a b ... OR c d ... OR ... -e -f ..."
    (a, b, ...), (c, d, ...) are conjunctive groups (i.e. terms in and)
    (-e, -f, ...) is the not-group (i.e. terms we don't want in the result)
    """
    tokens = preprocessing.preprocess(text.decode())  # need the query to be unicode
    conj_groups = []
    not_group = []
    group_idx = 0
    for t in tokens:
        if t == '||':
            group_idx += 1
        elif len(t) > 1 and t[0] == '-':
            not_group.append(t[1:])
        else:
            try:
                conj_groups[group_idx].append(t)
            except IndexError:  # the conj-group doesn't exist yet
                conj_groups.append([t])
    return conj_groups, not_group


def _compute_scores(index, query_vec):
    # Score the docs that contain all terms of the query.
    # To do the scoring in 1 pass, iteratively apply the "merging intersect algorithm" (IIR ch.1 pag.11)
    # keeping a running intersection score.
    # Notes:
    # intersection is computed iteratively: i.e. A ^ B ^ C is computed as (A ^ B) ^ C;
    # the running intersection score is a vector identical to a posting list that keeps a running score
    # for each doc in the partial intersection thus far (instead of the term weight of a simple posting).
    query_terms = query_vec.keys()  # need to fix the "ordering" of the terms in the query

    # test query terms against index
    terms_to_del = []
    for i, term in enumerate(query_terms):
        try:
            index[term]
        except KeyError:
            terms_to_del.append(i)

    # remove non-existing terms from query
    for i in terms_to_del:
        query_terms.pop(i)

    running_intersection_scores = []

    if len(query_terms) > 0:
        # initialize the running intersection score using the first term posting list
        first_tf = query_vec[query_terms[0]]

        running_intersection_scores = [[doc_id, first_tf * qif] for (doc_id, qif) in index[query_terms[0]]]

        for term in query_terms[1:]:
            query_term_tf = query_vec[term]
            p_list = index[term]
            r_idx, p_idx = 0, 0  # TypeError if only one zero
            new_running_intersection_scores = []
            while r_idx < len(running_intersection_scores) and p_idx < len(p_list):
                r_doc_id, r_score = running_intersection_scores[r_idx]
                p_doc_id, p_qif = p_list[p_idx]
                if r_doc_id == p_doc_id:  # term present in (running) intersection
                    # add the doc contribution for this term to the running score
                    new_running_intersection_scores.append([r_doc_id, r_score + query_term_tf * p_qif])
                    r_idx += 1
                    p_idx += 1
                elif r_doc_id < p_doc_id:
                    r_idx += 1
                else:
                    p_idx += 1
            running_intersection_scores = new_running_intersection_scores

    return running_intersection_scores


def _compute_overall_scores(group_scores):
    # merge doc scores, selecting the max score should the doc be present in more groups
    # "merging union algorithm"
    running_merger = group_scores[0]
    for scores in group_scores[1:]:
        r_idx, s_idx = 0, 0  # TypeError if only one zero
        new_running_merger = []
        while r_idx < len(running_merger) and s_idx < len(scores):
            r_doc_id, r_score = running_merger[r_idx]
            s_doc_id, s_score = scores[s_idx]
            if r_doc_id == s_doc_id:
                new_running_merger.append([r_doc_id, max(r_score, s_score)])
                r_idx += 1
                s_idx += 1
            elif r_doc_id < s_doc_id:
                new_running_merger.append([r_doc_id, r_score])
                r_idx += 1
            else:
                new_running_merger.append([s_doc_id, s_score])
                s_idx += 1
        running_merger = new_running_merger
    return running_merger


def _remove_docs_with_not_terms(index, scores, not_terms):
    # prune from scores the docs containing terms in the not_terms list
    # "merging subtraction algorithm"
    running_pruner = scores
    for term in not_terms:
        p_list = index[term]
        r_idx, p_idx = 0, 0  # TypeError if only one zero
        new_running_pruner = []
        while r_idx < len(running_pruner) and p_idx < len(p_list):
            r_doc_id, r_score = running_pruner[r_idx]
            p_doc_id = p_list[p_idx][0]
            if r_doc_id == p_doc_id:
                # forget the doc
                r_idx += 1
                p_idx += 1
            elif r_doc_id < p_doc_id:
                new_running_pruner.append([r_doc_id, r_score])
                r_idx += 1
            else:
                p_idx += 1
        running_pruner = new_running_pruner
    return running_pruner
