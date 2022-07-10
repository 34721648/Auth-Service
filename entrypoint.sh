#!/bin/bash
cd src
flask db upgrade
python app.py