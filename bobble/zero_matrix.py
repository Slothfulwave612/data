"""
__author__: Anmol Durgapal
"""

def zero(matrix):
    row_dict = {}
    col_dict = {}
    m = len(matrix)
    n = len(matrix[0])

    for i in range(m):
        for j in range(n):
            if matrix[i][j] == 0:
                if row_dict.get(i) == None:
                    row_dict[i] = True
                if col_dict.get(j) == None:
                    col_dict[j] = True

    for i in row_dict.keys():
        for j in range(0, n):
            matrix[i][j] = 0

    for i in col_dict.keys():
        for j in range(0, m):
            matrix[j][i] = 0
            
    return matrix
    
## provide your matrix here    
matrix = [
  [1, 1],
  [1, 0]
]    
    
print(zero(matrix))
