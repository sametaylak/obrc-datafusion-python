import sys
import numpy as np

from datafusion import SessionContext, col, lit
from datafusion import functions as f

ctx = SessionContext()

station_col = col('column_1')
temp_col = col('column_2')
min_col = f.min(temp_col).alias('min')
mean_col = f.mean(temp_col).alias('mean')
max_col = f.max(temp_col).alias('max')

df = ctx.read_csv(
    './measurements-100000.txt',
    delimiter=';',
    has_header=False,
    file_extension='.txt'
)

aggregated_df = df.aggregate(
    [station_col],
    [min_col, mean_col, max_col],
).sort(
    station_col.sort()
).select(
	f.concat_ws(
		'=',
		col('column_1'),
		f.concat_ws(
	    	'/',
	    	col('min'),
	    	f.trunc(col('mean'), lit(1)).alias('mean'),
	    	col('max')
	    )
	),
)

sys.stdout.write('{')
aggregated_list = aggregated_df.to_pylist()
for k, v in enumerate(aggregated_list):
	measurement = list(v.values())[0]
	sys.stdout.write(measurement)

	if k != len(aggregated_list) - 1:
		sys.stdout.write(', ')
sys.stdout.write('}')
