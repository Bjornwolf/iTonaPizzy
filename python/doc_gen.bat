cd "$(FULL_CURRENT_PATH)"

cd docs_pro
sphinx-apidoc -o . ..
cmd /c "make.bat html"
