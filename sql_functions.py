import pyodbc  # https://github.com/mkleehammer/pyodbc/wiki
import os
from pprint import pprint


connection_string: str = (
    "Driver={SQL Server};"
    "Server={CZ-DBS1.dlubal.local};"
    "Database={netgenium};"
    "Trusted_Connection=Yes"
)
autocommit = False

connection = pyodbc.connect(
    connection_string,
    autocommit=autocommit,
)

def get_failed_examples(ng_set) -> int:
    run_dict = {}
    set_runs = f"SELECT ng_exampleid, ng_runid FROM ng_testexamplerun0 WHERE ng_set = {ng_set} AND ng_runstatus != 'Passed'"
    cursor_set_runs = connection.cursor().execute(set_runs).fetchall()
    for row in cursor_set_runs:
        # print(row.ng_exampleid, row.ng_runid)
        run_dict[row.ng_exampleid] = row.ng_runid
    return run_dict

def get_newest_TIMER_Automatic_run():
    set_runs = f"SELECT TOP (1) ng_setid FROM ng_testexampleset0 WHERE ng_user = 'TIMER' AND ng_testexamplesetname = 'Automatic' ORDER BY ng_setid DESC"
    cursor_set_runs = connection.cursor().execute(set_runs).fetchall()
    newest_run = cursor_set_runs[0].ng_setid
    return newest_run

def combine_two_runs(ng_set1, ng_set2):
    combined_runs = []
    dict1 = get_failed_examples(ng_set1)
    dict2 = get_failed_examples(ng_set2)

    for key in dict1:
        if key in dict2:
            combined_runs.append([dict1[key], dict2[key]])
    
    return combined_runs

pprint(combine_two_runs(33043, 33033))





# pprint(get_failed_examples(33157))