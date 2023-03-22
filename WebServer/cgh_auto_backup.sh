#!/bin/bash
# tar --exclude='*/computations' --exclude='CanonicalCorrelationAnalysis' -zcvf ../WebServer_bkp_$(date '+%Y-%m-%d').tar.gz .
tar --exclude='*/computations' -zcvf ../WebServer_bkp_$(date '+%Y-%m-%d').tar.gz .
mv ../WebServer_bkp_$(date '+%Y-%m-%d').tar.gz /home/bscuser/Dropbox/Personal/Study/BSC/05_GraphCrunch3/code_backups/
# ls /home/bscuser/Dropbox/Personal/Study/BSC/05_GraphCrunch3/code_backups/
du -hd1 /home/bscuser/Dropbox/Personal/Study/BSC/05_GraphCrunch3/code_backups/*
