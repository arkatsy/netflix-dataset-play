"""
The original netflix_titles.csv file contains 'cast' as a column.
'cast' is a reserved keyword in postgres.

Instead of escaping the column name every time, 
this script renames the column 'cast' to 'show_cast' and writes the new header with
the rest of the rows to a new file named "./netflix_titles_fixed.csv"
"""

import csv


def rename_cast_to_show_cast(write_to_file_path: str = "./netflix_titles_fixed.csv", encoding: str = "latin1"):
    with open("./netflix_titles.csv", "r", encoding=encoding) as file:
        reader = csv.reader(file)
        header = next(reader)

        cast_index = header.index("cast")
        header[cast_index] = "show_cast"

        with open(write_to_file_path, "w", encoding=encoding) as new_file:
            writer = csv.writer(new_file)
            writer.writerow(header)
            for row in reader:
                writer.writerow(row)
