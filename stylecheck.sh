#!/bin/bash

pushd "${VIRTUAL_ENV}/.." > /dev/null

source "${VIRTUAL_ENV}/bin/activate"

python -m black --line-length 100 diskspaced tests

python -m pylint --rcfile=pylintrc diskspaced tests

python -m mypy --ignore-missing-imports diskspaced/ tests/

popd > /dev/null

