import ROOT as rt

bin_file = rt.TFile("templates/tmp2016bb_multiBins.root","READ")
bin_hist = bin_file.Get("mu_DY_S0")
bin_hist.Draw()
for i in range(bin_hist.GetNbinsX()):
    print(i)

bin_hist.SetDirectory(0)
bin_file.Close()

inputfile = rt.TFile("workspace_bb.root","READ")

ws = inputfile.Get("bb_ws")

ws.Print()
mass = ws.var("mass")

xframe = ws.var("mass").frame(rt.RooFit.Title("Signal"))
#list_mass = [400,500,690,900,1250,1610,2000,3500]
list_mass = [400,500]
sig_pdf_list = rt.RooArgList()
#sig_pdf_list = []
nsig_list = rt.RooArgList()
#nsig_list = []
#nsig_list = []
#for i in range(len(list_mass)-1):
for i in range(10):
    #nsig = rt.RooRealVar("nsig"+str(list_mass[i])+"to"+str(list_mass[i+1]), "Number of component 1 in signal", 100, 0, 5000000)    
    #nsig = rt.RooRealVar("nsig"+str(list_mass[i])+"to"+str(list_mass[i+1]), "Number of component 1 in signal", 0.1, 0.0001, 0.5)   
    if i <9: 
        nsig = rt.RooRealVar("nsig"+str(i), "Number of component 1 in signal", 0.1, 0.0001, 0.5)    
        print(type(nsig))
        nsig_list.add(nsig)
    #print(nsig_list.at(i).GetName())
    sig_pdf_list.add(ws.pdf("signal_pdf_"+str(i)))
    print(ws.pdf("signal_pdf_"+str(i)))

#pdf = ws.pdf("signal_pdf_0")

#print(pdf.GetName())
#pdf.plotOn(xframe)


sig = rt.RooAddPdf("sig", "Signal", sig_pdf_list, nsig_list, rt.kTRUE)
sig.plotOn(xframe)


xframe.Draw()

a = input('Press a key to exit')
if a:
    exit(0)
