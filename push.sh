#!/bin/bash
cp /root/.openclaw/workspace/index.html /root/.openclaw/workspace/kiloclaw-webapps/
cd /root/.openclaw/workspace/kiloclaw-webapps
git add -A
git commit -m "Client-side today highlighting (timezone-aware)"
git push
