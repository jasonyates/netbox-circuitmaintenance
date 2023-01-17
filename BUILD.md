
pip install bumpver build twine

bumpver update --minor
python -m build
twine upload -r testpypi dist/*
twine upload dist/*