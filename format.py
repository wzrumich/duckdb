#!/usr/bin/python

import os, time

last_format_file = '.last_format'
cpp_format_command = 'clang-format -i -sort-includes=${SORT_INCLUDES} -style=file "${FILE}"'
sql_format_command = 'pg_format "${FILE}" -o "${FILE}.out" && mv "${FILE}.out" "${FILE}"'
extensions = ['.cpp', '.c', '.hpp', '.h', '.cc', '.hh', '.sql']

format_commands = {
	'.cpp': cpp_format_command,
	'.c': cpp_format_command,
	'.hpp': cpp_format_command,
	'.h': cpp_format_command,
	'.hh': cpp_format_command,
	'.cc': cpp_format_command,
	'.sql': sql_format_command,
}
# get the last time this command was run, if ever

last_format_time = 0

if os.path.exists(last_format_file):
	with open(last_format_file, 'r') as f:
		try:
			last_format_time = float(f.read())
		except:
			pass


if last_format_time > 0:
	print('Last format: %s' % (time.ctime(last_format_time)))


time.ctime(os.path.getmtime('tools/sqlite3_api_wrapper/include/sqlite3.h'))

def format_directory(directory, sort_includes=True):
	directory_printed = False
	files = os.listdir(directory)
	for f in files:
		full_path = os.path.join(directory, f)
		if os.path.isdir(full_path):
			format_directory(full_path)
		else:
			# don't format TPC-H constants
			if 'tpch_constants.hpp' in full_path:
				continue
			for ext in extensions:
				if f.endswith(ext):
					if os.path.getmtime(full_path) > last_format_time:
						format_command = format_commands[ext]
						if not directory_printed:
							print(directory)
							directory_printed = True
						cmd = format_command.replace("${FILE}", full_path).replace("${SORT_INCLUDES}", "1" if sort_includes else "0")
						print(cmd)
						os.system(cmd)
					break

format_directory('src')
format_directory('test')
format_directory('third_party/dbgen')
format_directory('third_party/sqlsmith', False)
format_directory('tools')

# write the last modified time
with open(last_format_file, 'w+') as f:
	f.write(str(time.time()))
