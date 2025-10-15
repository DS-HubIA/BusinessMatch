#!/bin/bash
mkdir -p status
cp status/status_continuacao.json "status/backup_status_$(date +%H%M).json"
echo "✅ Backup criado em status/"
