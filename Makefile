# Install all development dependencies
#
.PHONY: init-deps-dev
init-deps-dev:
	pip install -U pip
	pip install -r requirements-dev.txt

# Install all dependencies in venv
.PHONY: init-deps
init-deps:
	pip install -r requirements.txt

# Run mysql db in daemon mode
.PHONY: test-containers
test-containers:
	@docker run --platform linux/amd64 --rm --name minio -p 9000:9000 -p 9001:9001  -d minio/minio server /data --console-address :9001


.PHONY: clean-test-containers
clean-test-containers:
	@docker stop minio || echo "stopped any containers left running"


# Run the unit tests
.PHONY: test
test: fmt fmt-check sort type testdata
	PYTHONPATH=./src coverage run --source src -m pytest -o junit_family=xunit1 --junitxml=test-results/junit.xml tests
	coverage report --fail-under 70
	coverage xml -o test-results/coverage.xml

.PHONY: testdata
testdata:
	cd tests/testdata && unzip creditcard.csv.zip

# Format code
.PHONY: fmt
fmt:
	black --exclude "venv|.venv" .

.PHONY: fmt-check
fmt-check:
	black --check --exclude "venv|.venv" .


.PHONY: sort
sort:
	isort .

.PHONY: type
type:
	mypy src

.PHONY: venv
venv:
	python -m venv .venv
