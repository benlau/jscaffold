.PHONY: test
test:
	pytest -s

.PHONY: build_package
build_package:
	python setup.py sdist bdist_wheel

.PHONY: clean
clean:
	rm -rf build
	rm -rf lib
	rm -rf dist
	rm -rf *.egg-info

.PHONY: try-publish
try-publish:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: lint
lint:
	pylama jscaffold

.PHONY: lint-fix
lint-fix:
	black jscaffold
