import json


def checking_results(test, answers):   # answers - list
    ''' Return dict with structure: {'result': 'text',
                                    'points': score of user <type int>, 'max_points': max score what user can get <type int>}.
       'points' and 'max_points' are optional parameters which are given by the key 'with_points' '''
    with_points = test['with_points']
    results = json.loads(test['results'])
    score = 0
    max_score = 0
    for ix, question in enumerate(test['questions']):
        score += question['answers'][answers[ix]]
        max_score += max(question['answers'].values())
    result_of_user = {}
    for r in results:
        if r.isdigit():
            if score == int(r):
                result_of_user = {'result': results[r]}
                break
        else:
            res_mn, res_mx = [int(x.strip()) for x in r.split('-')]
            if res_mn <= score <= res_mx:
                result_of_user = {'result': results[r]}
                break
    if with_points:
        result_of_user['points'] = score
        result_of_user['max_points'] = max_score
    return result_of_user
