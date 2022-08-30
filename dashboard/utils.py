def get_top5(data):
    data.loc[:, "total"] = data.loc[:, range(2005, 2017)].sum(axis=1)
    data.sort_values("total", inplace=True, ascending=False)
    top5 = data.iloc[:5]
    return top5
