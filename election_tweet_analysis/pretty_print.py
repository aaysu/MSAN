def pretty(d, indent=0):
    if isinstance(d, dict):
        for key, value in d.iteritems():
            print '\t' * indent + str(key)
            pretty(value, indent+1)
    elif isinstance(d, list):
        for index in range(len(d)):
            print '\t' * indent + str(index)
            pretty(d[index], indent + 1)
    elif isinstance(d,basestring):
        print '\t' * indent + d
    else:
        print '\t' * indent + str(d)
