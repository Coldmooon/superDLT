import json
import re
import requests
from requests.adapters import HTTPAdapter
import os
import numpy as np


def main():
    file_path = "dltData.json"

    with open(file_path, "r") as f:
        # Load the JSON data from the file
        X = json.load(f)
   
    total = X['value']['total']

    # Access the loaded JSON data
    # print(X['value']['list'][0]['lotteryDrawResult'])
    # print(X['value']['list'][2446]['lotteryDrawResult'])

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

    # Round the similarity matrix to the nearest integer
    # rounded_matrix = np.round(similarity_matrix).astype(int)
    
    # Find the positions where the similarity matrix equals 5
    positions = np.argwhere(similarity_matrix == 5)
    
    # Get the total count of number 5 occurrences
    count = len(positions)
    
    # Output the positions and count
    print("Positions:")
    for pos in positions:
        print(pos, ": ", T[pos[0]]['lotteryDrawNum'],' and ', T[pos[1]]['lotteryDrawNum'])
    print("Total count:", count)

if __name__ == '__main__':
    main()
