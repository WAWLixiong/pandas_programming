import polars as pl


def test1():
    df = pl.read_csv("https://j.mp/iriscsv")
    df = (df.filter(pl.col("sepal_length") > 5)
          .groupby("species")
          .agg(pl.all().sum())
          )


if __name__ == '__main__':
    test1()
