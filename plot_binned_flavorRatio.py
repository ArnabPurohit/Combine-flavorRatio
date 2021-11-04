import sys
from array import array
import ROOT

ROOT.gROOT.SetBatch(ROOT.kTRUE)

f = ROOT.TFile("higgsCombineTest.MultiDimFit.mH120.root","READ")
t = f.Get("limit")
x = array('d')
y = array('d')
x_le = array('d')
x_he = array('d')
y_le = array('d')
y_he = array('d')
mass = [200, 300, 400,500,690,900,1250,1610, 2000, 3500]
for i in range(len(mass)-1):
    x.append((mass[i]+mass[i+1])/2)
    x_le.append((mass[i+1]-mass[i])/2)
    x_he.append((mass[i+1]-mass[i])/2)
print(t.GetEntries())
count = 0
for event in t:
    if(count>2):
        continue
    print(event.r_bin1)
    if(count==0):
        y.append(event.r_bin1)
        y.append(event.r_bin2)
        y.append(event.r_bin3)
        y.append(event.r_bin4)
        y.append(event.r_bin5)
        y.append(event.r_bin6)
        y.append(event.r_bin7)
        y.append(event.r_bin8)
        y.append(event.r_bin9)
    if(count==1):
        y_le.append(event.r_bin1)
        y_le.append(event.r_bin2)
        y_le.append(event.r_bin3)
        y_le.append(event.r_bin4)
        y_le.append(event.r_bin5)
        y_le.append(event.r_bin6)
        y_le.append(event.r_bin7)
        y_le.append(event.r_bin8)
        y_le.append(event.r_bin9)
    if(count==2):
        y_he.append(event.r_bin1)
        y_he.append(event.r_bin2)
        y_he.append(event.r_bin3)
        y_he.append(event.r_bin4)
        y_he.append(event.r_bin5)
        y_he.append(event.r_bin6)
        y_he.append(event.r_bin7)
        y_he.append(event.r_bin8)
        y_he.append(event.r_bin9)
    count+=1

for i in range(len(mass)-1):
    y_le[i]=(y[i]-y_le[i])
    y_he[i]=(y_he[i]-y[i])
gr = ROOT.TGraphAsymmErrors(len(mass)-1,x,y,x_le,x_he,y_le,y_he)
#graph.Draw()
c = ROOT.TCanvas("c","c",800,800)
c.SetGridx()
c.SetGridy()
c.SetRightMargin(0.06)
c.SetLeftMargin(0.2)

# dummy historgram for axes labels, ranges, etc.
d = ROOT.TH1D("","", 1, 200,3500)
d.SetStats(ROOT.kFALSE)
d.SetBinContent(1,0.0)
d.GetXaxis().SetTitle('m_{#mu#mu} [GeV]')
d.GetYaxis().SetTitle('Flavor Ratio (R)')
d.SetLineColor(0)
d.SetLineWidth(0)
d.SetFillColor(0)
d.SetMinimum(0.0)
d.SetMaximum(2.0)
d.Draw()
gr.SetMarkerColor(1)
gr.SetMarkerStyle(21)
gr.SetLineColor(1)
gr.SetLineWidth(2)
gr.Draw("Psame")
legend = ROOT.TLegend(.60,.70,.90,.87)
legend.AddEntry(gr , "Observed Flavor Ratio", "l")
legend.SetShadowColor(0)
legend.SetFillColor(0)
legend.SetLineColor(0)
legend.Draw("same")

ROOT.gPad.RedrawAxis()

c.Draw()
c.SaveAs("FR_perBin_2016.png")
c.SaveAs("FR_perBin_2016.pdf")
c.SaveAs("FR_perBin_2016.root")
c.SaveAs("FR_perBin_2016.C")
