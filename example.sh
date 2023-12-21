#!/usr/bin/env bash
#python QCGauntlet.py cpactivity -h

# python QCGauntlet.py \
# -c /Users/dterciano/Desktop/LokeyLabFiles/TargetMol/Datasets/TargetMol_PMA_histdiffpy_nometa_Concatenated.csv \
# -o out \
# -rc unambiguous_name longname_proper \
# -k "/Users/dterciano/Desktop/LokeyLabFiles/TargetMol/Annotations/L4000-Bioactive Compound Library-Beverley Rabbitts (KIT10006535)_MapCleaned3_KSready.csv" \
# -rc "unambiguous_name" "longname_proper" \
# cpactivity --activityTitles "PMA" "NoPMA" --controlTitles "PMA" "DMSO"

# python QCGauntlet.py \
# -c /Users/dterciano/Desktop/LokeyLabFiles/TargetMol/Datasets/TargetMol_PMA_histdiffpy_nometa_Concatenated_DEAD_DROPPED.csv \
# -ac /Users/dterciano/Desktop/LokeyLabFiles/TargetMol/Datasets/TargetMol_DMSO_histdiffpy_nometa_Concatenated.csv \
# -o out \
# -rc unambiguous_name longname_proper \
# -k "/Users/dterciano/Desktop/LokeyLabFiles/TargetMol/Annotations/L4000-Bioactive Compound Library-Beverley Rabbitts (KIT10006535)_MapCleaned3_KSready.csv" \
# -rc "unambiguous_name" "longname_proper" \
# cpactivity --activityTitles "PMA" "NoPMA" --controlTitles "DMSO" "PMA"

# python QCGauntlet.py \
# -c /Users/dterciano/Desktop/LokeyLabFiles/TargetMol/Datasets/TargetMol_PMA_histdiffpy_nometa_Concatenated_DEAD_DROPPED.csv \
# -ac /Users/dterciano/Desktop/LokeyLabFiles/TargetMol/Datasets/TargetMol_DMSO_histdiffpy_nometa_Concatenated.csv \
# -o out \
# -k "/Users/dterciano/Desktop/LokeyLabFiles/TargetMol/Annotations/L4000-Bioactive Compound Library-Beverley Rabbitts (KIT10006535)_MapCleaned3_KSready.csv" \
# -rc "unambiguous_name" "longname_proper" \
# controlCluster -r -ct DMSO PMA

# python QCGauntlet.py \
# -c /Users/dterciano/Desktop/LokeyLabFiles/TargetMol/Datasets/TargetMol_PMA_histdiffpy_nometa_Concatenated_DEAD_DROPPED.csv \
# -ac /Users/dterciano/Desktop/LokeyLabFiles/TargetMol/Datasets/TargetMol_DMSO_histdiffpy_nometa_Concatenated.csv \
# -o out \
# -k "/Users/dterciano/Desktop/LokeyLabFiles/TargetMol/Annotations/TargetMol_KSReady_updatedTargetsRENAMED.csv" \
# -rc "unambiguous_name" "longname_proper" \
# cntrlHist -ct PMA DMSO

# python QCGauntlet.py \
# -c /Users/dterciano/Desktop/LokeyLabFiles/TargetMol/Datasets/TargetMol_PMA_histdiffpy_nometa_Concatenated_DEAD_DROPPED.csv \
# -ac /Users/dterciano/Desktop/LokeyLabFiles/TargetMol/Datasets/TargetMol_DMSO_histdiffpy_nometa_Concatenated.csv \
# -o out \
# -k "/Users/dterciano/Desktop/LokeyLabFiles/TargetMol/Annotations/L4000-Bioactive Compound Library-Beverley Rabbitts (KIT10006535)_MapCleaned3_KSready.csv" \
# -rc "unambiguous_name" "longname_proper" \
# cntrlBarPlots -ct DMSO PMA -ds PMA noPMA

# python QCGauntlet.py \
# -c /Users/dterciano/Desktop/LokeyLabFiles/TargetMol/Datasets/TargetMol_PMA_histdiffpy_nometa_Concatenated_DEAD_DROPPED.csv \
# -o test \
# -ac /Users/dterciano/Desktop/LokeyLabFiles/TargetMol/Datasets/TargetMol_DMSO_histdiffpy_nometa_Concatenated.csv \
# -k "/Users/dterciano/Desktop/LokeyLabFiles/TargetMol/Annotations/TargetMol_KSReady_updatedTargetsRENAMED.csv" \
# -rc unambiguous_name longname_proper \
# cpactivity -at PMA noPMA -ct DMSO PMA
# best to use the renamed KS Ready sheet

# optional alternate Condition
# -ac /Users/dterciano/Desktop/LokeyLabFiles/TargetMol/Datasets/TargetMol_DMSO_histdiffpy_nometa_Concatenated.csv \

# python3 QCGauntlet.py -c "/mnt/c/Users/derfelt/Desktop/LokeyLabFiles/TargetMol/Datasets/10uM_HD_concats/TargetMol_10uM_PMA_batch2.csv" \
#     -ac "/mnt/c/Users/derfelt/Desktop/LokeyLabFiles/TargetMol/Datasets/10uM_HD_concats/TargetMol_10uM_NO_PMA_batch2.csv" \
#     -o "/mnt/c/Users/derfelt/Desktop/10uM_batch2" \
#     -t 1.5 -k "/mnt/c/Users/derfelt/Desktop/LokeyLabFiles/TargetMol/Annotations/10uMDummyAnnots.csv" \
#     -rc "well" "sample_type" \
#     cpactivity -at pma nopma -ct $(cat tm_controls.txt)

python3 QCGauntlet.py -c /mnt/c/Users/derfelt/Desktop/LokeyLabFiles/ImmunoCP/designerHD_concats/DMSO_longConcat_hd.csv \
    -ac /mnt/c/Users/derfelt/Desktop/LokeyLabFiles/ImmunoCP/designerHD_concats/LPS-DMSO_longConcat_hd.csv \
    -o "/mnt/c/Users/derfelt/Desktop/designer_LPS-DMSOvDMSO" \
    cpactivity -at dmso lps-DMSO -ct DMSO-cntrl LPS-cntrl
