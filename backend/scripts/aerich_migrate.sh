#!/bin/sh -e
set -x

(
  aerich migrate & pid=$! 
  sleep 2
  kill $pid || true
)
(
  aerich upgrade & pid=$! 
  sleep 2
  kill $pid || true
)