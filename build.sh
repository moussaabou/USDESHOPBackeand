#!/usr/bin/env bash
# Script يستخدمه Render لتجهيز المشروع

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
