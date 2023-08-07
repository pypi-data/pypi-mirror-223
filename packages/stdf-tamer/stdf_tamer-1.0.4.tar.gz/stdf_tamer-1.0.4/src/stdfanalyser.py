"""List records in stdf file.

Usage:
  stdfanalyse <stdf_file_name_in>

Options:
  -h --help     Show this screen.
"""


import ams_rw_stdf
import bz2
import construct
from docopt import docopt
import gzip
from rich.console import Console


_opener = {"bz2": bz2.open, "gz": gzip.open, "stdf": open}


def main():
    console = Console()
    arguments = docopt(__doc__)
    si = arguments["<stdf_file_name_in>"]
    with _opener[si.split(".")[-1]](si, "rb") as f:
         while True:
                c = ams_rw_stdf.parse_record(f)
                console.print(str(c))
                if c.REC_TYP == 1 and c.REC_SUB == 20:
                     break


if __name__ == '__main__':
    main()
