build:
	@python -m build

upload-pypi: build-package
	@python3 -m twine upload --repository testpypi dist/*