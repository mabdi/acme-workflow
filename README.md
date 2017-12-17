# ACME-workflow
A sample vulnerable website for demo burp-workflow extension

Based on python3 and Flask

# Setting up

`pip3 install -r requirements.txt`

`rm -rf migrations`

`python3 manage.py db init`

`python3 manage.py db migrate`

`python3 manage.py db upgrade`

`python3 manage.py filldb`

`python3 run.py`

# Resources

UI from:

    https://codepen.io/ace-subido/pen/Cuiep

    https://codepen.io/ajaypatelaj/pen/zIBjJ

    https://codepen.io/jaycbrf/pen/iBszr
