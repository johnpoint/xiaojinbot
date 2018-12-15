# xiaojinbot

clone 本项目
cd xiaojinbot/
cp jinbot.service /lib/systemd/system/

systemctl daemon-reload
systemctl enable expressbot.service

service jinbot start
