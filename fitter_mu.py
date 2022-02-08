import ROOT as rt
import copy
#rt.gSystem.Load("RooDoubleCB/RooDoubleCB")

def readhists(ws,inputFileName,histName):
    #histfile = rt.TFile("tmp2018bb_400cut.root","READ")
    histfile = rt.TFile(inputFileName,"READ")
    
    #hist_mu_bkg = histfile.Get("mu_Other")
    #hist_el_bkg = histfile.Get("el_Other")
    hist_mu_bkg = copy.deepcopy(histfile.Get(histName))
    #hist_mu_bkg.SetDirectory(0)
    histfile.Close()
    #hist_mu_bkg.Draw()
    print(hist_mu_bkg.Integral())
    datahist = rt.RooDataHist("datahist", "datahist", rt.RooArgList(ws.var("mass")),rt.RooFit.Import(hist_mu_bkg))
    #histfile.Close()
    #ws.Import(datahist)
    getattr(ws,'import')(datahist,rt.RooCmdArg())


def makePdf(ws, channelName,nbkg, nsig):
    #fa1 = rt.TF1("fa1","[0]*exp([1] + [2]*x + [3]*x*x + [4]*x*x*x*x)*pow(x,[5])",0,10)
    #fa1 = rt.TF1("fa1","[0]*exp([1] + [2]*x)*pow(x,[3])",0,10)
    #fa1.SetParameters(1,-1,-1,-1,-1,-1)
    #mass = rt.RooRealVar("mass","mass",400.,3500.)
    bkg_a = rt.RooRealVar("bkg_"+channelName+"_a","bkg_"+channelName+"_a",nbkg, nbkg/2, nbkg*2)
    bkg_b = rt.RooRealVar("bkg_"+channelName+"_b","bkg_"+channelName+"_b",27,0, 100)
    bkg_c = rt.RooRealVar("bkg_"+channelName+"_c","bkg_"+channelName+"_c",-9.025E-3,-1, 0.01)
    bkg_d = rt.RooRealVar("bkg_"+channelName+"_d","bkg_"+channelName+"_d",0,-1, 0.01)
    bkg_e = rt.RooRealVar("bkg_"+channelName+"_e","bkg_"+channelName+"_e",0,-1, 0.01)
    bkg_f = rt.RooRealVar("bkg_"+channelName+"_f","bkg_"+channelName+"_f",0,-10, 0.01)
    #bkg_f.setConstant()
    getattr(ws,'import')(bkg_a,rt.RooCmdArg())
    getattr(ws,'import')(bkg_b,rt.RooCmdArg())
    getattr(ws,'import')(bkg_c,rt.RooCmdArg())
    getattr(ws,'import')(bkg_d,rt.RooCmdArg())
    getattr(ws,'import')(bkg_e,rt.RooCmdArg())
    getattr(ws,'import')(bkg_f,rt.RooCmdArg())
    """
    ws.Import(bkg_a)
    ws.Import(bkg_b)
    ws.Import(bkg_c)
    ws.Import(bkg_d)
    ws.Import(bkg_e)
    ws.Import(bkg_f)
    """
    #print(d.getVal())

    #bkgmodel = rt.RooGenericPdf("bkgmodel","bkgmodel","@1*exp(@2+@3*(@0-400)+@4*(@0-400)*(@0-400)+@5*(@0-400)*(@0-400)*(@0-400)*(@0-400))*pow((@0-400),@6)",rt.RooArgList(mass,a,b,c,d,e,f))
    bkgmodel = rt.RooGenericPdf("bkgmodel_"+channelName,"bkgmodel_"+channelName,"@1*exp(@2+@3*@0+@4*@0*@0+@5*@0*@0*@0)*pow(@0,@6)",rt.RooArgList(ws.obj("mass"),bkg_a,bkg_b,bkg_c,bkg_d,bkg_e,bkg_f))    
    #ws.Import(bkgmodel)
    getattr(ws,'import')(bkgmodel,rt.RooCmdArg())


    sig_a = rt.RooRealVar("sig_"+channelName+"_a","sig_"+channelName+"_a",nsig, nsig/2, nsig*2)
    sig_b = rt.RooRealVar("sig_"+channelName+"_b","sig_"+channelName+"_b",27,0, 100)
    sig_c = rt.RooRealVar("sig_"+channelName+"_c","sig_"+channelName+"_c",-9.025E-3,-1, 0.01)
    sig_d = rt.RooRealVar("sig_"+channelName+"_d","sig_"+channelName+"_d",0,-1, 0.01)
    sig_e = rt.RooRealVar("sig_"+channelName+"_e","sig_"+channelName+"_e",0,-1, 0.01)
    sig_f = rt.RooRealVar("sig_"+channelName+"_f","sig_"+channelName+"_f",0,-10, 0.01)
    #sig_f.setConstant()
    getattr(ws,'import')(sig_a,rt.RooCmdArg())
    getattr(ws,'import')(sig_b,rt.RooCmdArg())
    getattr(ws,'import')(sig_c,rt.RooCmdArg())
    getattr(ws,'import')(sig_d,rt.RooCmdArg())
    getattr(ws,'import')(sig_e,rt.RooCmdArg())
    getattr(ws,'import')(sig_f,rt.RooCmdArg())
    sigmodel = rt.RooGenericPdf("sigmodel_"+channelName,"sigmodel_"+channelName,"@1*exp(@2+@3*@0+@4*@0*@0+@5*@0*@0*@0)*pow(@0,@6)",rt.RooArgList(ws.obj("mass"),sig_a,sig_b,sig_c,sig_d,sig_e,sig_f))        
    getattr(ws,'import')(sigmodel,rt.RooCmdArg())

    mean = rt.RooRealVar("mean_" + channelName, "mean", .0, -2.0, 2.0)
    sigma = rt.RooRealVar("sigma_" + channelName, "sigma", 2, 0.0, 5.0)
    alpha1 = rt.RooRealVar("alpha1_" + channelName, "alpha1", 2, 0.001, 25)
    n1 = rt.RooRealVar("n1_" + channelName, "n1", 1.5, 0, 25)
    alpha2 = rt.RooRealVar("alpha2_" + channelName, "alpha2", 2.0, 0.001, 25)
    n2 = rt.RooRealVar("n2_" + channelName, "n2", 1.5, 0, 25)
    res_model = rt.RooDoubleCB("dcb_" + channelName, "dcb", ws.obj("mass"), mean, sigma, alpha1, n1, alpha2, n2)
    sigConvDCBmodel = rt.RooFFTConvPdf("sigxdcb","Sig(X)dcb",ws.obj("mass"),sigmodel, res_model)
    getattr(ws,'import')(mean,rt.RooCmdArg())
    getattr(ws,'import')(sigma,rt.RooCmdArg())
    getattr(ws,'import')(alpha1,rt.RooCmdArg())
    getattr(ws,'import')(n1,rt.RooCmdArg())
    getattr(ws,'import')(alpha2,rt.RooCmdArg())
    getattr(ws,'import')(n2,rt.RooCmdArg())
    getattr(ws,'import')(res_model,rt.RooCmdArg())
    getattr(ws,'import')(sigConvDCBmodel,rt.RooCmdArg())
    
    

def fitresult(ws,channelName,pdfName, datasetName):
    ws.pdf(pdfName).fitTo(ws.data(datasetName),
                          rt.RooFit.SumW2Error(rt.kTRUE), 
                          rt.RooFit.PrintLevel(-1),
                          rt.RooFit.Verbose(rt.kFALSE))
    print(type(ws.data(datasetName)))
    #ws.pdf(pdfName).fitTo(ws.data(datasetName))
    ws.var("bkg_"+channelName+"_a").setConstant(True)
    ws.var("bkg_"+channelName+"_b").setConstant(True)
    ws.var("bkg_"+channelName+"_c").setConstant(True)
    ws.var("bkg_"+channelName+"_d").setConstant(True)
    ws.var("bkg_"+channelName+"_e").setConstant(True)
    ws.var("bkg_"+channelName+"_f").setConstant(True)
    
    xframe = ws.var("mass").frame(rt.RooFit.Title("Background Fit"))
    ws.data(datasetName).plotOn(xframe,rt.RooFit.Binning(100))
    ws.pdf(pdfName).plotOn(xframe)
    #ws.pdf(pdfName).paramOn(xframe,rt.RooFit.Layout(0.62,0.90),rt.RooFit.Format("NEU",rt.RooFit.AutoPrecision(1)))
    xframe.Draw()
    nparam = ws.pdf(pdfName).getParameters(ws.data(datasetName)).getSize()
    #chi2 = xframe.chiSquare(ws.pdf(pdfName), ws.data(datasetName), nparam)
    chi2 = xframe.chiSquare(nparam)
    print("Fit chi square/ndof:", chi2)
    
def createWS(chanName):
    ws = rt.RooWorkspace(chanName+"_ws")
    mass = rt.RooRealVar('mass','mass', 400.0, 3500.)
    #ws.Import(mass)
    getattr(ws,'import')(mass,rt.RooCmdArg())
    return ws

def add_dataset(ws, dataset):
    #ws.Import(dataset)
    getattr(ws,'import')(dataset,rt.RooCmdArg())
def add_obs_data(ws, obsdata):
    #ws.Import(obsdata)
    getattr(ws,'import')(obsdata,rt.RooCmdArg())

def save_workspace(ws, out_name):
    outfile = rt.TFile(out_name+".root", "recreate")
    ws.Write()
    outfile.Close()
    #histfile.Close()
    #fa1.Draw()

def add_signal(ws, templateFilePath):
    list_mass = [400,500,690,900,1250,1610,2000,3500]
    tmpfile = rt.TFile(templateFilePath+"/tmp2016bb_multiBins.root","READ")
    #for i in range(len(list_mass)-1):
        #tmpfile = rt.TFile(templateFilePath+"/tmp2016bb_bin"+str(list_mass[i])+"to"+str(list_mass[i+1])+".root","READ")
    for i in range(10):
        tmphist = copy.deepcopy(tmpfile.Get("mu_DY_S"+str(i)))
        tmphist.SetDirectory(0)
        tmphist.Scale(1/tmphist.Integral())
        rdh_MC = rt.RooDataHist("rdh_MC","", rt.RooArgList(ws.var("mass")), rt.RooFit.Import(tmphist)) 
        #ras_rdh_MC = r.RooArgSet(rdh_MC)
        #signal_pdf = rt.RooHistPdf("signal_pdf"+str(list_mass[i])+"to"+str(list_mass[i+1]), "", rt.RooArgSet(ws.var("mass")), rdh_MC )
        signal_pdf = rt.RooHistPdf("signal_pdf_"+str(i), "", rt.RooArgSet(ws.var("mass")), rdh_MC )
        #ws.Import(signal_pdf)
        getattr(ws,'import')(signal_pdf,rt.RooCmdArg())
    tmpfile.Close()
        
if __name__ == "__main__":
    chanName = "bb"
    inputFileName = "/afs/cern.ch/work/a/arpurohi/private/Minxi_Unfolding/Combine-flavorRatio/MC/Other_mu_2016.root"
    inputHistName = "DimuonMassVertexConstrained_"
    nbkg = 100000
    nsig = 1000000
    ws = createWS(chanName)
    readhists(ws, inputFileName, inputHistName+chanName)
    makePdf(ws, chanName, nbkg, nsig)
    pdfName = "bkgmodel_"+chanName
    datasetName = "datahist"
    fitresult(ws,chanName, pdfName, datasetName)

    obs_data_inputFile = rt.TFile("/afs/cern.ch/work/a/arpurohi/private/Minxi_Unfolding/Combine-flavorRatio/combined_results/templates/tmp2016bb_multiBins.root","READ")
    data_obs_hist = copy.deepcopy(obs_data_inputFile.Get("mu_data_obs"))
    data_obs_hist.SetDirectory(0)
    obs_data_inputFile.Close()
    #add_obs_data(ws, data_obs_hist)
    #combined_results/templates/tmp2016be_multiBins.root
    add_signal(ws,"/afs/cern.ch/work/a/arpurohi/private/Minxi_Unfolding/Combine-flavorRatio/combined_results/templates")
    save_workspace(ws, "workspace_"+chanName+"_mu")
    """
    a = input('Press a key to exit')
    if a:
        exit(0)
    """