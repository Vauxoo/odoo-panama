# coding: utf-8
############################################################################
#    Module Writen For Odoo, Open Source Management Solution
#
#    Copyright (c) 2011 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
#    coded by: hugo@vauxoo.com
#    planned by: Nhomar Hernandez <nhomar@vauxoo.com>
############################################################################
import csv

csv_file_path = '../source/source_csv.csv'

csvData = csv.reader(open(csv_file_path), delimiter=',')
csvData.next()  # Headers
provincia = ''
distrito = ''
corregimiento = ''
barrio = ''
with open('../source/proseced_csv.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',',
                           quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in csvData:
        if row[0] != '':
            provincia = row[0]
        elif row[1] != '':
            distrito = row[1]
        elif row[2] != '':
            corregimiento = row[2]
        elif row[3] != '':
            barrio = row[3]
            csvwriter.writerow(
                [provincia] + [distrito] + [corregimiento] + [barrio])
        else:
            continue
        continue
