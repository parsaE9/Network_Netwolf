def remove_empty_lines(file_name):
    fh = open(file_name)
    lines = fh.readlines()
    fh.close()
    keep = []
    for line in lines:
        if not line.isspace():
            keep.append(line)
    fh = open(file_name, "w")
    fh.write("".join(keep))
    fh.close()
