from Parameters import eff_corr

def writeDatacards(cardName, fileName, year, cg, templates, acc_eff):

    print('write datacard for %s %s'%(year, cg))
    if "el_DY_BL" in templates.keys():
        tmpcard=open("datacards/tmp/card_tmp_singleBin.txt", "r")
    else:
        tmpcard=open("datacards/tmp/card_tmp.txt", "r") 
    tmptxt=tmpcard.read()
    tmptxt=tmptxt.replace('tmp', fileName)
    nev_mu_obs=templates['mu_data_obs'].Integral()
    tmptxt=tmptxt.replace('nev_mu_obs',str(nev_mu_obs))
    nev_el_obs=templates['el_data_obs'].Integral()
    tmptxt=tmptxt.replace('nev_el_obs',str(nev_el_obs))
    nev_el_dy_s=templates['el_DY_S'].Integral()
    tmptxt=tmptxt.replace('nev_el_dy_s',str(nev_el_dy_s))
    nev_mu_dy_s=templates['mu_DY_S'].Integral()
    tmptxt=tmptxt.replace('nev_mu_dy_s',str(nev_mu_dy_s))
    if "el_DY_BL" in templates.keys():
        nev_el_dy_bl=templates['el_DY_BL'].Integral()
        tmptxt=tmptxt.replace('nev_el_dy_bl',str(nev_el_dy_bl))
        nev_mu_dy_bl=templates['mu_DY_BL'].Integral()
        tmptxt=tmptxt.replace('nev_mu_dy_bl',str(nev_mu_dy_bl))
        nev_el_dy_bh=templates['el_DY_BH'].Integral()
        tmptxt=tmptxt.replace('nev_el_dy_bh',str(nev_el_dy_bh))
        nev_mu_dy_bh=templates['mu_DY_BH'].Integral()
        tmptxt=tmptxt.replace('nev_mu_dy_bh',str(nev_mu_dy_bh))

    else:
        nev_el_dy_b=templates['el_DY_B'].Integral()
        tmptxt=tmptxt.replace('nev_el_dy_b',str(nev_el_dy_b))
        nev_mu_dy_b=templates['mu_DY_B'].Integral()
        tmptxt=tmptxt.replace('nev_mu_dy_b',str(nev_mu_dy_b))
    nev_el_o=templates['el_Other'].Integral()
    tmptxt=tmptxt.replace('nev_el_o',str(nev_el_o))
    nev_mu_o=templates['mu_Other'].Integral()
    tmptxt=tmptxt.replace('nev_mu_o',str(nev_mu_o))    
    tmptxt=tmptxt.replace('acc_eff_med',str(acc_eff[0]))
    tmptxt=tmptxt.replace('acc_eff_err',str(acc_eff[1]))
    Effv=eff_corr["eff"+cg]
    tmptxt=tmptxt.replace('Effv',Effv)
    trigkey="trig"+year+cg
    Trigv=eff_corr[trigkey]
    tmptxt=tmptxt.replace('trig',trigkey)
    tmptxt=tmptxt.replace('Trigv',Trigv)
    tmptxt=tmptxt.replace('R1','R'+year+cg)
    tmptxt=tmptxt.replace('Rmu','Rmu'+year+cg)
    tmptxt=tmptxt.replace('Rel','Rel'+year+cg)
    for uncer in ["muMassScale","elMassScale","Smear","Prefire","PUScale","MuonID"]:
        for key in templates.keys():
            
            if "Down" in key and uncer in key.split("_")[-1] and "S" not in key.split("_")[-2] and "B" not in key.split("_")[-2] and "Other" not in key.split("_")[-2]: 
                key1=key.strip("Down")
                tmptxt=tmptxt.replace(uncer, key1.split("_")[-2]+"_"+uncer)
                break   
    datacard=open("datacards/"+cardName+".txt", "w")  
    datacard.write(tmptxt)
    tmpcard.close()
    datacard.close()

