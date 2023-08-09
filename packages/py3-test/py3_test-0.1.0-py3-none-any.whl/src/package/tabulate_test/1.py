from tabulate import tabulate

d = [["Mark", 12, 95], ["Jay", 11, 88], ["Jack", 14, 90]]

print(tabulate(d, headers=["Name", "Age", "Percent"]))
