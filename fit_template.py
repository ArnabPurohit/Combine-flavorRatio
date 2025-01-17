import ROOT as rt

histfile = rt.TFile("tmp2018bb_400cut.root","READ")

hist_mu_bkg = histfile.Get("mu_Other")
hist_el_bkg = histfile.Get("el_Other")
#fa1 = rt.TF1("fa1","[0]*exp([1] + [2]*x + [3]*x*x + [4]*x*x*x*x)*pow(x,[5])",0,10)
#fa1 = rt.TF1("fa1","[0]*exp([1] + [2]*x)*pow(x,[3])",0,10)
#fa1.SetParameters(1,-1,-1,-1,-1,-1)
mass = rt.RooRealVar("mass","mass",0.,3500.)
a = rt.RooRealVar("a","a",10, 0, 10000)
b = rt.RooRealVar("b","b",-0.001,-50, 0)
c = rt.RooRealVar("c","c",-1.,-50, 0)
d = rt.RooRealVar("d","d",-1.,-50, 0)
e = rt.RooRealVar("e","e",-1.,-50, 0)
f = rt.RooRealVar("f","f",-1.,-50, 0)
#print(d.getVal())
dh = rt.RooDataHist("dh", "dh", rt.RooArgList(mass),rt.RooFit.Import(hist_mu_bkg))
#bwmodel = rt.RooGenericPdf("bwmodel","bwmodel","@1*exp(@2+@3*(@0-400)+@4*(@0-400)*(@0-400)+@5*(@0-400)*(@0-400)*(@0-400)*(@0-400))*pow((@0-400),@6)",rt.RooArgList(mass,a,b,c,d,e,f))

#bwmodel = rt.RooGenericPdf("bwmodel","bwmodel","@1*exp(@2+@3*@0+@4*@0*@0+@5*@0*@0*@0*@0)*pow(@0,@6)",rt.RooArgList(mass,a,b,c,d,e,f))
bwmodel = rt.RooGenericPdf("bwmodel","bwmodel","@1*exp(@2*@0)",rt.RooArgList(mass,a,b))
#fa1.SetParameters(1,1,1,1)
bwmodel.fitTo(dh)
xframe = mass.frame(rt.RooFit.Title("Background Fit"))
dh.plotOn(xframe)
bwmodel.plotOn(xframe)

xframe.Draw()
#fa1.Draw()
var = input('Press a key to exit')
if a:
    exit(0)
