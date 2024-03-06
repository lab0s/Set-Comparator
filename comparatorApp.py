import subprocess

# Path to comparetor.exe
comparator_path = 'T:/Tools/aTC_bin/bin/comparator.exe'


def run_comparator(
        first_path,
        second_path,
        diff_path,
        absolute_tolerance,
        relative_tolerance,
        compare_absolute_values,
        ignore_strings
):
    """
    Inputs:
    first_path -> string
    second_path -> string
    diff_path -> string
    absolute_tolerance -> float
    relative_tolerance -> float
    compare_absolute_values -> bool
        -> 0 - False
        -> 1 - True
    ignore_strings -> bool
        -> 0 - False
        -> 1 - True
    bool values must be inputed as 0 or 1 and not as True or False

    Outputs:
    0 - No difference found
    1 - You entered incorrect parameters
    2 - Difference found
    else - Diff cannot be done or missing data
    """
    process = subprocess.Popen([
        comparator_path, 
        f"{first_path}", 
        f"{second_path}", 
        f"{diff_path}", 
        f"{absolute_tolerance}", 
        f"{relative_tolerance}", 
        f"{compare_absolute_values}", 
        f"{ignore_strings}"],
        stdout=subprocess.PIPE)
    
    process.wait()
    output = process.returncode
    process.terminate()

    # print(first_path)
    # print(second_path)
    # print(output)
    # print()

    return output

