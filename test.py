import requests

# URL endpoint for generating Sudoku board
url = 'https://sugoku.onrender.com/board?difficulty=random'

# Sending GET request to the API
response = requests.get(url)

# Parsing the response JSON
data = response.json()

# Printing the generated Sudoku board
print("Generated Sudoku Board:")
print(type(data['board']))
for row in data['board']:
    print(row)
