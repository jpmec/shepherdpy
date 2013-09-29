output=$(python test_shepherd.py 2>&1 | tail -1)

diff <(echo $output) <(echo 'OK')
