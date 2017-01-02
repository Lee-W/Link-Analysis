from itertools import islice, product

from Association_Rule import find_frequent_patterns, generate_association_rules, load_data


def rolling_window(seq, n=2):
    it = iter(seq)
    result = tuple(islice(it, n))

    if len(result) == n:
        yield result
    for element in it:
        result = result[1:] + (element,)
        yield result


def transactions_to_graph(transactions, output_filename):
    EDGE_FORMAT_STR = '{source},{dest}\n'
    with open(output_filename, 'w') as output_file:
        for transaction in transactions:
            for edge in rolling_window(transaction):
                source, dest = edge
                output_file.write(EDGE_FORMAT_STR.format(source=source, dest=dest))


def association_rule_to_graph(association_rules, output_filename):
    EDGE_FORMAT_STR = '{source},{dest}\n'

    edges = set()
    for cause, effect in association_rules.keys():
        for p in product(cause, effect):
            edges.add(p)

    with open(output_filename, 'w') as output_file:
        for source, dest in edges:
            output_file.write(EDGE_FORMAT_STR.format(source=source, dest=dest))


if __name__ == "__main__":
    input_filename = './ibm_data/data.ntrans_5.tlen_3.nitems_0.01'
    min_support = 0.2
    min_confident = 0.4
    output_file1 = 'dataset/graph_7.txt'
    output_file2 = 'dataset/graph_8.txt'

    transactions = list(load_data(input_filename))
    transactions_to_graph(transactions, output_file1)

    number_of_transactions = len(transactions)
    min_support_count = int(number_of_transactions * min_support)
    frequent_patterns = find_frequent_patterns(transactions, min_support_count)
    association_rules = generate_association_rules(frequent_patterns, min_confident)
    association_rule_to_graph(association_rules, output_file2)
