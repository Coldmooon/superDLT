import json
import re
import requests
from requests.adapters import HTTPAdapter
import os
import numpy as np


def lotteryResult(file_path='dltData.json'):

    with open(file_path, "r") as f:
        # Load the JSON data from the file
        X = json.load(f)
   
    total = X['value']['total']

    # Y is a lottery results string list.
    Y = [ X['value']['list'][i]['lotteryDrawResult'] for i in range(total)]
    T = [ {'lotteryDrawTime':X['value']['list'][i]['lotteryDrawTime'],
           'lotteryDrawNum': X['value']['list'][i]['lotteryDrawNum']} for i in range(total)]

    # Initialize the one-hot matrix with zeros
    one_hot_matrix = np.zeros((total, 35))
    
    # Iterate through each element in Y
    for i, element in enumerate(Y):
        # Split the element string into individual numbers
        numbers = element.split()
    
        # Iterate through each number in the element
        for number in numbers[:5]:
            # Convert the number to an integer and subtract 1 to get the column index
            column_index = int(number) - 1
    
            # Set the corresponding column in the one-hot matrix to 1
            one_hot_matrix[i, column_index] = 1
   
    # Calculate the similarity matrix
    similarity_matrix = np.dot(one_hot_matrix, one_hot_matrix.T).astype(int)

    # Set diagonal elements to 0
    np.fill_diagonal(similarity_matrix, 0)
    
    return similarity_matrix, one_hot_matrix, T

def lotteryStats(collision, similarity_matrix, T):
    # Find the positions where the similarity matrix equals the given number.
    positions = np.argwhere(similarity_matrix == collision)
    
    # Get the total count of number 5 occurrences
    count = len(positions)/2
    
    # Output the positions and count
    print("重复出现 " + str(collision) + " 个数的位置:")
    for pos in positions:
        print(pos, ": ", T[pos[0]]['lotteryDrawNum'], ' 和 ',  T[pos[1]]['lotteryDrawNum'])
    print("总计:", count)
    
def takeLook(your_number, one_hot_matrix, T):
    
    one_hot_vec = np.zeros((1, 35))
    
    # Iterate through each element in Y
    for element in your_number:
        column_index = int(element) - 1
        one_hot_vec[0, column_index] = 1
   
    # Calculate the similarity matrix
    res = np.dot(one_hot_matrix, one_hot_vec.T).astype(int)
    res = res.flatten()
    
    collision_dict = {}

    values_to_find = [5, 4, 3]

    for value in values_to_find:
        collision_dict[value] = np.argwhere(res == value).flatten().tolist()

    for value, positions in collision_dict.items():
        count = len(positions)
        if count > 0:
            print("\n重了 " + str(value) + " 个数的有 " + str(count) + " 次，分别在：")
    #         print(f"Value {value}: {positions} \n")
            for pos in positions:
                print("  :", T[pos]['lotteryDrawNum'], " 期")
        else:
            print("\n没有重了 " + str(value) + " 个数的情况。")
 
    return res
    
