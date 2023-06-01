from bs4 import BeautifulSoup
import re
from collections import Counter
import psycopg2
import random

html = """
<html>
<head>
<title>Our Python Class exam</title>

<style type="text/css">

	body{
		width:1000px;
		margin: auto;
	}
	table,tr,td{
		border:solid;
		padding: 5px;
	}
	table{
		border-collapse: collapse;
		width:100%;
	}
	h3{
		font-size: 25px;
		color:green;
		text-align: center;
		margin-top: 100px;
	}
	p{
		font-size: 18px;
		font-weight: bold;
	}
</style>

</head>
<body>
<h3>TABLE SHOWING COLOURS OF DRESS BY WORKERS AT BINCOM ICT FOR THE WEEK</h3>
<table>

	<thead>
		<th>DAY</th><th>COLOURS</th>
	</thead>
	<tbody>
	<tr>
		<td>MONDAY</td>
		<td>GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, BLUE, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN</td>
	</tr>
	<tr>
		<td>TUESDAY</td>
		<td>ARSH, BROWN, GREEN, BROWN, BLUE, BLUE, BLEW, PINK, PINK, ORANGE, ORANGE, RED, WHITE, BLUE, WHITE, WHITE, BLUE, BLUE, BLUE</td>
	</tr>
	<tr>
		<td>WEDNESDAY</td>
		<td>GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, RED, YELLOW, ORANGE, RED, ORANGE, RED, BLUE, BLUE, WHITE, BLUE, BLUE, WHITE, WHITE</td>
	</tr>
	<tr>
		<td>THURSDAY</td>
		<td>BLUE, BLUE, GREEN, WHITE, BLUE, BROWN, PINK, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN</td>
	</tr>
	<tr>
		<td>FRIDAY</td>
		<td>GREEN, WHITE, GREEN, BROWN, BLUE, BLUE, BLACK, WHITE, ORANGE, RED, RED, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, WHITE</td>
	</tr>

	</tbody>
</table>

<p>Examine the sequence below very well, you will discover that for every 1s that appear 3 times, the output will be one, otherwise the output will be 0.</p>
<p>0101101011101011011101101000111 <span style="color:orange;">Input</span></p>
<p>0000000000100000000100000000001 <span style="color:orange;">Output</span></p>
<p>
</body>
</html>
"""

scrape_with_Bsoup = BeautifulSoup(html, 'html.parser')

# I Extracted color data from the table
color_table = scrape_with_Bsoup.find('table')
color_rows = color_table.find_all('tr')[1:]
colors = []

for row in color_rows:
    color_data = row.find_all('td')[1].text.strip()
    colors += re.findall(r'\b\w+\b', color_data)

# 1. Finding the mean color in the table
finding_mean_color = Counter(colors).most_common(1)[0][0]

# 2. Finding the color mostly worn throughout the week
most_common_color = Counter(colors).most_common(1)[0][0]

# 3. Finding the median color
sorted_colors = sorted(colors)
n = len(sorted_colors)
if n % 2 == 0:
    median_color = sorted_colors[n // 2 - 1]
else:
    median_color = sorted_colors[n // 2]

# 4. Calculating the variance of the colors
color_counts = Counter(colors)
total_count = sum(color_counts.values())
variance = sum((count / total_count) * ((count / total_count) - 1) for count in color_counts.values())

# 5. Calculating the probability that the color is red
red_probability = color_counts['RED'] / total_count

# Printing the results
print("1. Mean color:", finding_mean_color)
print("2. Most worn color throughout the week:", most_common_color)
print("3. Median color:", median_color)
print("4. Variance of colors:", variance)
print("5. Probability that the color is red:", red_probability)

# 6. Saving the colors and their frequencies in PostgreSQL database
dataconnection = psycopg2.connect(database="class_exam", user="", password="",
                                  host="localhost", port="")
cursor = dataconnection.cursor()

# Create a table to store color frequencies
cursor.execute("CREATE TABLE IF NOT EXISTS color_frequencies (color TEXT PRIMARY KEY, frequency INTEGER)")

# adding colors frequencies into the table
for color, count in color_counts.items():
    cursor.execute("INSERT INTO color_frequencies (color, frequency) VALUES (%s, %s)", (color, count))

# Committing  changes and closing the connection
dataconnection.commit()
dataconnection.close()


# 7. Recursive searching algorithm to search for a number entered by the user in a list of numbers
def recursive_search(number, number_list, start_index=0):
    if start_index >= len(number_list):
        return False
    if number_list[start_index] == number:
        return True
    return recursive_search(number, number_list, start_index + 1)


# Testing recursive searching algorithm
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
search_number = int(input("Enter a number to search: "))
found = recursive_search(search_number, numbers)
if found:
    print("Number found in the list.")
else:
    print("Number not found in the list.")

# 8. Generating 4-digit random numbers of 0s and 1s and convert them to base 10
random_number = ''.join(random.choice('01') for _ in range(4))
decimal_number = int(random_number, 2)

print("Random 4-digit number:", random_number)
print("Decimal equivalent:", decimal_number)


# 9. Summing the first 50 Fibonacci sequence
def sum_fibonacci(n):
    fib_sequence = [0, 1]
    for i in range(2, n):
        fib_sequence.append(fib_sequence[i - 1] + fib_sequence[i - 2])
    return sum(fib_sequence[:n])


fib_sum = sum_fibonacci(50)
print("Sum of the first 50 Fibonacci numbers:", fib_sum)
