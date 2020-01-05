def data_reader_200105(file_data, separator=','):
    """ignore #
    ignore line without string
    target and logic are separated by separator"""
    file_data.readline()#delete first line

    dict_target_logic = {}

    for s_line in file_data:
        if '#' in s_line:
            s_line = s_line[:s_line.find('#')]
            #ignore Remarks
        s_line = s_line.strip()
        if len(s_line) == 0:
            continue

        s_target, s_logic = s_line.split(separator)
        dict_target_logic[s_target] = s_logic

    return dict_target_logic
