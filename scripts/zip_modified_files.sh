#!/usr/bin/bash
# Zip modified .py and .ini files from the /crs1906/exercises directory

zipFile='C:\crs1906\modified_python_exercises.zip'
fileList='modified_1906_files.txt'

echo 'Zipping all .py and .ini files modified this week...'

cd /c

find crs1906/exercises -not -path '*/*venv*/*' -not -path '*/.idea/*' -mtime -5 \( -name '*.py' -o -name '*.ini' \) | sed 's#^#/#' > /c/crs1906/$fileList

'C:\Program Files\7-Zip\7z.exe' a -tzip -spf2 "$zipFile" @'C:\crs1906\'$fileList > /dev/null

rm "/c/crs1906/$fileList"

cat <<!

Done. Your modified files were zipped to $zipFile
Upload the zip file to the cloud or email it to yourself.
When you come back to the Computing Sandbox, download the zip file and extract it to C:\\

!
echo -n "Press <Enter> to continue: "
read line