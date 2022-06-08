"""
This is the main Driver file for processing.
"""

from src.utils import *

if __name__ == "__main__":
    url, params = take_input()
    results = initial_checks(url, params)
    if not results:
        print("Not able to process this API endpoint")
    else:
        variable_dict = construct_base_structure(results)
        primary, variable_dict = generate_results(results, variable_dict)
        generate_files(variable_dict, primary, cloud_mode=True)
