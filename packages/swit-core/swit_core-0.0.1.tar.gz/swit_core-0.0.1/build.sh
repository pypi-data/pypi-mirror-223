rm -rf dist/*

set -e

./run_tests.sh
python3 -m build
python3 -m twine upload dist/*