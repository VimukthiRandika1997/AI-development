#!/bin/bash

rm -r alembic || true
alembic init alembic
cp -r alembic_/* alembic