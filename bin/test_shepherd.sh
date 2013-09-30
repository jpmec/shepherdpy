(cd ../shepherdpy && python -m unittest discover)

output=$(cd ../shepherdpy && python -m unittest discover 2>&1 | tail -1)

diff <(echo $output) <(echo 'OK')
