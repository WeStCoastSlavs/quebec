import random
import json
import numpy as np


def gini(x):
    mad = np.abs(np.subtract.outer(x, x)).mean()
    rmad = mad/np.mean(x)
    g = 0.5 * rmad
    return g


def generateChineseRestaurant(customers):
    # First customer always sits at the first table
    tables = [1]
    gini_vals = []
    #for all other customers do
    for cust in range(2, customers+1):
        # rand between 0 and 1
        rand = random.random()
        # Total probability to sit at a table
        prob = 0
        # No table found yet
        table_found = False
        # Iterate over tables
        for table, guests in enumerate(tables):
            # calc probability for actual table and add it to total probability
            prob += guests / (cust)
            # If rand is smaller than the current total prob., customer will sit down at current table
            if rand < prob:
                # incr. #customers for that table
                tables[table] += 1
                # customer has found table
                table_found = True
                # no more tables need to be iterated, break out for loop
                break
        # If table iteration is over and no table was found, open new table
        if not table_found:
            tables.append(1)
        tables_s = sorted(tables)
        gini_vals.append(gini(tables_s))
    return tables, gini_vals

if __name__ == "__main__":
    restaurants = 1000

    network = generateChineseRestaurant(restaurants)
    with open('network_' + str(restaurants) + '.json', 'w') as out:
        json.dump(network, out)