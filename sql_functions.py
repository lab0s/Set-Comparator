import pyodbc  # https://github.com/mkleehammer/pyodbc/wiki
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

cursor = connection.cursor()

def get_TE_folders_subfolders():
    test_dict = {}

    query = "SELECT ng_exampleid FROM ng_testexample0"
    query_exec = cursor.execute(query).fetchall()

    for row_testID in query_exec:
        testID = str(row_testID.ng_exampleid)
        test_dict[testID] = []

        query = f"SELECT ng_runid, ng_exampleid FROM ng_testexamplerun0 WHERE ng_exampleid = {testID}"
        query_exec = connection.cursor().execute(query).fetchall()

        for row_runID in query_exec:
            runID = str(row_runID.ng_runid)
            test_dict[testID].append(runID)
    
    return test_dict

def get_testID_from_runID(runID):
    query = f"SELECT ng_exampleid FROM ng_testexamplerun0 WHERE ng_runid = {runID}"
    query_exec = cursor.execute(query).fetchall()
    testID = query_exec[0].ng_exampleid
    return testID

def get_examples(ng_set) -> int:
    """
    Returns a dictionary with example IDs as keys and run IDs as values
    """
    run_dict = {}
    query = f"SELECT ng_exampleid, ng_runid FROM ng_testexamplerun0 WHERE ng_set = {ng_set}"
    query_exec = cursor.execute(query).fetchall()
    for row in query_exec:
        run_dict[row.ng_exampleid] = row.ng_runid
    return run_dict

def is_set_ID_exist(ng_set):
    query = f"SELECT TOP (1) ng_setid FROM ng_testexampleset0 WHERE ng_setid = {ng_set}"
    query_exec = cursor.execute(query).fetchall()
    if query_exec:
        return True
    else:
        return False

def get_failed_examples(ng_set) -> int:
    run_dict = {}
    query = f"SELECT ng_exampleid, ng_runid FROM ng_testexamplerun0 WHERE ng_set = {ng_set} AND ng_runstatus != 'Passed'"
    query_exec = cursor.execute(query).fetchall()
    for row in query_exec:
        run_dict[row.ng_exampleid] = row.ng_runid
    return run_dict

def get_newest_TIMER_Automatic_run():
    query = f"SELECT TOP (1) ng_setid FROM ng_testexampleset0 WHERE ng_user = 'TIMER' AND ng_testexamplesetname = 'Automatic' ORDER BY ng_setid DESC"
    query_exec = cursor.execute(query).fetchall()
    newest_run = query_exec[0].ng_setid
    return newest_run

def get_setID_by_hash(ng_hash):
    query = f"SELECT TOP (1) ng_setid FROM ng_testexampleset0 WHERE ng_hash = '{ng_hash}' AND ng_testexamplesetname = 'Automatic' AND ng_user = 'TIMER' ORDER BY ng_setid DESC"
    query_exec = cursor.execute(query).fetchall()
    setID_by_hash = query_exec[0].ng_setid
    return setID_by_hash

# print(get_setID_by_hash('0dcd86e33ff'))

def get_ng_hash_by_setID(ng_set):
    query = f"SELECT TOP (1) ng_hash FROM ng_testexampleset0 WHERE ng_setid = {ng_set}"
    query_exec = cursor.execute(query).fetchall()
    ng_hash_by_setID = query_exec[0].ng_hash
    return ng_hash_by_setID

def get_TE_absolute_tolerance(ng_exampleid):
    query = f"SELECT ng_absolutetolerance FROM ng_testexample0 WHERE ng_exampleid = {ng_exampleid}"
    query_exec = connection.cursor().execute(query).fetchall()
    absolute_tolerance = query_exec[0].ng_absolutetolerance
    return absolute_tolerance

def get_TE_relative_tolerance(ng_exampleid):
    query = f"SELECT ng_relativetolerance FROM ng_testexample0 WHERE ng_exampleid = {ng_exampleid}"
    query_exec = cursor.execute(query).fetchall()
    relative_tolerance = query_exec[0].ng_relativetolerance
    return relative_tolerance

def is_exist_atumatic_run(repository_commit_hash):
    """
    Return latest automatic run of GM according to parent of concrete branch
    -> commit_hash -> input from git
    -> find in NG database latest build version run based on commit_hash
    """
    try:
        query = f"SELECT ng_hash FROM ng_testexampleset0 WHERE ng_user = 'TIMER' AND ng_testexamplesetname = 'Automatic' AND ng_branch = 'grandmaster' AND ng_hash = '{repository_commit_hash}' ORDER BY id DESC"
        query_exec = cursor.execute(query).fetchall()
        gm_hash = query_exec[0].ng_hash
        return gm_hash
    except:
        return None
    
def get_branch_name_by_setID(ng_set):
    query = f"SELECT ng_branch FROM ng_testexampleset0 WHERE ng_setid = {ng_set}"
    query_exec = cursor.execute(query).fetchall()
    branch_name = query_exec[0].ng_branch
    return branch_name
    
def combine_two_runs(ng_set1, ng_set2, ng_set1_fail_only=True):
    if ng_set1_fail_only:
        combined_runs = []
        dict1 = get_failed_examples(ng_set1)
        dict2 = get_examples(ng_set2)

        for key in dict1:
            if key in dict2:
                combined_runs.append([dict1[key], dict2[key]])
        return combined_runs
        
    else:
        combined_runs = []
        dict1 = get_examples(ng_set1)
        dict2 = get_examples(ng_set2)

        for key in dict1:
            if key in dict2:
                combined_runs.append([dict1[key], dict2[key]])
        return combined_runs

        