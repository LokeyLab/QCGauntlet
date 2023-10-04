import Bio.Cluster as pycluster, pandas as pd, numpy as np
import matplotlib.pyplot as plt, seaborn as sns
import os, shutil, subprocess, sys

def pyclusterHeatmap_pearsonComplete(inTabFile, outname, rowCluster = True, colCluster = True):
    record = pycluster.read(open(inTabFile))
    genetree, exptree = None, None
    if rowCluster:
        genetree = record.treecluster(method='m',dist='c',transpose=0)
        genetree.scale()

    if colCluster:
        exptree = record.treecluster(method='m',dist= 'c',transpose=1)
        exptree.scale()

    # genetree.scale()
    # exptree.scale()
    record.save(outname,genetree,exptree)

def renameKeys(mainDf: pd.DataFrame, keyDf: pd.DataFrame, renameColumn) -> pd.DataFrame:
    mergeDf = pd.merge(mainDf, keyDf, left_index=True, right_index=True, how='left', sort=False).copy()
    mergeDf.index = mergeDf[renameColumn]
    mergeDf = mergeDf.drop(renameColumn, axis=1, inplace=False)
    return mergeDf

class CreateClusterFiles:
    def __init__(self, 
            inDf: pd.DataFrame, 
            annotFile: pd.DataFrame, 
            splitBy: str, 
            numPlates: int, 
            reps = None, 
            excludePlates: list = None, 
            indexCol = None, 
            cntrlOnly = False, 
            controlLabels = ['DMSO._.0', 'PMA._.0']):

        self.inDf = inDf
        self.annotFile = annotFile
        self.splitBy = splitBy
        self.numPlates = numPlates
        self.reps = reps
        self.excludePlates = excludePlates
        self.indexCol = indexCol
        self.cntrlOnly = cntrlOnly
        self.controlLabels = controlLabels

        self.plateNames = [f'{self.splitBy}_{str(i).zfill(2)}_rep1' for i in range(1, self.numPlates+1)]

        if self.reps is not None:
            repNames = [f'{self.splitBy}_{str(i).zfill(2)}_rep2' for i in self.reps]
            self.plateNames.extend(repNames)
        
        if excludePlates is not None:
            self.plateNames = list(set(self.plateNames) - set(self.excludePlates))

    def __delete_directory_contents(self, directory_path):
        try:
            # Delete all items (files and subfolders) within the directory
            for item in os.listdir(directory_path):
                item_path = os.path.join(directory_path, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)

            # Delete the empty directory itself
            os.rmdir(directory_path)

        except Exception as e:
            print(f"An error occurred: {e}")
    
    def __renameKeys(self, mainDf: pd.DataFrame, keyDf: pd.DataFrame, renameColumn) -> pd.DataFrame:
        mergeDf = pd.merge(mainDf, keyDf, left_index=True, right_index=True, how='left', sort=False).copy()
        mergeDf.index = mergeDf[renameColumn]
        mergeDf = mergeDf.drop(renameColumn, axis=1, inplace=False)
        return mergeDf

    def __pyclusterHeatmap_pearsonComplete(self, inTabFile, outname, rowCluster = True, colCluster = True):
        record = pycluster.read(open(inTabFile))
        genetree, exptree = None, None
        if rowCluster:
            genetree = record.treecluster(method='m',dist='c',transpose=0)
            genetree.scale()

        if colCluster:
            exptree = record.treecluster(method='m',dist= 'c',transpose=1)
            exptree.scale()

        # genetree.scale()
        # exptree.scale()
        record.save(outname,genetree,exptree)

    def createTempFiles(self) -> None:
        try:
            os.mkdir('.temp')
        except:
            self.__delete_directory_contents('.temp')
            os.mkdir('.temp')
        
        for name in self.plateNames:

            if self.indexCol is None:
                currDf = self.inDf[self.inDf.index.str.contains(name)]
            else:
                currDf = self.inDf[self.inDf.iloc[:,self.indexCol].str.contains(name)]
            
            currDf = self.__renameKeys(mainDf=currDf, keyDf=self.annotFile, renameColumn='longname_proper')
            if self.cntrlOnly:
                currDf = currDf[currDf.index.str.contains('|'.join(self.controlLabels))]
            else:
                currDf = currDf[~currDf.index.str.contains('|'.join(self.controlLabels))]

            currDf.to_csv(path_or_buf=f'.temp/{name}.tsv', sep='\t')

        return

    def generateFiles(self, folderName: str, rowCluster = True, colCluster = True):

        # generate Temp files first
        self.createTempFiles()

        # create folder to hold data
        try:
            os.mkdir(folderName)
        except:
            self.__delete_directory_contents(folderName)
            os.mkdir(folderName)
        
        numFiles = len(os.listdir('.temp/'))
        # do through each plate and generate cluster files for each
        for i, file in enumerate(os.listdir('.temp/')):
            name = file.split('.')[0]
            path = os.path.join('.temp/',file)

            print(f'generating cluster files for: {name} ({i+1}/{numFiles})', file=sys.stderr)

            # create sub folders for each plate (3 files will typically be produced)
            currFolder = f'{folderName}/{name}'
            try:
                os.mkdir(currFolder)
            except:
                self.__delete_directory_contents(currFolder)
                os.mkdir(currFolder)
            
            self.__pyclusterHeatmap_pearsonComplete(inTabFile=path, outname=f'{currFolder}/{name}', rowCluster=rowCluster, colCluster=colCluster)
        
        #clean up
        self.__delete_directory_contents('.temp/')
        
        return

    def generateThresholdStats(self, outname: str, threshold = 0.5):

        def calculateScore(df: pd.DataFrame, axis = 1):
            return df.apply(lambda x: np.sqrt(np.sum(np.square(x))), axis=axis)

        #generate Temp files
        self.createTempFiles()

        calcResults = {
            'Control': [],
            'Count': [],
            'Percentage': []
        }
        for file in os.listdir('.temp/'):
            name = file.split('.')[0]
            path = os.path.join('.temp/', file)

            df = pd.read_csv(path, sep='\t', index_col=0)
            df = calculateScore(df=df)
            df.name = 'scores'

            totalCntrls = len(df)
            df = df[(df >= threshold)]

            calcResults['Control'].append(name)
            calcResults['Count'].append(len(df))
            calcResults['Percentage'].append(len(df)/totalCntrls)
        
        results = pd.DataFrame(data=calcResults).set_index('Control')
        results.to_csv(f'{outname}.tsv', sep='\t')

        results.sort_index(inplace=True)
        fig, ax = plt.subplots(figsize=(16,9))
        sns.barplot(data=results, x=results.index, y='Percentage', ax=ax)

        ax.set_title(f'Percent of controls above threshold : {threshold}', fontsize = 14)
        ax.set_xticklabels(ax.get_xticklabels(),rotation=45,size=12,ha='right', rotation_mode='anchor')
        ax.set_xlabel('Plate')
        for p in ax.patches:
            height = p.get_height()
            # ax.annotate(f'{(height/countTotal)*100:0.1f}%', (p.get_x() + p.get_width() / 2., height),\
            #             ha='center', va='bottom', fontsize = 5)
            ax.annotate(f'{height*100:0.1f}%', (p.get_x() + p.get_width() / 2., height),\
                        ha='center', va='bottom', fontsize = 8)

        fig.tight_layout()
        fig.savefig(f'{outname}.pdf', format='pdf', dpi = 320)
        plt.close(fig=fig)

        #clean up files
        self.__delete_directory_contents('.temp/')
