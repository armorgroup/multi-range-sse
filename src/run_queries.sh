#!/bin/bash
# Construct the databases, indexes, and shuffling shcemes
echo "Constructing databases, indexes, and shuffling schemes..."
python3 src/construction.py
echo "Successfully constructed databases, indexes, and shuffling schemes."

echo "Temporary files are being removed..."

# Run query shapes sequentially
python3 src/isoqreport.py
python3 src/baqreport.py
python3 src/gaqreport.py
python3 src/oaqreport.py -ot max
python3 src/oaqreport.py -ot min

echo "All scripts executed successfully."
