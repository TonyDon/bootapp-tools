import os

sts_plugins_dir = r'C:\app\sts4\plugins'
files = os.listdir(sts_plugins_dir)
file_dict = dict()
remove_file_dict = dict()
for f in files:
    curr_f = os.path.join(sts_plugins_dir, f)
    f_st = os.stat(curr_f)
    if os.path.isfile(curr_f):
        f_mtime = f_st.st_mtime
        f_parts_split_char_idx = f.rindex('_')
        f_part_name = f[:f_parts_split_char_idx]
        f_part_verion = f[f_parts_split_char_idx+1:]
        f_mate = (f_mtime, f_part_name, f_part_verion)
        meta = file_dict.get(f_part_name)
        if meta is None :
            file_dict[f_part_name] = f_mate
        elif meta < f_mate :
            file_dict[f_part_name] = f_mate
            remove_file_dict[f_part_name] = meta[1]+"_"+meta[2]
            
sts_plugins_mv = r'C:\sts-plugis\v'
for k,v in remove_file_dict.items():
    print(v)
    os.rename(os.path.join(sts_plugins_dir, v), os.path.join(sts_plugins_mv, v))   

input("pause...")