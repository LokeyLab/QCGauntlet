# QCGauntlet
## A quality control tool (for CP3) that analyzes 1 or 2 conditions of a given dataset
#### Written and created by Derfel Terciano

***
## Description:
This python program generates analytical figures that help determine the quality of experiments. This program can generate the following visuals:
- Scatter plots of CP Activity Scores (with threshold lines) *NOTE: works only with two conditions)*
- Elbow plots of CP Activity scores (with threshold lines)
- Clustermap files for Java TreeView
- Histograms for control condition correlations
- Barplots of CP Activity control wells that are over a threshold.

***By default***: thresholds are set to 0.5
***

## Usage/Help
The following are help prompts from the program that describe how to use the program:

    usage: python QCGauntlet.py [command] [arg] [subparser] ...

    A CLI program that processes datasets and analyzes the quality of it.

    options:
    -h, --help            show this help message and exit
    -c [MAINCOND], --mainCond [MAINCOND]
                            File location/path for the main condition or first
                            condition of the dataset (must be a .csv file)
    -ac [ALTERNATECOND], --alternateCond [ALTERNATECOND]
                            (optional) File location/path ofr the second/alternate
                            condition of the dataset (must be a .csv file if used)
    -o [OUTPUT], --output [OUTPUT]
                            A string title for the output files (file extensions
                            will be automatically handled)
    -t [THRESHOLD], --threshold [THRESHOLD]
                            Sets the threshold value for analysis. (default: 0.5)
    -indCol INDEXCOLUMN [INDEXCOLUMN ...], --indexColumn INDEXCOLUMN [INDEXCOLUMN ...]
                            Specifies what the index column is in all the datasets
                            (annotation sheet/plate maps don't count)
    -k [KEYFILE], --keyFile [KEYFILE]
                            Input path/location of annotation sheet/plate map
                            (optional)//Use this only if you want to rename the
                            wells in the dataset [Warning: certain analytical
                            tools may require that this parameter is used]
    -rc RENAMECOLUMNS RENAMECOLUMNS, --renameColumns RENAMECOLUMNS RENAMECOLUMNS
                            If the -k parameter is used then it is highly
                            recommended that you use this parameter which is in
                            the order of column that specifies wells and then
                            column of their renamed values

    Gauntlet Analysis:
    {cpactivity,controlCluster,cntrlHist,cntrlBarPlots}
        cpactivity          Activates cp Activity Score analysis and generates
        controlCluster      Activates clustermap generation of controls
        cntrlHist           Activates histogram generation of the distribution of
                            control correlations
        cntrlBarPlots       Activates generation of controls over threshold in the
                            form of barplots

`cpactivity` help prompt:

    usage: python QCGauntlet.py [command] [arg] [subparser] ... cpactivity
        [-h] [-s [SEP]] [-pi [PLATELABELINDEX]]
        [-at ACTIVITYTITLES ACTIVITYTITLES] [-ct CONTROLTITLES CONTROLTITLES]

    options:
    -h, --help            show this help message and exit
    -s [SEP], --sep [SEP]
                            Determines the seperator/delimiter used to " "split
                            text into their plates (default: "._.")
    -pi [PLATELABELINDEX], --plateLabelIndex [PLATELABELINDEX]
                            After seprating the index labels by the sep command,
                            what index are the plate labels on? (def: -1)
    -at ACTIVITYTITLES ACTIVITYTITLES, --activityTitles ACTIVITYTITLES ACTIVITYTITLES
                            titles of scores calculated in order of -c then -ac
                            params (if -ac is used)
    -ct CONTROLTITLES CONTROLTITLES, --controlTitles CONTROLTITLES CONTROLTITLES
                            List of control titles/labels (i.e. DMSO PMA)

`controlCluster` help:

    usage: python QCGauntlet.py [command] [arg] [subparser] ... controlCluster
        [-h] [-s [SEP]] [-r] [-c] [-ct CONTROLTITLES CONTROLTITLES]
        [-pi [PLATELABELINDEX]]

    options:
    -h, --help            show this help message and exit
    -s [SEP], --sep [SEP]
                            Determines the seperator/delimiter used to " "split
                            text into their plates (default: "._.")
    -r, --rowCLuster      Toggles row clustering (default: True)
    -c, --colCLuster      Toggles column clustering (default: True)
    -ct CONTROLTITLES CONTROLTITLES, --controlTitles CONTROLTITLES CONTROLTITLES
                            List of control titles/labels (i.e. DMSO PMA)
    -pi [PLATELABELINDEX], --plateLabelIndex [PLATELABELINDEX]
                            After seprating the index labels by the sep command,
                            what index are the plate labels on? (def: -1)

`cntrlHist` help:

    usage: python QCGauntlet.py [command] [arg] [subparser] ... cntrlHist
        [-h] [-ct CONTROLTITLES CONTROLTITLES] [-pi [PLATELABELINDEX]]
        [-s [SEP]]

    options:
    -h, --help            show this help message and exit
    -ct CONTROLTITLES CONTROLTITLES, --controlTitles CONTROLTITLES CONTROLTITLES
                            List of control titles/labels (i.e. DMSO PMA)
    -pi [PLATELABELINDEX], --plateLabelIndex [PLATELABELINDEX]
                            After seprating the index labels by the sep command,
                            what index are the plate labels on? (def: -1)
    -s [SEP], --sep [SEP]
                            Determines the seperator/delimiter used to " "split
                            text into their plates (default: "._.")

`cntrlBarPlots` help:

    usage: python QCGauntlet.py [command] [arg] [subparser] ... cntrlBarPlots
        [-h] -ds DATASETLABEL DATASETLABEL [-ct CONTROLTITLES CONTROLTITLES]
        [-pi [PLATELABELINDEX]] [-s [SEP]]

    options:
    -h, --help            show this help message and exit
    -ds DATASETLABEL DATASETLABEL, --datasetLabel DATASETLABEL DATASETLABEL
                            Specifies what to name figure from the dataset name
                            (i.e. PMA plate) if 2 conditions are inputted, then
                            the arguments could be: name for -c then name for -ac
    -ct CONTROLTITLES CONTROLTITLES, --controlTitles CONTROLTITLES CONTROLTITLES
                            List of control titles/labels (i.e. DMSO PMA)
    -pi [PLATELABELINDEX], --plateLabelIndex [PLATELABELINDEX]
                            After seprating the index labels by the sep command,
                            what index are the plate labels on? (def: -1)
    -s [SEP], --sep [SEP]
                            Determines the seperator/delimiter used to " "split
                            text into their plates (default: "._.")

**TODO/Task List:**

- [x] Re-Write cpActivityScores.py &rarr; cpActivityScoresV2.py
- [x] Differentiate between 1 or 2 conditions for cpActivityScoresV2.py
- [x] Re-Write controlPlates.py to be more efficient and automatically seperates plates (using the new and improved process).
- [x] Find ways to improve controlCorr.py (I may not even touch it at all)
- [x] Write out command line (QCGauntlet.py)
    - [x] Implement cpActivityScores (scatter plot bundle)
    - [x] Implement control Clustering (Java TreeView files)
    - [x] Implement histograms for controls
    - [x] Implement bar plots for controls over threshold

**Future Tasks**
- [x] Write a GUI (using tkinter/gooeyparse)
    - This will ultimately make it easier for others to use and not only the informaticist avaliable at hand

***
# QCGauntletApp.py
***
## A quality control front end tool (for CP3) that analyzes 1 or 2 conditions of a given dataset
#### Written and created by Derfel Terciano

This is the front end version of QCGauntlet, all input fields mimic the command line options given in QCGauntlet.py.

***Note:*** This is currently only avaliable for MacOS