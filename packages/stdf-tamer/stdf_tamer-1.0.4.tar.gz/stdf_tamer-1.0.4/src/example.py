import ams_rw_stdf_writer
import random

ams_rw_stdf_writer.load_limit_file("limits.xlsx")
f = ams_rw_stdf_writer.start_stdf_file("experiment2.stdf.bz2")
for id in range(20):
    ams_rw_stdf_writer.start_sample(f)
    ams_rw_stdf_writer.test_value_between(f, 1001, "example_test", random.random())
    ams_rw_stdf_writer.test_value_between(f, 1002, "example_test2", random.random()*10)
    ams_rw_stdf_writer.finish_sample(f, str(id))

#ams_rw_stdf_writer.finish_stdf_file(f)
