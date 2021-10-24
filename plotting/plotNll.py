import ROOT
from math import log
import root_numpy
import numpy as np
from Parameters import lumi_el, lumi_mu

def plotNll(year, cg, massCut, isLabel, output, **rootFiles):
	
    ROOT.gStyle.SetOptStat(0)
    count=0
    histDict={}
    
    for label, rootFile in rootFiles.items():
        count+=1
        f1=ROOT.TFile.Open("combineOutputs/"+rootFile+".root","r")
        tree=f1.Get("limit")
        nllCombine=root_numpy.tree2array(tree,"deltaNLL")
        rCombine=root_numpy.tree2array(tree,"r") 
        Max=np.max(rCombine)
        
        Min=np.min(rCombine)
        
        r=np.linspace(Min, Max,1000)
        histDict[label]=ROOT.TH1D("hist"+str(count), year+" "+cg+" masscut "+str(massCut)+" GeV", len(r)-1, r)
        histDict[label].GetXaxis().SetTitle('flavor ratio')
        histDict[label].GetYaxis().SetTitle('-2#Delta lnL')
        histDict[label].SetLineColor(count+1)
        for i in range(1,len(nllCombine)): 
             
            if nllCombine[i]>0: histDict[label].SetBinContent(i,nllCombine[i])
            else: histDict[label].SetBinContent(i,0)
        histDict[label].GetYaxis().SetRangeUser(0.0,25)
        histDict[label].SetDirectory(0)
        tree.SetDirectory(0)
        f1.Close()
    ly = ROOT.TLegend(0.65, 0.7, 0.9, 0.9)
    c=ROOT.TCanvas("c","c",800,800)
    count=0

    for key in histDict.keys():

        count+=1
        if count==1: histDict[key].Draw("hist")
        else: histDict[key].Draw("samehist")
        ly.AddEntry(histDict[key], key)  

    if isLabel: ly.Draw()

    treLine = ROOT.TLine(Min, 1.0, Max, 1.0)
    treLine.SetLineStyle(2)
    treLine.Draw()
    latexCMS = ROOT.TLatex()
    latexCMS.SetTextFont(61)
    latexCMS.SetNDC(True)
    latexCMS.SetTextSize(0.04)
    latexCMS.DrawLatex(0.13,0.85,"CMS")
    latexCMS.DrawLatex(0.13,0.8,"Work in progress")
    latex = ROOT.TLatex()
    latex.SetTextFont(42)
    latex.SetTextAlign(31)
    latex.SetTextSize(0.02)
    latex.SetNDC(True)
    if year in lumi_mu.keys(): latex.DrawLatex(0.9, 0.91, "%s fb^{-1} (13 TeV, #mu#mu ), %s fb^{-1} (13 TeV, ee)"%(str(int(lumi_mu[year]/1000)),str(int(lumi_el[year]/1000))))
    else: latex.DrawLatex(0.9, 0.91, "140 fb^{-1} (13 TeV, #mu#mu ), 137 fb^{-1} (13 TeV, ee)")
    print("plots/NLL/%s.pdf"%output)
    c.Print("plots/NLL/%s.pdf"%output)


