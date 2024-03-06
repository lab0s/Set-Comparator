from sql_functions import *
import subprocess

local_repo_path = '' # 'D:\Sources\R20a'

# branch_name = 'remotes/origin/team4/DrtinaT/clippingResultsRefactor_REBASED12'

def get_commit_hash_by_branch_name(repo_path, branch_name):
    repo_path = local_repo_path
    cmd = ['git', 'rev-parse', branch_name]
    try:
        result = subprocess.run(cmd, cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return result.stdout.decode().strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

def get_branch_name_by_commit_hash(repo_path, commit_hash):
    cmd = ['git', 'name-rev', '--name-only', commit_hash]
    try:
        result = subprocess.run(cmd, cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return result.stdout.decode().strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None


def get_parent_branch_hash(repo_path, branch_name):
    cmd = ['git', 'rev-parse', f"{branch_name}^"]
    try:
        result = subprocess.run(cmd, cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return result.stdout.decode().strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

def get_commit_author_by_commit_hash(repo_path, commit_hash):
    cmd = ['git', 'show', '--format=%an <%ae>', commit_hash]
    try:
        result = subprocess.run(cmd, cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        output_lines =  result.stdout.decode().split('\n')
        author_name = output_lines[0].split()[0]
        return author_name
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

def get_parent_HEAD_automatic_run_hash_SQL(repo_path, branch_name):
    # instead of brancg_name we can use commit_hash
    i = 0

    flag = True
    while flag:
        cmd = ['git', 'rev-parse', f"{branch_name}~{i}"]
        try:
            git_hash = subprocess.run(cmd, cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            git_hash = git_hash.stdout.decode().strip()
            git_hash = git_hash[:11]

            if is_exist_atumatic_run(git_hash) == git_hash:
                flag = False
                return git_hash[:11] # part of list due to commit in NG
            else:
                i += 1
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None

def get_parent_HEAD_automatic_run_ng_setID(repo_path, actual_set_ID):
    try:
        actual_ng_hash = get_ng_hash_by_setID(actual_set_ID)
        # print(f'actual_ng_hash: {actual_ng_hash}')
        parent_hash = get_parent_HEAD_automatic_run_hash_SQL(repo_path, actual_ng_hash)
        # print(f'parent_hash: {parent_hash}')
        parent_setID_by_hash = get_setID_by_hash(parent_hash)
        # print(f'parent_setID_by_hash: {parent_setID_by_hash}')
        return parent_setID_by_hash
    except Exception as e:
        # print(f'Error: {e}')
        return "GM not found"

def get_last_nth_GM_commit_hash_SQL(repo_path, n=0):
    GM_branch_name = 'origin/HEAD'
    cmd = ['git', 'rev-parse', f"{GM_branch_name}~{n}"]
    try:
        result = subprocess.run(cmd, cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return result.stdout.decode().strip()[:11]
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

# print(get_parent_HEAD_automatic_run_ng_setID(local_repo_path, 34655))
# print(get_parent_HEAD_automatic_run_hash_SQL(local_repo_path, '3a4c2dc76f8'))