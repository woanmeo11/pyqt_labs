#!/bin/bash
gunicorn --config python:config app:app
