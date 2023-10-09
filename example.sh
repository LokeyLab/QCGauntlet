#!/usr/bin/env bash
#python QCGauntlet.py cpactivity -h

# python QCGauntlet.py \
# -c /Users/dterciano/Desktop/LokeyLabFiles/TargetMol/Datasets/TargetMol_PMA_histdiffpy_nometa_Concatenated.csv \
# -o out \
# -rc unambiguous_name longname_proper \
# -k "/Users/dterciano/Desktop/LokeyLabFiles/TargetMol/Annotations/L4000-Bioactive Compound Library-Beverley Rabbitts (KIT10006535)_MapCleaned3_KSready.csv" \
# -rc "unambiguous_name" "longname_proper" \
# cpactivity --activityTitles "PMA" "NoPMA" --controlTitles "PMA" "DMSO"

python QCGauntlet.py \
-c /Users/dterciano/Desktop/LokeyLabFiles/TargetMol/Datasets/TargetMol_PMA_histdiffpy_nometa_Concatenated_DEAD_DROPPED.csv \
-ac /Users/dterciano/Desktop/LokeyLabFiles/TargetMol/Datasets/TargetMol_DMSO_histdiffpy_nometa_Concatenated.csv \
-o out \
-rc unambiguous_name longname_proper \
-k "/Users/dterciano/Desktop/LokeyLabFiles/TargetMol/Annotations/L4000-Bioactive Compound Library-Beverley Rabbitts (KIT10006535)_MapCleaned3_KSready.csv" \
-rc "unambiguous_name" "longname_proper" \
cpactivity --activityTitles "PMA" "NoPMA" --controlTitles "DMSO" "PMA"
