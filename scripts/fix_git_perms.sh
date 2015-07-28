cd /cygdrive/c/crs1906
chown -R user:Users .git
find .git -type d -exec chmod 755 {} ";"
find .git -type f -exec chmod 644 {} ";"
