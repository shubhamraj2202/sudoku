@echo off
echo ------------------------------------------------------------------------------
echo ======================INSTALATION BEGINS======================================
echo ------------------------------------------------------------------------------
python -m pip install -r requirements.txt

echo ------------------------------------------------------------------------------
echo =======================TEST CASES STARTS======================================
echo ------------------------------------------------------------------------------

python -m nose2 -v
pause