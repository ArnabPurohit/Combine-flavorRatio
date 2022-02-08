import ROOT as rt
import copy
from array import array

nbkg = 10000
nsig = 1000
channelName = "bb"
mass = rt.RooRealVar('mass','mass', 400.0, 3500.)
#fa1 = rt.TF1("fa1","[0]*exp([1] + [2]*x + [3]*x*x + [4]*x*x*x*x)*pow(x,[5])",0,10)
#fa1 = rt.TF1("fa1","[0]*exp([1] + [2]*x)*pow(x,[3])",0,10)
#fa1.SetParameters(1,-1,-1,-1,-1,-1)
#mass = rt.RooRealVar("mass","mass",400.,3500.)
bkg_a = rt.RooRealVar("ele_bkg_"+channelName+"_a","bkg_"+channelName+"_a",nbkg, nbkg/2, nbkg*2)
bkg_b = rt.RooRealVar("ele_bkg_"+channelName+"_b","bkg_"+channelName+"_b",27,0, 100)
bkg_c = rt.RooRealVar("ele_bkg_"+channelName+"_c","bkg_"+channelName+"_c",-9.025E-3,-1, 0.01)
bkg_d = rt.RooRealVar("ele_bkg_"+channelName+"_d","bkg_"+channelName+"_d",0,-1, 0.01)
bkg_e = rt.RooRealVar("ele_bkg_"+channelName+"_e","bkg_"+channelName+"_e",0,-1, 0.01)
bkg_f = rt.RooRealVar("ele_bkg_"+channelName+"_f","bkg_"+channelName+"_f",0,-10, 0.01)
#bkg_f.setConstant()
#print(d.getVal())

#bkgmodel = rt.RooGenericPdf("bkgmodel","bkgmodel","@1*exp(@2+@3*(@0-400)+@4*(@0-400)*(@0-400)+@5*(@0-400)*(@0-400)*(@0-400)*(@0-400))*pow((@0-400),@6)",rt.RooArgList(mass,a,b,c,d,e,f))

bkgmodel = rt.RooGenericPdf("ele_bkgmodel_"+channelName,"ele_bkgmodel_"+channelName,"@1*exp(@2+@3*@0+@4*@0*@0+@5*@0*@0*@0)*pow(@0,@6)",rt.RooArgList(mass,bkg_a,bkg_b,bkg_c,bkg_d,bkg_e,bkg_f))
#getattr(ws,'import')(bkgmodel)


sig_a = rt.RooRealVar("ele_sig_"+channelName+"_a","ele_sig_"+channelName+"_a",nsig, nsig/2, nsig*2)
sig_b = rt.RooRealVar("ele_sig_"+channelName+"_b","ele_sig_"+channelName+"_b",27,0, 100)
sig_c = rt.RooRealVar("ele_sig_"+channelName+"_c","ele_sig_"+channelName+"_c",-9.025E-3,-1, 0.01)
sig_d = rt.RooRealVar("ele_sig_"+channelName+"_d","ele_sig_"+channelName+"_d",0,-1, 0.01)
sig_e = rt.RooRealVar("ele_sig_"+channelName+"_e","ele_sig_"+channelName+"_e",0,-1, 0.01)
sig_f = rt.RooRealVar("ele_sig_"+channelName+"_f","ele_sig_"+channelName+"_f",0,-10, 0.01)
#sig_f.setConstant()
sigmodel = rt.RooGenericPdf("ele_sigmodel_"+channelName,"ele_sigmodel_"+channelName,"@1*exp(@2+@3*@0+@4*@0*@0+@5*@0*@0*@0)*pow(@0,@6)",rt.RooArgList(mass,sig_a,sig_b,sig_c,sig_d,sig_e,sig_f))        
#getattr(ws,'import')(sigmodel,rt.RooCmdArg())

mean = rt.RooRealVar("ele_mean_" + channelName, "mean", .0, -2.0, 2.0)
sigma = rt.RooRealVar("ele_sigma_" + channelName, "sigma", 2, 0.0, 5.0)
sigma_formulavar = rt.RooFormulaVar("sigma_formulavar", "abs(@0/(@1*@1))",rt.RooArgList(sigma, mass))
means = array('d', [400+3100*a/10 for a in range(11)])
sigmas = array('d', [2.+a/10.0 for a in range(11)])
print(means, sigmas)
sigma_spline = rt.RooSpline1D("sigma_spline", "sigma_spline", mass, 10, means, sigmas)
alpha1 = rt.RooRealVar("ele_alpha1_" + channelName, "alpha1", 2, 0.001, 25)
n1 = rt.RooRealVar("ele_n1_" + channelName, "n1", 1.5, 0, 25)
alpha2 = rt.RooRealVar("ele_alpha2_" + channelName, "alpha2", 2.0, 0.001, 25)
n2 = rt.RooRealVar("ele_n2_" + channelName, "n2", 1.5, 0, 25)
#res_model = rt.RooDoubleCB("ele_dcb_" + channelName, "dcb", ws.obj("mass"), mean, sigma, alpha1, n1, alpha2, n2)
res_model = rt.RooDoubleCB("ele_dcb_" + channelName, "dcb", mass, mean, sigma, alpha1, n1, alpha2, n2)
res_model_formualvar = rt.RooDoubleCB("ele_dcb_formualvar" + channelName, "dcb_formualvar", mass, mean, sigma_formulavar, alpha1, n1, alpha2, n2)
res_model_spline = rt.RooDoubleCB("ele_dcb_spline" + channelName, "dcb_spline", mass, mean, sigma_spline, alpha1, n1, alpha2, n2)
#sigConvDCBmodel = rt.RooFFTConvPdf("ele_sigxdcb"+channelName,"Sig(X)dcb"+channelName,ws.obj("mass"),sigmodel, res_model)
sigConvDCBmodel = rt.RooFFTConvPdf("ele_sigxdcb"+channelName,"Sig(X)dcb"+channelName,mass, sigmodel, res_model)
sigConvDCBmodel_formualvar = rt.RooFFTConvPdf("ele_sigxdcb_formualvar"+channelName,"Sig(X)dcb_formualvar"+channelName,mass, sigmodel, res_model_formualvar)
sigConvDCBmodel_spline = rt.RooFFTConvPdf("ele_sigxdcb_spline"+channelName,"Sig(X)dcb_spline"+channelName,mass, sigmodel, res_model_spline)


xframe = mass.frame(rt.RooFit.Title("Background Fit"))
sigConvDCBmodel.plotOn(xframe)
sigConvDCBmodel.paramOn(xframe,rt.RooFit.Layout(0.62,0.90),rt.RooFit.Format("NEU",rt.RooFit.AutoPrecision(1)))
sigConvDCBmodel_formualvar.plotOn(xframe, rt.RooFit.LineColor(rt.kGreen))
sigConvDCBmodel_formualvar.paramOn(xframe,rt.RooFit.Layout(0.62,0.90),rt.RooFit.Format("NEU",rt.RooFit.AutoPrecision(1)))
sigConvDCBmodel_spline.plotOn(xframe, rt.RooFit.LineColor(rt.kRed))
sigConvDCBmodel_spline.paramOn(xframe,rt.RooFit.Layout(0.62,0.90),rt.RooFit.Format("NEU",rt.RooFit.AutoPrecision(1)))
xframe.Draw()

a = input('Press a key to exit')
if a:
    exit(0)
    
