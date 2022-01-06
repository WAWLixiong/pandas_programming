import pandas as pd
import numpy as np


def test1():
    """整理透视， pd.pivot 只能对数据进行整理，遇到重复数据会报错"""
    df = pd.DataFrame({
        'foo': ['one', 'one', 'one', 'two', 'two', 'two'],
        'bar': ['A', 'B', 'C', 'A', 'B', 'C'],
        'baz': [1, 2, 3, 4, 5, 6],
        'zoo': ['x', 'y', 'z', 'q', 'w', 't']
    })
    pivot_df = df.pivot(index='foo', columns='bar', values='baz')
    print(pivot_df)
    print(pivot_df.index)


def test2():
    """实现excel的聚合透视"""
    df = pd.DataFrame({
        "A": ["foo", "foo", "foo", "foo", "foo", "bar", "bar", "bar", "bar"],
        "B": ["one", "one", "one", "two", "two", "one", "one", "two", "two"],
        "C": ["small", "large", "large", "small", "small", "large", "small", "small", "large"],
        "D": [1, 2, 2, 3, 3, 4, 5, 6, 7],
        "E": [2, 4, 5, 5, 6, 6, 8, 9, 9]
    })
    print(df)
    print('=========')
    pivot_df = df.pivot_table(
        index=['A', 'B'], columns=['C'], values='D', aggfunc=np.sum, margins=True, margins_name='sum'
    )
    print(pivot_df)
    print('=========')
    table = pd.pivot_table(df, values=['D', 'E'], index=['A', 'C'], aggfunc={'D': np.mean, 'E': [min, max, np.mean]})
    print(table)


if __name__ == '__main__':
    test2()
