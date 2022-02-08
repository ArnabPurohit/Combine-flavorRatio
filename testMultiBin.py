from func.tmpHandle import tmpHandle
from func.writeDatacards import writeDatacards
from func.getAccEffAndErr import getAccEffAndErr
from func.runCB import runCB
from plotting.plotNll import plotNll
from plotting.plotTmps import plotTmps
from plotting.plotImpact import plotImpact
from Parameters import sys_uncers
from func.getFrAndLimits import getFrAndLimits 
import os
import sys

#--floatOtherPOIs=1
def main():

    cardNames=[]
    cardNames_bb=[]
    cardNames_be=[]
    scanRange=(0.01, 10.)
    massCut=400
    Bngs=[200,300,400,500,690,900,1250,1610,2000,3500]
    FRmed={} 
    FRlow={}
    FRhigh={}
    #print("test run with mass cutoff "+str(massCut))
    for year in ["2016","2017","2018"]:
        for cg in ["bb","be"]:
            key=year+cg
            FRmed[key]=[]
            FRlow[key]=[]
            FRhigh[key]=[]
            cardName="ch"+year+cg+"_"+"multiBins"
            tmpName="tmp"+year+cg+"_"+"multiBins"
            #fileName="output"+year+cg+"_"+str(massCut)+"cut"
            fileName="testMultiBins"
            plotName="testMultiBins"
            cardNames.append(cardName)
            if cg=="bb":cardNames_bb.append(cardName)
            else: cardNames_be.append(cardName)
            Bngs1=Bngs+[-1]
            acc_eff={}
            for i in range(1, 11):
                acc_eff['S'+str(i)] = getAccEffAndErr(year, cg, Bngs1[i-1],Bngs1[i])
            tmps=tmpHandle(year, cg)
            tmps.createTmps(massCut, sys_uncers, massCutH=Bngs, isMultiBin=True)
            tmps.saveTmps(tmpName)
            writeDatacards(cardName, tmpName, year, cg, tmps.templates, acc_eff)
            cmd='text2workspace.py -P HiggsAnalysis.CombinedLimit.FRatioPerBinModel:FRatioPerBinModel datacards/%s.txt -o datacards/%s.root'%(cardName, cardName)
            os.system(cmd)
            continue
            for i in range(9,10):
                cmd="combine -M MultiDimFit --setParameters=r_bin1=1,r_bin2=1,r_bin3=1,r_bin4=1,r_bin5=1,r_bin6=1,r_bin7=1,r_bin8=1,r_bin9=1  -t -1 -m 125 --floatOtherPOIs=1  --algo=grid --points=1000 -P r_bin%s --setParameterRanges r_bin%s=0.01,10  --X-rtd MINIMIZER_analytic  datacards/%s.root"%(str(i),str(i),cardName)
                os.system(cmd)
                cmd="mv higgsCombineTest.MultiDimFit.mH125.root combineOutputs/testMultiBins.root"
                os.system(cmd)
                inputs={"result":fileName}
                plotNll(year, cg, massCut, False, plotName, i, **inputs)
                frs=getFrAndLimits(fileName,i)
                FRmed[key].append(str(frs[2]))
                FRhigh[key].append(str(frs[3]))
                FRlow[key].append(str(frs[1]))
    sys.exit()
    FRmed["allYearCombine"]=[]
    FRmed["allYearCombine_bb"]=[]
    FRmed["allYearCombine_be"]=[]    
    FRlow["allYearCombine"]=[]
    FRlow["allYearCombine_bb"]=[]
    FRlow["allYearCombine_be"]=[]
    FRhigh["allYearCombine"]=[]
    FRhigh["allYearCombine_bb"]=[]
    FRhigh["allYearCombine_be"]=[]
    for i in range(9,10):        
        runCB(scanRange, "allYearCombine_mulitBins", i, *cardNames)
        frs=getFrAndLimits("allYearCombine_mulitBins",i)
        inputs={"result":"allYearCombine_mulitBins"}
        plotNll("all", "all", massCut, False, "allYearCombine_mulitBins", i, **inputs)
        FRmed["allYearCombine"].append(str(frs[2]))
        FRhigh["allYearCombine"].append(str(frs[3]))
        FRlow["allYearCombine"].append(str(frs[1]))
        runCB(scanRange, "allYearCombine_mulitBins_bb", i, *cardNames_bb)
        inputs={"result":"allYearCombine_mulitBins_bb"}
        plotNll("all", "bb", massCut, False, "allYearCombine_mulitBins", i, **inputs)
        frs=getFrAndLimits("allYearCombine_mulitBins_bb",i)
        FRmed["allYearCombine_bb"].append(str(frs[2]))
        FRhigh["allYearCombine_bb"].append(str(frs[3]))
        FRlow["allYearCombine_bb"].append(str(frs[1]))
        runCB(scanRange, "allYearCombine_mulitBins_be", i, *cardNames_be)
        inputs={"result":"allYearCombine_mulitBins_be"}
        plotNll("all", "be", massCut, False, "allYearCombine_mulitBins", i, **inputs)
        frs=getFrAndLimits("allYearCombine_mulitBins_be",i)
        FRmed["allYearCombine_be"].append(str(frs[2]))
        FRhigh["allYearCombine_be"].append(str(frs[3]))
        FRlow["allYearCombine_be"].append(str(frs[1]))
    
    print(FRlow)
    print(FRmed)
    print(FRhigh)
if __name__=="__main__":
    main()
