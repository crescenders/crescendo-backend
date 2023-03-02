pip freeze >> tmp.txt
pip uninstall -r tmp.txt -y
rm tmp.txt
pip install -r requirements/dev.txt