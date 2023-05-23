#!/bin/bash

# Python 3.10 설치
sudo apt update
sudo apt install -y python3.10

# 가상 환경 생성 및 활성화
python3.10 -m venv .venv
source .venv/bin/activate

# requirements.txt 설치
pip install -r requirements.txt

# 스크립트 종료 후 가상 환경 비활성화
deactivate
