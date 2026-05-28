@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
cd /d "C:\Users\Administrator\.openclaw-autoclaw\workspace\scripts"
python hailuo_test.py > "C:\Users\Administrator\.openclaw-autoclaw\media\hailuo_test_log.txt" 2>&1
