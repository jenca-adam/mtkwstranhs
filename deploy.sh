#!/usr/bin/env bash
# vim: et ts=4 sw=4 ai

systemctl stop prvocisla

CODEDIR=/data/www/prvocisla

rm -r "$CODEDIR" 
mkdir -pv "$CODEDIR"

cp -rvf static "$CODEDIR"
cp -rvf templates "$CODEDIR"
cp -rvf pics "$CODEDIR"
cp -rvf *.py "$CODEDIR"
sed -i "s@sqlite:///sg.db@sqlite:///$CODEDIR/sg.db@" "$CODEDIR/setup.py"
find "$CODEDIR" -name '*.pyc' -exec rm -v {} \;
find "$CODEDIR" -name '*~' -exec rm -v {} \;
chmod -v -R u=rX,g=,o= "$CODEDIR"
find  "$CODEDIR" -type d -exec chmod -v u+w {} \;
(
cd $CODEDIR
python3 sg.py
chmod u+w sg.db
)
chown -Rv www-data:www-data "$CODEDIR"

sleep 1
systemctl start prvocisla
