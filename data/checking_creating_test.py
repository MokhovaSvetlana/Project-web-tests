def do_result_table(form):
    max_points = count_max_points(form)
    num_result = 1
    results = [(max_points, form["result_message_max"])]
    while form.get(f"result_score_{num_result}"):
        if max_points > int(form[f"result_score_{num_result}"]):
            results.append((int(form[f"result_score_{num_result}"]), form[f"result_message_{num_result}"]))
        num_result += 1
    results.sort(key=lambda result: result[0], reverse=True)
    results_for_return = []
    for ix_result in range(len(results)):
        results_for_return.append((f"{results[ix_result + 1][0] + 1 if ix_result != len(results) - 1 else 0}-"
                                  f"{results[ix_result][0]}", results[ix_result][1]))
    return results_for_return


def count_max_points(form):
    max_points = 0
    num_question = 1
    while form.get(f"question{num_question}"):
        max_points += max(int(form[f"score{num_question}.{num_answer}"])
                          if form[f"score{num_question}.{num_answer}"].isdigit() else 0
                          for num_answer in range(1, 4))
        num_question += 1
    return max_points
