import csv

with open('./laptops.csv', mode="r", encoding='UTF-8') as file:
    # create a CSV reader object
    csv_reader = csv.reader(file)

    # iterate over each row in the CSV file
    for row in csv_reader:
        # print each item in the row
        for item in row:
            print(item)
