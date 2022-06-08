"""
This file consists of all the utils that can be called to process and Flatten the API endpoints.
"""

import json
import os.path

import requests
import pandas as pd

"""                                       Initialize Global Variables                                                """

"""              Take inputs from user. Remove this part in Lambda deployment and extract from event                 """


def take_input():
    """
    Take URL as input from the user as well as any params that need to be sent.
    :return:
    """
    print("Enter URL: ")
    url = input()  # https://jsonplaceholder.typicode.com/todos example
    print("Enter params: ")
    params = json.loads(input())  # Example: {}
    return url, params


"""                  Initialize the application and check if the current script will work on this                    """


def initial_checks(url, params):
    """
    Check if the current script will be able to process this API endpoint or not.
    :param url: URL that is to be flattened
    :param params: Any required params for processing.
    :return: Returns either results or None in case the response is not suupported.
    """
    result1 = requests.get(
        url,
        params=params
    )
    results = result1.json()
    if type(results) == list:
        return results
    elif type(results) == dict and len(results.keys()) == 1 and type(results[results.keys()[0]]) == list:
        return results[results.keys()[0]]

    return None


def construct_base_structure(results):
    """
    Construct base structure of the primary keys.
    :param results: List of results
    :return: Create base Structure of documents.
    """
    variable_dict ={}
    re_json = results[0]
    for j in re_json:
        if isinstance(re_json[j], list) or isinstance(re_json[j], dict):
            variable_dict[j] = []
    return variable_dict


"""                                      Solution for generating the files                                           """


def generate_results(results, variable_dict):
    """
    Load data in python object.
    :param results: The result list
    :param variable_dict:
    :return: Primary and structured document list
    """
    primary = []
    for abc in results:
        for key in abc:
            if isinstance(abc[key], dict):
                abc[key]['number'] = abc['number']
                variable_dict[key].append(abc[key])
            if isinstance(abc[key], list):
                for idx in range(len(abc[key])):
                    abc[key][idx]['number'] = abc['number']
                    if key not in variable_dict:
                        variable_dict[key] = []
                    try:
                        variable_dict[key].append(abc[key][idx])
                    except Exception as e:
                        print(e)

        for key in variable_dict:
            if key in abc:
                del abc[key]
        primary.append(abc)
    return primary, variable_dict


def generate_files(variable_dict, primary, cloud_mode=False):
    """
    Load results in a Dataframe and convert to CSV files. Append if the file already exists otherwise create.
    :param variable_dict: Structured list of objects
    :param primary: Main list
    :param cloud_mode: By default files will be generated in local otherwise in the tmp directory.
    """
    for key in variable_dict:
        df = pd.DataFrame(variable_dict[key])
        file_exists = os.path.exists(f'{key}.csv')
        if file_exists:
            df1 = pd.read_csv(f'{key}.csv')
            df = pd.concat([df, df1])
        df.to_csv("/tmp/" if cloud_mode else "" + key + ".csv", index=False)

    df = pd.DataFrame(primary)
    file_exists = os.path.exists('primary.csv')
    if file_exists:
        df1 = pd.read_csv(f'primary.csv')
        df = pd.concat([df, df1])
    df.to_csv("/tmp/primary.csv" if cloud_mode else "primary.csv", index=False)
