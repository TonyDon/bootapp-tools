import os

photo_dir = r'C:\doc\photo\deskmap'
files = os.listdir(photo_dir)
index = 1
for f in files:
    fbn = os.path.basename(f)
    nfbn = '%02d.jpg' % (index)
    os.rename(os.path.join(photo_dir, fbn), os.path.join(photo_dir, nfbn))
    index +=1