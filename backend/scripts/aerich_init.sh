#!/bin/sh -e
set -x

aerich init -t app.database.TORTOISE_ORM
(
  aerich init-db & pid=$! 
  sleep 2
  kill $pid || true
)
