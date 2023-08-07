def chunks(lst, n, reverse=False):
    """return successive n-sized chunks from lst."""
    res = []
    for i in range(0, len(lst), n):
        if reverse:
            res += [reversed(lst[i:i + n])]
        else:
            res += [lst[i:i + n]]
    return res
