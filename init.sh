#!/usr/bin/env bash

env_file=".env"
echo

sudo apt install -y python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
touch $env_file
{
  echo ;
  echo "# Edit lines below this ";
  echo "AWS_ACCESS_KEY_ID=";
  echo "AWS_SECRET_ACCESS_KEY=";
  echo "S3_ENDPOINT=";
  echo "REGION_NAME=";
  echo "BUCKET_NAME=";
  echo "SUCCESS_ACTION_REDIRECT_URL=";
  echo ;
} >> $env_file
echo -e "\e[32m.env file created, please edit it before run Flask"
echo -e "\033[0mRun in terminal: \e[32msource venv/bin/activate && flask run"

