import bz2
import gzip
import glob
import ams_rw_stdf
import pandas as pd
import construct
import os
import sys


_opener = {"bz2": bz2.open, "gz": gzip.open, "stdf": open}

def main():
    try:
        opath = input("where to write the xlsx to(full path preferred)")
        assert opath[-4:] == "xlsx", "only xlsx files are supported!"
        print("start to build index")
        files = filter(os.path.isfile, glob.glob("\\\\fsrwdata\\intrwp\\projects\\as5951m\\*"))
        files_with_times = [[os.path.getmtime(x), x] for x in files]

        def collect_filename_and_lot():
            for si in glob.glob("\\\\fsrwdata\\intrwp\\projects\\as5951m\\*.stdf*"):
                _ = sys.stdout.write(".")
                with _opener[si.split(".")[-1]](si, "rb") as f:
                    while True:
                        try:
                            c = ams_rw_stdf.RECORD.parse_stream(f)
                        except construct.core.StreamError as e:
                            break
                        if c.REC_TYP == 1 and c.REC_SUB == 10:
                            if len(c.PL.LOT_ID)>3:
                                yield [c.PL.LOT_ID, si] 

        df = pd.DataFrame(data=collect_filename_and_lot(), columns=["LOT ID", "File path"])
        df.to_excel(opath)
        input(f"wrote result to:{opath}... press enter to close this window")
    except Exception as e:
        print(e)
        input(f"there was a issue... sry...")
        
if __name__ == "__main__":
    main()

