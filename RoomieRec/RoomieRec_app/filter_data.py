def filter(listings, input):
    keep = []
    for index, row in listings.iterrows():
        logical = []
        if input[0] is not None:
            if row['price'] <= input[0]:
                logical.append(True)
            else:
                logical.append(False)
        else:
            logical.append(True)
        if input[1] is not None:
            if row['price'] >= input[1]:
                logical.append(True)
            else:
                logical.append(False)
        else:
            logical.append(True)
        if input[2] is not None and row['movein'] is not None:
            if row['movein'] <= input[2]:
                logical.append(True)
            else:
                logical.append(False)
        else:
            logical.append(True)
        if input[3]:
            if row['neighborhood'] in input[3]:
                logical.append(True)
            else:
                logical.append(False)
        else:
            logical.append(True)
        if input[4]:
            deep_logical = []
            for attribute in input[4]:
                if attribute in row['attributes']:
                    deep_logical.append(True)
                else:
                    deep_logical.append(False)
            if all(deep_logical):
                logical.append(True)
            else:
                logical.append(False)
        else:
            logical.append(True)
        if all(logical):
            keep.append(index)
    return keep
