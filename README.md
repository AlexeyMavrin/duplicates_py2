# Duplicates

The "Duplicates" is a tool for convenient duplicate files removal.
"Duplicates" is just a wrapper over awesome duplicate search tool "https://github.com/michaelkrisper/duplicate-file-finder". So far this is the fastest and most reliable duplicate finder tool I've seen.

The primary problem is removing the duplicates from the specified directories only and keeping other folders intact (even if there are duplicates there too). 

For example when getting a bunch of new photos removing the duplicates only from the new files, but never from the photos library.

The "Duplicates" removes files only in work directory (always keep one copy if all duplicates under work folder). The golden directory used to search for duplicates, however, no files deleted there.

## Usage

Searches for duplicates in both folders but remove duplicated files from **new_pics** only. Nothing deleted in **my_photos_library**
```sh
duplicates --work new_pics --golden my_photos_library --purge
```

Remove duplicates under the folder (keep one copy only)
```sh
duplicates --work work  --purge    
```

Find and print duplicates only (sorted by file size - largest first). Delete nothing.
```sh
duplicates --work work 
```

## Install

Get the source code, go to duplicates directory and run
```sh
git clone https://github.com/AlexeyMavrin/duplicates.git
cd duplicates
python setup.py install
python setup.py test
```

## TODO
Allow multiple work directories at the same time
