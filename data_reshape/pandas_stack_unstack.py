import pandas as pd


def test1():
    """stack以后成为一个Series"""
    df_single_level_cols = pd.DataFrame(
        [[0, 1], [2, 3]],
        index=['cat', 'dog'],
        columns=['weight', 'height']
    )
    print(df_single_level_cols)
    stacked_df = df_single_level_cols.stack()
    print(stacked_df)
    print(type(stacked_df))


if __name__ == '__main__':
    test1()
