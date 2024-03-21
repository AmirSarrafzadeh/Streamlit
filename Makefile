run:
	@echo "Running the program"
	pip freeze > requirements.txt
	git add .
	git commit -m "Updated the script"
	git push