@echo off
echo Writing modified Python files to C:\crs1906\modified_exercises.zip
"C:\software\Git\bin\bash" -c "cd /c/crs1906; find exercises -not -path '*/venv/*' -not -path '*/.idea/*' -mtime -4 -name '*.py' -exec 'C:\Program Files\7-Zip\7z.exe' a -r -tzip -spf2 'C:\crs1906\modified_exercises.zip' {} \; > /dev/null"
