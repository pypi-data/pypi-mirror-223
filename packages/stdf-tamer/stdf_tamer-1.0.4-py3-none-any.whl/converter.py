"""export stdf data to more usefull format.

Usage:
  stdfconvert --output=<output> --stdf-in=<stdf-in> [--compression=<zstd>]

Options:
  -h --help     Show this screen.
"""
import ams_rw_stdf
import bz2
import construct
from docopt import docopt
import gzip
import pathlib
import polars as pl
from rich.console import Console
import collections
import time
import sys


console = Console()
err_console = Console(stderr=True, style="bold red")
_opener = {"bz2": bz2.open, "gz": gzip.open, "stdf": open}

schema = [('Test_Nr', pl.Int64),
          ('Test_Name', pl.Utf8),
          ('ULim', pl.Float64), 
          ('LLim', pl.Float64),
          ('res', pl.Float64)]

output_writers = {".ipc":     lambda df, outpath, compression: df.write_ipc(outpath, compression=compression),
                  ".feather": lambda df, outpath, compression: df.write_ipc(outpath, compression=compression),
                  ".parquet": lambda df, outpath, compression: df.write_parquet(outpath, compression=compression),
                  ".xlsx":    lambda df, outpath, _: df.write_excel(outpath)}

tests = 0                 # global to allow to use this value for information printing...

# global to allow for allowing lean data colleciton, setting these global values just once
operator = None           
test_cod = None
lot_id  = None
start_t = None    

def _iter_stream(f):
    try:
        while True:
            yield ams_rw_stdf.parse_record(f)
    except construct.core.StreamError as e:
        if "stream read less than specified amount, expected 2, found 0" not in str(e):
            err_console.print_exception()
            sys.exit(1)
    except Exception as e:
        err_console.print(f"Parsing issue")
        err_console.print_exception()
        sys.exit(1)

def worker(si, ftype):
    with _opener[ftype](si, "rb") as f:
        data = None
        for c in _iter_stream(f):
            type_and_subtyp = (c.REC_TYP, c.REC_SUB,)
            if type_and_subtyp == (15, 10,):
                key = (c.PL.HEAD_NUM<<8) | c.PL.SITE_NUM
                data[key].append((c.PL.TEST_NUM, c.PL.TEST_TXT, 
                                  c.PL.HI_LIMIT, c.PL.LO_LIMIT,
                                  c.PL.RESULT,))
            elif type_and_subtyp == (5, 20,):
                global tests
                key = (c.PL.HEAD_NUM<<8) | c.PL.SITE_NUM
                part_tests = len(data[key])
                tests += part_tests
                console.print(f"Adding part {c.PL.PART_TXT}/{c.PL.PART_ID} of head {c.PL.HEAD_NUM} site {c.PL.SITE_NUM} a total of {part_tests} tests...")
                yield pl.LazyFrame(data[key], schema=schema).with_columns(pl.lit(c.PL.PART_ID).cast(pl.Utf8).alias("part_id"), 
                                                                          pl.lit(c.PL.PART_TXT).cast(pl.Utf8).alias("part_txt"),)
                data[key] = []
            elif type_and_subtyp == (1, 10,):
                global operator
                global test_cod
                global lot_id
                global start_t

                test_cod = c.PL.TEST_COD
                lot_id   = c.PL.LOT_ID
                operator = c.PL.OPER_NAM
                start_t = c.PL.START_T
                data = collections.defaultdict(lambda : [])
                console.print(f"Converting LOT ID: '{lot_id}'...")

def main():
    start_time = time.time()
    try:
        arguments = docopt(__doc__)
        outpath = pathlib.Path(arguments["--output"])
        si = arguments["--stdf-in"]
        ftype = si.split(".")[-1]
            
        if ftype not in _opener:
            err_console.print(f"{ftype} is an unsupported file extension, only *.{', *.'.join(_opener.keys())} are supported")
            sys.exit(1)
        if outpath.suffix not in output_writers:
            err_console.print(f"please use one of these file formats as output: *{', *'.join(output_writers.keys())}")
            sys.exit(1)
        
        data = pl.concat(worker(si, ftype), rechunk=False)
        data = data.with_columns(pl.lit(test_cod).cast(pl.Categorical).alias("TEST_COD"),
                                 pl.lit(lot_id).cast(pl.Categorical).alias("lot_id"),
                                 pl.lit(operator).cast(pl.Categorical).alias("operator"),
                                 pl.lit(start_t).cast(pl.UInt32).alias("START_T"),
                                 pl.col("part_id").cast(pl.Categorical).alias("part_id"),
                                 pl.col("part_txt").cast(pl.Categorical).alias("part_txt"),)
        output_writers[outpath.suffix](data.collect(), outpath, compression=arguments["--compression"])
        runtime = time.time()-start_time
        console.print(f"conversion complete. Took {runtime:0.3f} s  {tests/runtime:0.1f} tests/s, succesfully written {outpath}")
    except Exception as e:
        err_console.print_exception()

if __name__ == "__main__":
    main()
