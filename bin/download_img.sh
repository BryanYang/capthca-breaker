#!/bin/bash


folder="origin6"
num=50

#如果文件夹不存在，创建文件夹
if [ ! -d $folder ]; then
  mkdir $folder
fi

for ((i=1; i<=$num; i++))
do
  curl -o $folder/$i.jpeg http://alitest.e.fanxiaojian.cn/metis-login-web/captcha\?captchaKey\=45165vjvdfggce8b
done