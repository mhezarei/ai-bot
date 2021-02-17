def find_fit_word(answer, select_number):
    if select_number:
        if len(answer["city"]) == 2:
            return answer["city"][1]
        if len(answer["date"]) == 2:
            return answer["date"][1]
        if len(answer["religious_time"]) == 2:
            return answer["religious_time"][1]
        if len(answer["time"]) == 2:
            return answer["time"][1]
        return answer["city"][0]
    elif not select_number:
        if len(answer["city"]) == 2:
            return answer["city"][0]
        if len(answer["date"]) == 2:
            return answer["date"][0]
        if len(answer["religious_time"]) == 2:
            return answer["religious_time"][0]
        if len(answer["time"]) == 2:
            return answer["time"][0]
        return answer["city"][0]
