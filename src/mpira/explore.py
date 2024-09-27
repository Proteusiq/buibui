# from pathlib import Path
import duckdb


if __name__ == "__main__":
    dataf = duckdb.sql("SELECT * FROM read_json('../data/*.json', format='array')")
    print(dataf)
