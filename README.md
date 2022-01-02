# find_duplicate_folders
Analyze a file tree, looking for folders whose files are all duplicated elsewhere.

Use case:
I've imported stacks of CDs of pictures.  Sometimes I reorganized the files/folders.  Some CDs were "originals" some were probably backups.  Some might be a mixture of new images + older images.  A hodge-podge.  I figured it would be easier to write a script to look for duplicate imports rather than to analyze each CD by hand.

So, now it's time to put that theory to the test.

fdupes kinda does this, but on a file-by-file basis.  It will choose duplicates to remove.  But, no guarantees that it won't pick alternate files from duplicate folders A and B, leaving a partial coverage in folder.  I want a script that reports the A/B duplication, and lets me choose the keeper.

Approach:
 * I have a folder of sha1 hashes of all files, with the full path
 * step 1: for each leaf folder, make an aggregate hash.  Report on duplicate hashes.   Remove both folders from future consideration.
 * step 2: for each leaf folder, determine if each file is present in someother folder.  If all files are accounted for, report the folder, and the alternate file locations.  This will find the case where a folder has be reorganized on import.
