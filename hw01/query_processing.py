""" Module containing query processing functions. """
import preprocessing

# Be careful that keywords are words s.t. stemming leaves them unchanged
VEGETARIAN_KEYWORD = 'vegetarian'
VEGAN_KEYWORD = 'vegan'
LACTOSE_INT_KEYWORD = 'lactose-int'

VEGETARIAN_NOT_GROUP = ['meat', 'steak', 'beef', 'pork', 'chicken', 'ragu', 'fillet', 'scallops', 'prosciutto', 'fish',
                        'tuna', 'mussels', 'clams', 'lobster', 'squid', 'sardine', 'prawns', 'bacon', 'ham']
VEGAN_NOT_GROUP = ['cheese', 'milk', 'egg', 'butter', 'parmesan']  # list only terms that are not in VEGETARIAN
LACTOSE_INT_NOT_GROUP = ['cheese', 'milk', 'butter', 'parmesan', 'cream']


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
        group_scores.append(_compute_scores(index, group_vec))

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
    tokens = preprocessing.preprocess(text.decode(), stemming=False)  # need the query to be unicode
    conj_groups = [[]]
    not_group = []
    group_idx = 0
    for t in tokens:
        if t == '||':
            group_idx += 1
            conj_groups.append([])
        elif len(t) > 1 and t[0] == '-':
            not_group.append(t[1:])
        elif len(t) > 1 and t[0] == '*':
            not_group.extend(get_special_not_group(t[1:]))
        else:
            conj_groups[group_idx].append(t)
    conj_groups = [preprocessing.stem(group) for group in conj_groups]
    not_group = preprocessing.stem(not_group)
    return conj_groups, not_group


def get_special_not_group(keyword):
    result = []
    if keyword == VEGETARIAN_KEYWORD:
        result = VEGETARIAN_NOT_GROUP
    elif keyword == VEGAN_KEYWORD:
        result = VEGETARIAN_NOT_GROUP + VEGAN_NOT_GROUP
    elif keyword == LACTOSE_INT_KEYWORD:
        result = LACTOSE_INT_NOT_GROUP
    return result


def _compute_scores(index, query_vec):
    # Score the docs that contain all terms of the query.
    # To do the scoring in 1 pass, iteratively apply the "merging intersect algorithm" (IIR ch.1 pag.11)
    # keeping a running intersection score.
    # Notes:
    # intersection is computed iteratively: i.e. A ^ B ^ C is computed as (A ^ B) ^ C;
    # the running intersection score is a vector identical to a posting list that keeps a running score
    # for each doc in the partial intersection thus far (instead of the term weight of a simple posting).

    # get a list of the query terms actually present in the index
    query_terms = query_vec.keys()

    if len(query_terms) <= 0 or [term for term in query_terms if term not in index]:
        return []

    # initialize the running intersection score using the first term posting list
    first_tf = query_vec[query_terms[0]]
    running_intersection_scores = [[doc_id, first_tf * qif] for (doc_id, qif) in index[query_terms[0]]]

    for term in query_terms[1:]:
        query_term_tf = query_vec[term]
        p_list = index[term]
        r_idx = p_idx = 0
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
    if len(group_scores) <= 0:
        return []

    running_merger = group_scores[0]
    for scores in group_scores[1:]:
        r_idx = s_idx = 0
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
        # manage leftovers
        if r_idx < len(running_merger):
            # running_merger still contains other docs
            new_running_merger.extend(running_merger[r_idx:])
        elif s_idx < len(scores):
            # scores still contains other docs
            new_running_merger.extend(scores[s_idx:])
        running_merger = new_running_merger
    return running_merger


def _remove_docs_with_not_terms(index, scores, not_terms):
    # prune from scores the docs containing terms in the not_terms list
    # "merging subtraction algorithm"
    if len(scores) <= 0:
        return []

    # get a list of the not terms actually present in the index
    not_terms = [term for term in not_terms if term in index]

    running_pruner = scores
    for term in not_terms:
        p_list = index[term]
        r_idx = p_idx = 0
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
        # manage leftovers
        if r_idx < len(running_pruner):
            # running_pruner still contains other docs
            new_running_pruner.extend(running_pruner[r_idx:])
        running_pruner = new_running_pruner
    return running_pruner
