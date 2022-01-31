from django.core.management.base import BaseCommand
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import requests
from stock.models import Member, Profile, Asset
import time
import datetime
from django.utils import timezone

class Command(BaseCommand):
    help = "collect member info"
    
    def handle(self, *args, **options):
        ##copied from test.py output
        start = time.perf_counter()
        member_list = [
        'SPY','MMM','ABT','ABBV','ABMD','ACN','ATVI','ADBE','AMD','AAP','AES','AFL','A','APD','AKAM','ALK','ALB','ARE','ALGN','ALLE','LNT','ALL','GOOGL','GOOG',
        'MO','AMZN','AMCR','AEE','AAL','AEP','AXP','AIG','AMT','AWK','AMP','ABC','AME','AMGN','APH','ADI','ANSS','ANTM','AON','AOS','APA','AAPL','AMAT','APTV',
        'ADM','ANET','AJG','AIZ','T','ATO','ADSK','ADP','AZO','AVB','AVY','BKR','BLL','BAC','BK','BAX','BDX','BRK.B','BBY','BIO','BIIB','BLK','BA','BKNG','BWA',
        'BXP','BSX','BMY','AVGO','BR','BF.B','CHRW','COG','CDNS','CZR','CPB','COF','CAH','KMX','CCL','CARR','CTLT','CAT','CBOE','CBRE','CDW','CE','CNC','CNP',
        'CERN','CF','CRL','SCHW','CHTR','CVX','CMG','CB','CHD','CI','CINF','CTAS','CSCO','C','CFG','CTXS','CLX','CME','CMS','KO','CTSH','CL','CMCSA','CMA','CAG',
        'COP','ED','STZ','COO','CPRT','GLW','CTVA','COST','CCI','CSX','CMI','CVS','DHI','DHR','DRI','DVA','DE','DAL','XRAY','DVN','DXCM','FANG','DLR','DFS','DISCA',
        'DISCK','DISH','DG','DLTR','D','DPZ','DOV','DOW','DTE','DUK','DRE','DD','DXC','EMN','ETN','EBAY','ECL','EIX','EW','EA','EMR','ENPH','ETR','EOG','EFX','EQIX',
        'EQR','ESS','EL','ETSY','EVRG','ES','RE','EXC','EXPE','EXPD','EXR','XOM','FFIV','FB','FAST','FRT','FDX','FIS','FITB','FE','FRC','FISV','FLT','FMC','F','FTNT',
        'FTV','FBHS','FOXA','FOX','BEN','FCX','GPS','GRMN','IT','GNRC','GD','GE','GIS','GM','GPC','GILD','GL','GPN','GS','GWW','HAL','HBI','HIG','HAS','HCA','PEAK',
        'HSIC','HSY','HES','HPE','HLT','HOLX','HD','HON','HRL','HST','HWM','HPQ','HUM','HBAN','HII','IEX','IDXX','INFO','ITW','ILMN','INCY','IR','INTC','ICE','IBM',
        'IP','IPG','IFF','INTU','ISRG','IVZ','IPGP','IQV','IRM','JKHY','J','JBHT','JNJ','JCI','JPM','JNPR','KSU','K','KEY','KEYS','KMB','KIM','KMI','KLAC',
        'KHC','KR','LB','LHX','LH','LRCX','LW','LVS','LEG','LDOS','LEN','LLY','LNC','LIN','LYV','LKQ','LMT','L','LOW','LUMN','LYB','MTB','MRO','MPC','MKTX','MAR',
        'MMC','MLM','MAS','MA','MKC','MXIM','MCD','MCK','MDT','MRK','MET','MTD','MGM','MCHP','MU','MSFT','MAA','MRNA','MHK','TAP','MDLZ','MPWR','MNST','MCO','MS',
        'MOS','MSI','MSCI','NDAQ','NTAP','NFLX','NWL','NEM','NWSA','NWS','NEE','NLSN','NKE','NI','NSC','NTRS','NOC','NLOK','NCLH','NOV','NRG','NUE','NVDA','NVR','NXPI',
        'ORLY','OXY','ODFL','OMC','OKE','ORCL','OGN','OTIS','PCAR','PKG','PH','PAYX','PAYC','PYPL','PENN','PNR','PBCT','PEP','PKI','PRGO','PFE','PM','PSX','PNW','PXD',
        'PNC','POOL','PPG','PPL','PFG','PG','PGR','PLD','PRU','PTC','PEG','PSA','PHM','PVH','QRVO','PWR','QCOM','DGX','RL','RJF','RTX','O','REG','REGN','RF','RSG','RMD',
        'RHI','ROK','ROL','ROP','ROST','RCL','SPGI','CRM','SBAC','SLB','STX','SEE','SRE','NOW','SHW','SPG','SWKS','SNA','SO','LUV','SWK','SBUX','STT','STE','SYK','SIVB',
        'SYF','SNPS','SYY','TMUS','TROW','TTWO','TPR','TGT','TEL','TDY','TFX','TER','TSLA','TXN','TXT','TMO','TJX','TSCO','TT','TDG','TRV','TRMB','TFC','TWTR','TYL','TSN',
        'UDR','ULTA','USB','UAA','UA','UNP','UAL','UNH','UPS','URI','UHS','UNM','VLO','VTR','VRSN','VRSK','VZ','VRTX','VFC','VIAC','VTRS','V','VNO','VMC','WRB','WAB','WMT',
        'WBA','DIS','WM','WAT','WEC','WFC','WELL','WST','WDC','WU','WRK','WY','WHR','WMB','WLTW','WYNN','XEL','XLNX','XYL','YUM','ZBRA','ZBH','ZION','ZTS',    
        'A','AA','AAC','AAC.U','AAC.W','AAI-B','AAI-C','AAIC','AAIN','AAN','AAP','AAQ.U','AAQ.W','AAQC','AAT','AB','ABB','ABBV','ABC','ABEV',
        'ABG','ABM','ABR','ABT','AC','ACA','ACC','ACCO','ACEL','ACH','ACI','ACI.S','ACI.T','ACI.U','ACI.W','ACIC','ACII',
        'ACM','ACN','ACN.U','ACN.W','ACND','ACP','ACP-A','ACR','ACR-C','ACR-D','ACR.U','ACRE','ACV','ADC','ADCT','ADE.U','ADE.W','ADEX','ADF','ADF.U','ADF.W',
        'ADM','ADNT','ADS','ADT','ADX','AEB','AEE','AEFC','AEG','AEL','AEL-A','AEL-B','AEM','AENZ','AEO','AER','AES','AESC','AEV.W','AEVA','AFB','AFG','AFGB',
        'AFGC','AFGD','AFGE','AFI','AFL','AFT','AG','AGA.U','AGA.W','AGAC','AGCB','AGCO','AGD','AGI','AGL','AGM','AGM-C','AGM-D','AGM-E','AGM-F','AGM-G','AGM.A',
        'AGO','AGO-B','AGO-E','AGO-F','AGR','AGRO','AGS','AGTI','AGX','AHC','AHH','AHH-A','AHL-C','AHL-D','AHL-E','AHT','AHT-D','AHT-F','AHT-G','AHT-H','AHT-I',
        'AI','AIC','AIF','AIG','AIG-A','AIN','AIO','AIR','AIRC','AIT','AIV','AIW','AIZ','AIZN','AJA.U','AJA.W','AJAX','AJG','AJRD','AJX','AJXA','AKO.A','AKO.B',
        'AKR','AL','AL-A','ALB','ALC','ALCC','ALE','ALEX','ALG','ALI-A','ALI-B','ALI-E','ALI.W','ALIT','ALK','ALL','ALL-B','ALL-G','ALL-H','ALL-I','ALL-Y','ALLE',
        'ALLY','ALP-Q','ALSN','ALT-A','ALTG','ALU.U','ALU.W','ALUS','ALV','ALX','AM','AMAM','AMB.W','AMBC','AMC','AMCR','AME','AMG','AMH','AMH-E','AMH-F','AMH-G',
        'AMH-H','AMK','AMN','AMOV','AMP','AMP.U','AMP.W','AMPI','AMPY','AMR','AMRC','AMRX','AMT','AMWL','AMX','AN','ANA.U','ANA.W','ANAC','ANET','ANF','ANTM','AOD',
        'AOMR','AON','AON.U','AON.W','AONE','AOS','AP','APAM','APD','APG','APG.U','APG.W','APGB','APH','APLE','APO','APO-A','APO-B','APRN','APS.U','APS.W','APSG',
        'APT-A','APTS','APTV','AQN','AQNA','AQNB','AQNU','AQUA','AR','ARC','ARCH','ARCO','ARD','ARDC','ARE','ARE-A','ARES','ARG-A','ARGD','ARGO','ARI','ARL','ARLO',
        'ARMK','ARNC','AROC','ARR','ARR-C','ARW','ASA','ASA.U','ASA.W','ASAI','ASAN','ASAQ','ASB','ASB-D','ASB-E','ASB-F','ASC','ASG','ASGI','ASGN','ASH','ASIX',
        'ASP.U','ASP.W','ASPL','ASPN','ASR','ASX','ASZ','ASZ.U','ASZ.W','ATA','ATA.D','ATA.U','ATA.V','ATA.W','ATAQ','ATC','ATC-D','ATC-E','ATC-G','ATC-H','ATC-I',
        'ATCO','ATEN','ATGE','ATH','ATH-A','ATH-B','ATH-C','ATH-D','ATH.U','ATH.W','ATHM','ATHN','ATI','ATI.W','ATIP','ATKR','ATM.U','ATM.W','ATMR','ATO','ATR','ATTO',
        'ATUS','AU','AUD','AUS','AUS.U','AUS.W','AUY','AVA','AVA.U','AVA.W','AVAL','AVAN','AVB','AVD','AVK','AVLR','AVNS','AVNT','AVT-A','AVTR','AVY','AVYA','AWF','AWI',
        'AWK','AWP','AWR','AX','AXL','AXP','AXR','AXS','AXS-E','AXTA','AYI','AYX','AZEK','AZO','AZRE','AZUL','AZZ','B','BA','BABA','BAC','BAC-B','BAC-E','BAC-K',
        'BAC-L','BAC-M','BAC-N','BAC-O','BAC-P','BAH','BAK','BALY','BAM','BAMH','BAMI','BAMR','BAN-E','BANC','BAP','BAR.W','BARK','BAX','BB','BBAR','BBD','BBDC',
        'BBDO','BBL','BBN','BBU','BBVA','BBW','BBY','BC','BC-A','BC-B','BC-C','BCAT','BCC','BCE','BCEI','BCH','BCO','BCS','BCSF','BCX','BDC','BDJ','BDN','BDX','BDXB',
        'BE','BEDU','BEKE','BEN','BEP','BEP-A','BEPC','BEPH','BERY','BEST','BF.A','BF.B','BFAM','BFK','BFL.W','BFLY','BFS','BFS-D','BFS-E','BFZ','BG','BGB','BGH',
        'BGIO','BGR','BGS','BGS.U','BGS.W','BGSF','BGSX','BGT','BGX','BGY','BH','BH.A','BHC','BHE','BHG','BHK','BHLB','BHP','BHR','BHR-B','BHR-D','BHV','BHVN','BIF',
        'BIG','BIGZ','BILL','BIO','BIO.B','BIP','BIP-A','BIP-B','BIPC','BIPH','BIT','BIT.U','BIT.W','BITE','BJ','BK','BKD','BKE','BKH','BKI','BKN','BKR','BKT','BKU',
        'BLD','BLDR','BLE','BLK','BLL','BLND','BLU.U','BLU.W','BLUA','BLW','BLX','BMA','BME','BMEZ','BMI','BML-G','BML-H','BML-J','BML-L','BMO','BMY','BNED','BNL','BNS'
        ,'BNY','BOA.S','BOA.T','BOA.U','BOA.W','BOAC','BOAS','BOD.W','BODY','BOE','BOH','BOH-A','BOOT','BORR','BOX','BP','BPMP','BPT','BQ','BR','BRBR','BRC','BRDG','BRFS',
        'BRK.A','BRK.B','BRMK','BRO','BRSP','BRT','BRW','BRX','BSA','BSA.U','BSAC','BSBR','BSIG','BSL','BSM','BSMX','BSN','BSN.U','BSN.W','BST','BST.P','BSTZ','BSX','BSX-A',
        'BTA','BTCM','BTI','BTO','BTT','BTU','BTZ','BUD','BUI','BUR','BURL','BV','BVH','BVN','BW','BW-A','BWA','BWG','BWSN','BWXT','BX','BXC','BXMT','BXMX','BXP','BXS',
        'BXS-A','BY','BYD','BYM','BZH','C','C-J','C-K','C-N','CAAP','CABO','CACI','CADE','CAE','CAF','CAG','CAH','CAI','CAI-A','CAI-B','CAJ','CAL','CALX','CAN.W','CANG',
        'CANO','CAP','CAP.U','CAP.W','CAPL','CARR','CARS','CAS','CAS.U','CAS.W','CAT','CATO','CB','CBA.U','CBA.W','CBAH','CBB','CBB-B','CBD','CBH','CBRE','CBT','CBU','CBZ',
        'CC','CCA.U','CCA.W','CCAC','CCEP','CCI','CCI.U','CCI.W','CCIV','CCJ','CCK','CCL','CCM','CCO','CCS','CCU','CCV','CCV.S','CCV.T','CCV.U','CCV.W','CCVI','CCZ','CDAY',
        'CDE','CDR','CDR-B','CDR-C','CE','CEA','CEE','CEIX','CEL.P','CELP','CEM','CEN','CEPU','CEQ.P','CEQP','CF','CFG','CFG-D','CFG-E','CFR','CFR-B','CFX','CFXA','CGA','CGAU',
        'CHA.S','CHA.T','CHAA','CHCT','CHD','CHE','CHGG','CHH','CHM-A','CHM-B','CHMI','CHN','CHP.W','CHPT','CHRA','CHS','CHT','CHWY','CI','CIA','CIB','CIEN','CIF','CIG',
        'CIG.C','CII','CIM','CIM-A','CIM-B','CIM-C','CIM-D','CINR','CINF','CIO','CIO-A','CIR','CIT','CIT-B','CIXX','CL','CLA.S','CLA.T','CLA.U','CLA.W','CLAA','CLAS','CLB','CLB.U',
        'CLB.W','CLBR','CLD-A','CLDR','CLDT','CLF','CLH','CLI','CLI.S','CLI.T','CLI.U','CLI.W','CLII','CLIM','CLN-G','CLN-H','CLN-I','CLN-J','CLNC','CLNY','CLPR','CLR','CLS',
        'CLV-A','CLVT','CLW','CLX','CM','CMA','CMC','CMCM','CMG','CMI','CMO','CMO-E','CMP','CMR-B','CMR-C','CMR-D','CMR-E','CMRE','CMS','CMS-B','CMS-C','CMSA','CMSC','CMSD',
        'CMU','CNA','CNC','CND','CND.U','CND.W','CNF','CNHI','CNI','CNK','CNMD','CNNE','CNO','CNO-A','CNP','CNP-B','CNQ','CNR','CNS','CNVY','CNX','CO','COD-A','COD-B','COD-C',
        'CODI','COE','COF','COF-G','COF-H','COF-I','COF-J','COF-K','COF-L','COG','COLD','COMP','COO','COP','COR','COR-Z','COR.U','CORR','COTY','COUR','CP','CPA','CPAC','CPB',
        'CPE','CPF','CPG','CPK','CPLG','CPNG','CPRI','CPS','CPS.U','CPS.W','CPSR','CPT','CPT.U','CPT.W','CPTK','CPU.U','CPU.W','CPUH','CR','CRC','CRD.A','CRD.B','CRH','CRH.U',
        'CRH.W','CRHC','CRI','CRK','CRL','CRM','CRS','CRT','CRU','CRU.U','CRU.W','CRY','CS','CSAN','CSL','CSLT','CSPR','CSR','CSR-C','CST.U','CST.W','CSTA','CSTM','CSU','CSV',
        'CTA-A','CTA-B','CTA.U','CTA.W','CTAC','CTBB','CTDD','CTK','CTLT','CTO','CTO-A','CTO.W','CTOS','CTR','CTS','CTT','CTVA','CUB-C','CUB-D','CUB-E','CUB-F','CUBB','CUBE',
        'CUBI','CUK','CULP','CURO','CURV','CUZ','CVA','CVE','CVE.W','CVEO','CVI','CVI.U','CVI.W','CVII','CVNA','CVS','CVX','CW','CWE.A','CWEN','CWH','CWK','CWT','CX','CXE','CXH',
        'CXM','CXP','CXW','CYD','CYH','D','DAC','DAL','DAN','DAO','DAR','DASH','DAVA','DB','DBD','DBI','DBL','DBR-G','DBR-H','DBR-I','DBR-J','DBRG','DCF','DCI','DCO','DCP','DCP-B',
        'DCP-C','DCUE','DD','DDD','DDF','DDL','DDS','DDT','DE','DEA','DECK','DEH','DEH.U','DEH.W','DEI','DELL','DEN','DEO','DESP','DEX','DFIN','DFN.U','DFN.W','DFNS','DFP',
        'DFS','DG','DGN.U','DGN.W','DGNR','DGX','DHF','DHI','DHR','DHR-A','DHR-B','DHT','DHX','DIAX','DIDI','DIN','DIS','DK','DKL','DKS','DLB','DLN-A','DLN-B','DLNG','DLR',
        'DLR-J','DLR-K','DLR-L','DLX','DLY','DM','DMB','DMO','DMS','DMS.W','DMY.D','DMY.U','DMY.V','DMY.W','DMYI','DMYQ','DNB','DNMR','DNOW','DNP','DNZ','DNZ.U','DNZ.W','DOC',
        'DOCN','DOCS','DOOR','DOV','DOW','DPG','DPZ','DQ','DRD','DRE','DRH','DRH-A','DRI','DRQ','DRUA','DS','DS-B','DS-C','DS-D','DSE','DSL','DSM','DSSI','DSU','DSX','DSX-B',
        'DT','DTB','DTE','DTE.P','DTF','DTJ','DTL.P','DTM','DTM.P','DTP','DTW','DTY','DUK','DUK-A','DUKB','DUKH','DV','DVA','DVD','DVN','DWI.U','DWI.W','DWIN','DX','DX-C',
        'DXC','DY','DYFN','E','EAF','EAI','EARN','EAT','EB','EBF','EBR','EBR.B','EBS','EC','ECC','ECCB','ECCC','ECCW','ECCX','ECCY','ECL','ECOM','ED','EDD','EDF','EDI','EDN',
        'EDR','EDU','EEA','EEX','EFC','EFC-A','EFL','EFR','EFT','EFX','EGF','EGG.U','EGG.W','EGHT','EGO','EGP','EGY','EHC','EHI','EHT','EIC','EIG','EIX','EL','ELAN','ELAT',
        'ELC','ELF','ELP','ELS','ELVT','ELY','EMD','EME','EMF','EMN','EMO','EMP','EMP.U','EMP.W','EMPW','EMR','ENB','ENBA','ENBL','ENIA','ENIC','ENJ','ENLC','ENO','ENP.U',
        'ENP.W','ENPC','ENR','ENR-A','ENS','ENV','ENVA','ENZ','EOC.U','EOD','EOG','EOI','EOS','EOT','EP-C','EPAC','EPAM','EPC','EPD','EPR','EPR-C','EPR-E','EPR-G','EPRT',
        'EPW.U','EPW.W','EPWR','EQC','EQC-D','EQD','EQD.U','EQD.W','EQH','EQH-A','EQH-C','EQH.U','EQH.W','EQHA','EQNR','EQR','EQS','EQT','ERF','ERJ','ERO','ES','ESE','ESGC',
        'ESI','ESM','ESM.U','ESM.W','ESNT','ESRT','ESS','ESTC','ESTE','ET','ET-C','ET-D','ET-E','ETB','ETG','ETH','ETI.P','ETJ','ETN','ETO','ETR','ETRN','ETV','ETW','ETW.W',
        'ETWO','ETX','ETY','EURN','EVA','EVC','EVF','EVG','EVH','EVN','EVR','EVRG','EVRI','EVT','EVTC','EW','EXD','EXG','EXK','EXP','EXPR','EXR','EXTN','F','F-B','F-C','FAC.S',
        'FAC.T','FAC.U','FAC.W','FACA','FACT','FAF','FAM','FBC','FBHS','FBK','FBP','FC','FCA.U','FCA.W','FCAX','FCF','FCN','FCPT','FCRW','FCRX','FCT','FCX','FDEU','FDP','FDS',
        'FDX','FE','FEDU','FEI','FENG','FEO','FERG','FET','FF','FFA','FFC','FGB','FGN.U','FGN.W','FGNA','FHI','FHN','FHN-A','FHN-B','FHN-C','FHN-D','FHN-E','FHN-F','FHS','FI',
        'FICO','FIF','FIGS','FINS','FINV','FIS','FIV','FIX','FL','FLC','FLM.U','FLM.W','FLME','FLNG','FLO','FLOW','FLR','FLS','FLT','FLY','FMA.U','FMA.W','FMAC','FMC','FMN',
        'FMO','FMS','FMX','FMY','FN','FNB','FNB-E','FND','FNF','FNV','FOA','FOA.W','FOE','FOF','FOR','FOUR','FPA.U','FPA.W','FPAC','FPF','FPH','FPI','FPI-B','FPL','FR','FRA',
        'FRC','FRC-H','FRC-I','FRC-J','FRC-K','FRC-L','FRE.W','FREY','FRO','FRT','FRT-C','FRX','FRX.S','FRX.T','FRX.U','FRX.W','FRXB','FSD','FSK','FSLF','FSLY','FSM','FSN.U',
        'FSN.W','FSNB','FSR','FSS','FST','FST.U','FST.W','FT','FTA-A','FTA-B','FTA-C','FTAI','FTCH','FTE.U','FTE.W','FTEV','FTHY','FTI','FTK','FTS','FTV','FTV-A','FUBO',
        'FUL','FUN','FUS.U','FUS.W','FUSE','FVI.U','FVI.W','FVIV','FVRR','FVT','FVT.U','FVT.W','FXLV','FZT','FZT.U','FZT.W','G','GAB','GAB-G','GAB-H','GAB-J','GAB-K','GAB.P',
        'GAM','GAM-B','GAP.U','GAP.W','GAPA','GATO','GATX','GB','GB.W','GBAB','GBL','GBX','GCI','GCO','GCP','GCV','GD','GDDY','GDL','GDL-C','GDO','GDOT','GDV','GDV-G','GDV-H',
        'GE','GEF','GEF.B','GEL','GEN.W','GENI','GEO','GER','GES','GF','GFF','GFI','GFL','GFLU','GFO.U','GFO.W','GFOR','GFX','GFX.U','GFX.W','GGB','GGG','GGM','GGT','GGT-E',
        'GGT-G','GGT.P','GGZ','GGZ-A','GHC','GHG','GHL','GHLD','GHM','GHY','GIB','GIC','GIL','GIM','GIS','GJH','GJO','GJP','GJR','GJS','GJT','GKOS','GL','GL-C','GL-D',
        'GLE.U','GLE.W','GLEO','GLO-A','GLO-B','GLO-C','GLO-G','GLOB','GLOP','GLP','GLP-A','GLP-B','GLT','GLW','GM','GME','GMED','GMR-A','GMRE','GMS','GNE','GNE-A','GNK',
        'GNL','GNL-A','GNL-B','GNP.U','GNP.W','GNPK','GNRC','GNT','GNT-A','GNW','GOA.U','GOA.W','GOAC','GOF','GOL','GOLD','GOLF','GOOS','GOTU','GPC','GPI','GPJA','GPK','GPM',
        'GPMT','GPN','GPOR','GPRK','GPS','GPX','GRA','GRC','GRP.U','GRX','GS','GS-A','GS-C','GS-D','GS-J','GS-K','GSA.U','GSA.W','GSAH','GSBD','GSK','GSL','GSL-B','GSLD',
        'GSQ.U','GSQ.W','GSQD','GTES','GTLS','GTN','GTN.A','GTS','GTT','GTY','GUT','GUT-A','GUT-C','GVA','GWB','GWRE','GWW','H','HAE','HAL','HASI','HAYW','HBB','HBI','HBM',
        'HCA','HCC','HCHC','HCI','HCXY','HCXZ','HD','HDB','HE','HEI','HEI.A','HEP','HEQ','HES','HESM','HEXO','HFC','HFR-A','HFRO','HGH','HGLB','HGV','HHC','HHL.U','HHL.W',
        'HHLA','HI','HIE','HIG','HIG-G','HIG.U','HIG.W','HIGA','HII','HIL','HIM.W','HIMS','HIO','HIW','HIX','HKIB','HL','HL-B','HLF','HLI','HLL.W','HLLY','HLT','HLX','HMC',
        'HML-A','HMLP','HMN','HMY','HNGR','HNI','HNP','HOG','HOME','HOV','HP','HPE','HPF','HPI','HPP','HPQ','HPS','HPX','HPX.U','HPX.W','HQH','HQL','HR','HRB','HRC','HRI',
        'HRL','HRTG','HSBC','HSC','HSY','HT','HT-C','HT-D','HT-E','HTA','HTD','HTFB','HTGC','HTH','HTP.U','HTP.W','HTPA','HTY','HUBB','HUBS','HUG.U','HUG.W','HUGS','HUM',
        'HUN','HUYA','HVT','HVT.A','HWM','HXL','HY','HYB','HYI','HYLN','HYT','HZA.U','HZA.W','HZAC','HZN','HZO','HZO.U','HZO.W','HZON','IAA','IAC.S','IAC.T','IAC.U','IAC.W',
        'IACA','IACB','IACC','IAE','IAG','IBA','IBE.U','IBE.W','IBER','IBM','IBN','IBP','ICD','ICE','ICL','IDA','IDE','IDT','IEX','IFF','IFFT','IFN','IFS','IGA','IGD','IGI',
        'IGR','IGT','IH','IHC','IHD','IHG','IHIT','IHTA','IIA.U','IIA.W','IIAC','IIF','IIIN','IIM','IIP-A','IIPR','IMAX','IMP.U','IMP.W','IMPX','INFO','INFY','ING','INGR',
        'INN','INN-D','INN-E','INS','INS-A','INSI','INSP','INSW','INT','INVH','IO','IP','IPG','IPI','IPO.D','IPO.F','IPO.V','IPO.Z','IPOD','IPOF','IPV.D','IPV.S','IPV.T',
        'IPV.V','IPVA','IPVF','IQI','IQV','IR','IRL','IRM','IRS','IRS.W','IRT','IS','ISD','ISO.U','ISO.W','ISOS','IT','ITCB','ITGR','ITT','ITUB','ITW','IVA.U','IVA.W','IVAN',
        'IVC','IVH','IVR','IVR-B','IVR-C','IVZ','IX','J','JAT.U','JAX','JBGS','JBI','JBI.W','JBK','JBL','JBT','JCE','JCI','JCO','JDD','JEF','JELD','JEMD','JEQ','JFR','JGH',
        'JHAA','JHB','JHG','JHI','JHS','JHX','JILL','JKS','JLL','JLS','JMIA','JMM','JMP','JNJ','JNPR','JOE','JOF','JP','JPC','JPI','JPM','JPM-C','JPM-D','JPM-J','JPM-K',
        'JPM-L','JPS','JPT','JQC','JRI','JRO','JRS','JSD','JT','JTA','JTD','JW.A','JW.B','JWN','JWS.S','JWS.T','JWSM','K','KAH.U','KAH.W','KAHC','KAI','KAMN','KAR','KB',
        'KBH','KBR','KCA.U','KCA.W','KCAC','KEN','KEP','KEX','KEY','KEY-I','KEY-J','KEY-K','KEYS','KF','KFS','KFY','KGC','KIM','KIM-L','KIM-M','KIO','KKR','KKR-B','KKR-C',
        'KKRS','KL','KMB','KMF','KMI','KMPR','KMT','KMX','KN','KNL','KNOP','KNX','KO','KODK','KOF','KOP','KOS','KR','KRA','KRC','KRE-A','KREF','KRG','KRO','KRP','KSM','KSS',
        'KSU','KSU.P','KT','KTB','KTF','KTH','KTN','KUKE','KW','KWA.U','KWA.W','KWAC','KWR','KYN','L','LAC','LAD','LADR','LAIX','LAZ','LB','LBRT','LC','LCI','LCII','LDI','LDL',
        'LDOS','LDP','LEA','LEA.U','LEA.W','LEAP','LEG','LEJU','LEN','LEN.B','LEO','LEV','LEV.W','LEVI','LFC','LFT','LFT-A','LGF.A','LGF.B','LGI','LGV','LGV.U','LGV.W','LH',
        'LHC','LHC.U','LHC.W','LHX','LII','LII.U','LII.W','LIII','LIN','LINX','LITB','LL','LLY','LMND','LMT','LNC','LND','LNF.U','LNF.W','LNFA','LNN','LOK.S','LOK.T','LOK.U',
        'LOK.W','LOKB','LOKM','LOMA','LOW','LPG','LPI','LPL','LPX','LRN','LSI','LSPD','LTC','LTHM','LU','LUB','LUMN','LUV','LVS','LW','LXFR','LXP','LXP-C','LXU','LYB','LYG',
        'LYV','LZB','M','MA','MAA','MAA-I','MAC','MAC.U','MAC.W','MACC','MAIN','MAN','MANU','MAS','MATX','MAV','MAX','MAXR','MBA.U','MBA.W','MBAC','MBI','MBT','MC','MCA',
        'MCB','MCD','MCG','MCI','MCK','MCN','MCO','MCR','MCS','MCW','MCY','MD','MDC','MDH','MDH.U','MDH.W','MDLA','MDLQ','MDLX','MDLY','MDP','MDT','MDU','MEC','MED','MEG',
        'MEI','MER-K','MET','MET-A','MET-E','MET-F','MFA','MFA-B','MFA-C','MFC','MFD','MFG','MFGP','MFL','MFM','MFV','MG','MGA','MGF','MGM','MGP','MGR','MGRB','MGU','MGY',
        'MH-A','MH-C','MH-D','MHD','MHF','MHI','MHK','MHLA','MHN','MHNC','MHO','MIC','MIE','MIN','MIT','MIT-A','MIT-B','MIT-C','MIT.U','MIT.W','MITT','MIXT','MIY','MKC',
        'MKC.V','MKF.W','MKFG','MKL','MLI','MLM','MLP','MLR','MMC','MMD','MMI','MMM','MMP','MMS','MMT','MMU','MN','MNP','MNR','MNR-C','MNRL','MNSO','MO','MOD','MODN','MOG.A',
        'MOG.B','MOGU','MOH','MOS','MOT.U','MOT.W','MOTV','MOV','MP','MPA','MPC','MPL.W','MPLN','MPLX','MPV','MPW','MPX','MQT','MQY','MRC','MRK','MRO','MS','MS-A','MS-E',
        'MS-F','MS-I','MS-K','MS-L','MSA','MSB','MSC','MSCI','MSD','MSGE','MSGN','MSGS','MSI','MSM','MSP','MT','MTB','MTCN','MTD','MTDR','MTG','MTH','MTL','MTL.P','MTN','MTOR',
        'MTR','MTRN','MTW','MTX','MTZ','MUA','MUC','MUE','MUFG','MUI','MUJ','MUR','MUSA','MUX','MVF','MVO','MVT','MWA','MX','MXE','MXF','MXL','MYC','MYD','MYE','MYI','MYJ','MYN',
        'MYOV','MYTE','NAC','NAD','NAN','NAPA','NAT','NAZ','NBB','NBHC','NBR','NBXG','NC','NCA','NCLH','NCR','NCV','NCV-A','NCZ','NCZ-A','NDMO','NDP','NE','NEA','NEE','NEE-K',
        'NEE-N','NEE-O','NEE-P','NEE-Q','NEM','NEP','NET','NETI','NEU','NEV','NEW','NEWR','NEX','NEXA','NFG','NFH','NFH.W','NFJ','NGA.S','NGA.T','NGAB','NGC','NGC.U','NGC.W',
        'NGG','NGL','NGL-B','NGL-C','NGS','NGVC','NGVT','NHF','NHF-A','NHI','NI','NI-B','NID','NIE','NIM','NIMC','NINE','NIO','NIQ','NJR','NKE','NKG','NKX','NL','NLS','NLSN',
        'NLY','NLY-F','NLY-G','NLY-I','NM','NM-G','NM-H','NMCO','NMG','NMI','NMK-B','NMK-C','NMM','NMR','NMS','NMT','NMZ','NNA','NNI','NNN','NNN-F','NNY','NOA','NOAH','NOC',
        'NOK','NOM','NOMD','NOV','NOVA','NOW','NP','NPCT','NPK','NPO','NPTN','NPV','NQP','NR','NRE-A','NREF','NRG','NRGX','NRK','NRP','NRT','NRUC','NRZ','NRZ-A','NRZ-B','NRZ-C',
        'NS','NS-A','NS-B','NS-C','NSA','NSA-A','NSC','NSH','NSH.U','NSH.W','NSL','NSP','NSS','NST.D','NST.S','NST.T','NST.U','NST.V','NST.W','NSTB','NSTC','NSTD','NTB','NTCO',
        'NTEST','NTG','NTP','NTR','NTST','NTZ','NUE','NUO','NUS','NUV','NUV.W','NUVB','NUW','NVG','NVGS','NVO','NVR','NVRO','NVS','NVST','NVT','NVTA','NWG','NWHM','NWN','NX',
        'NXC','NXJ','NXN','NXP','NXQ','NXR','NXRT','NXU','NXU.U','NXU.W','NYC','NYC-A','NYC-U','NYCB','NYT','NZF','O','OAC.S','OAC.Z','OACB','OAK-A','OAK-B','OC','OCA','OCA.U',
        'OCA.W','OCFT','OCN','ODC','OEC','OFC','OFG','OFG-D','OG','OGE','OGN','OGS','OHI','OI','OIA','OIB.C','OII','OIS','OKE','OLN','OLO','OLP','OMC','OMF','OMI','ONE','ONTF',
        'ONTO','OOMA','OPA','OPA.U','OPA.W','OPP','OPP-A','OPY','OR','ORA','ORAN','ORC','ORCC','ORCL','ORI','ORN','OSCR','OSG','OSH','OSI','OSI.U','OSI.W','OSK','OTIS','OUS.W',
        'OUST','OUT','OVV','OWL','OWL.T','OWL.W','OWLT','OXM','OXY','OXY.W','PAC','PAC.U','PAC.W','PACE','PACK','PAG','PAGS','PAI','PAM','PANW','PAR','PARR','PATH','PAY','PAYC',
        'PB','PBA','PBC','PBF','PBFX','PBH','PBI','PBI-B','PBR','PBR.A','PBT','PCF','PCG','PCGU','PCI','PCK','PCM','PCN','PCOR','PCP.S','PCP.T','PCPC','PCQ','PD','PDA.U',
        'PDA.W','PDAC','PDI','PDM','PDO','PDO.U','PDO.W','PDOT','PDS','PDT','PEAK','PEB','PEB-C','PEB-D','PEB-E','PEB-F','PEB-G','PEG','PEI','PEI-B','PEI-C','PEI-D','PEN',
        'PEO','PFD','PFE','PFGC','PFH','PFL','PFN','PFO','PFS','PFSI','PG','PGP','PGR','PGRE','PGTI','PGZ','PH','PHD','PHG','PHI','PHK','PHM','PHR','PHT','PHX','PIA.U','PIA.W',
        'PIAI','PIC.U','PIC.W','PICC','PII','PIM','PINE','PING','PINS','PIP.U','PIP.W','PIPP','PIPR','PJT','PK','PKE','PKG','PKI','PKO','PKX','PLAN','PLD','PLNT','PLOW','PLTR',
        'PLYM','PM','PMF','PML','PMM','PMO','PMT','PMT-A','PMT-B','PMV.U','PMV.W','PMVC','PMX','PNC','PNC-P','PNF','PNI','PNM','PNR','PNT.U','PNT.W','PNTM','PNW','POLY','PON.U',
        'PON.W','POND','POR','POST','PPG','PPL','PPT','PQG','PRA','PRE-J','PRG','PRGO','PRI','PRI-A','PRI-D','PRI-E','PRI-F','PRI-G','PRI-H','PRI-I','PRLB','PRMW','PRO','PROS',
        'PRP.S','PRP.T','PRP.U','PRP.W','PRPB','PRPC','PRS','PRT','PRTY','PRU','PSA','PSA-C','PSA-D','PSA-E','PSA-F','PSA-G','PSA-H','PSA-I','PSA-J','PSA-K','PSA-L','PSA-M',
        'PSA-N','PSA-O','PSA-P','PSB','PSB-W','PSB-X','PSB-Y','PSB-Z','PSF','PSF.W','PSFE','PSN','PSO','PSP.U','PSP.W','PSPC','PST.W','PSTG','PSTH','PSTL','PSX','PSXP','PTA',
        'PTR','PTY','PUK','PUK-A','PUK.P','PUMP','PV','PV.U','PV.W','PVG','PVH','PVL','PWR','PXD','PYN','PYS','PYT','PZC','PZN','QD','QFT.U','QFT.W','QFTA','QGEN','QS','QS.W',
        'QSR','QTS','QTS-A','QTS-B','QTWO','QUAD','QUOT','QVCC','QVCD','R','RA','RAAS','RACE','RAD','RAMP','RBA','RBA.U','RBA.W','RBAC','RBC','RBLX','RC','RC-B','RC-C','RC-D',
        'RC-E','RCA','RCB','RCC','RCI','RCL','RCS','RCUS','RDN','RDS.A','RDS.B','RDY','RE','RELX','RENN','RERE','RES','REV','REVG','REX','REX-A','REX-B','REX-C','REXR','REZI',
        'RF','RF-B','RF-C','RF-E','RFI','RFL','RFM','RFMZ','RFP','RGA','RGR','RGS','RGT','RH','RHI','RHP','RIC.U','RIC.W','RICE','RIG','RIO','RIV','RJF','RKT','RKT.U','RKT.W',
        'RKTA','RL','RLGY','RLI','RLJ','RLJ-A','RLX','RM','RMAX','RMD','RMI','RMM','RMO','RMP.P','RMT','RNG','RNGR','RNP','RNR','RNR-E','RNR-F','RNR-G','ROG','ROK','ROL','RON.U',
        'ROP','ROS.U','ROS.W','ROSS','ROT','ROT.U','ROT.W','RPAI','RPM','RPT','RPT-D','RQI','RRC','RRD','RS','RSF','RSG','RSI','RTP','RTP.S','RTP.T','RTP.U','RTP.W','RTPZ','RTX',
        'RVI','RVLV','RVT','RWT','RXN','RY','RY-T','RYAM','RYB','RYI','RYN','RZA','RZB','S','SA','SAF','SAFE','SAH','SAIC','SAIL','SAK','SAM','SAN','SAND','SAP','SAR','SAVE','SB',
        'SB-C','SB-D','SBBA','SBG','SBG.U','SBG.W','SBH','SBI','SBI.U','SBI.W','SBII','SBOW','SBR','SBS','SBSW','SC','SCCO','SCD','SCE-G','SCE-H','SCE-J','SCE-K','SCE-L',
        'SCH-D','SCH-J','SCHW','SCI','SCL','SCM','SCP.U','SCP.W','SCPE','SCS','SCU','SCV.U','SCV.W','SCVX','SCX','SD','SDHY','SE','SEA.U','SEA.W','SEAH','SEAS','SEE','SEM',
        'SEMR','SF','SF-A','SF-B','SF-C','SFB','SFBS','SFE','SFL','SFT.U','SFT.W','SFTW','SFUN','SGFY','SGU','SHAK','SHG','SHI','SHLX','SHO','SHO-F','SHO-H','SHOP','SHW','SI',
        'SID','SIG','SII','SIT-A','SITC','SITE','SIX','SJI','SJIJ','SJIV','SJM','SJR','SJT','SJW','SKI.W','SKIL','SKL.W','SKLZ','SKM','SKT','SKX','SKY','SLA.U','SLA.W','SLAC',
        'SLB','SLCA','SLF','SLG','SLG-I','SLQT','SM','SMAR','SMFG','SMG','SMHI','SMLP','SMM','SMP','SMWB','SNA','SNAP','SNDR','SNI.U','SNI.W','SNII','SNN','SNOW','SNP','SNP.U',
        'SNP.W','SNPR','SNR','SNV','SNV-D','SNV-E','SNX','SO','SOA.U','SOA.W','SOAC','SOGO','SOI','SOJB','SOJC','SOJD','SOJE','SOL','SOLN','SON','SONY','SOR','SOS','SPA.U',
        'SPA.W','SPAQ','SPB','SPCE','SPE','SPE-B','SPF.U','SPF.W','SPFR','SPG','SPG-J','SPG.U','SPG.W','SPGI','SPGS','SPH','SPL-A','SPLP','SPN-B','SPN.U','SPN.W','SPNT','SPNV',
        'SPOT','SPR','SPR.U','SPR.W','SPRQ','SPXC','SPXX','SQ','SQM','SQNS','SQSP','SQZ','SR','SR-A','SRC','SRC-A','SRE','SRE-B','SREA','SRG','SRG-A','SRI','SRL','SRLP','SRT',
        'SRV','SSD','SSL','SSTK','ST','STA-D','STA-G','STA-I','STAG','STAR','STC','STE','STE.W','STEM','STG','STK','STL','STL-A','STLA','STM','STN','STNG','STON','STOR','STP.S',
        'STP.T','STPC','STR.U','STR.W','STRE','STT','STT-D','STT-G','STVN','STWD','STZ','STZ.B','SU','SUI','SUM','SUN','SUN.W','SUNL','SUP','SUPV','SUZ','SWB.U','SWB.W','SWBK',
        'SWCH','SWI','SWK','SWM','SWN','SWT','SWX','SWZ','SXC','SXI','SXT','SYF','SYF-A','SYK','SYY','SZC','T','T-A','T-C','TAC','TAC.U','TAC.W','TACA','TAK','TAL','TALO','TAP',
        'TAP.A','TARO','TBA','TBB','TBC','TBI','TCI','TCS','TD','TDA','TDC','TDF','TDG','TDI','TDOC','TDS','TDS-U','TDW','TDW.A','TDW.B','TDY','TEAF','TECK','TEF','TEI','TEL',
        'TEN','TEO','TEVA','TEX','TFC','TFC-I','TFC-O','TFC-R','TFII','TFSA','TFX','TG','TGH','TGH-A','TGI','TGNA','TGP','TGP-A','TGP-B','TGS','TGT','THC','THG','THO','THQ',
        'THR','THS','THW','TIMB','TIN.U','TIN.W','TINV','TISI','TIXT','TJX','TK','TKC','TKR','TLG.U','TLG.W','TLGA','TLK','TLYS','TM','TMA.U','TMA.W','TMAC','TME','TMHC','TMO',
        'TMST','TMX','TNC','TNET','TNK','TNL','TNP','TNP-D','TNP-E','TNP-F','TOL','TPB','TPC','TPG.U','TPG.W','TPGS','TPGY','TPH','TPL','TPR','TPTA','TPVG','TPX','TPZ','TR','TRC',
        'TRC.U','TRC.W','TRCA','TRE.U','TRE.W','TREB','TREC','TREX','TRGP','TRI','TRN','TRNO','TROX','TRP','TRQ','TRT-A','TRT-B','TRT-C','TRT-D','TRT-P','TRTN','TRTX','TRU',
        'TRV','TS','TSE','TSI','TSLX','TSM','TSN','TSP.U','TSP.W','TSPQ','TSQ','TT','TTC','TTE','TTI','TTM','TTP','TU','TUFN','TUP','TUYA','TV','TVC','TVE','TWI','TWLO','TWN',
        'TWN.H','TWN.I','TWN.S','TWN.T','TWN.U','TWN.W','TWND','TWNI','TWNT','TWO','TWO-A','TWO-B','TWO-C','TWOA','TWTR','TX','TXT','TY','TY.P','TYG','TYL','U','UA','UAA','UAN',
        'UBA','UBER','UBP','UBP-H','UBP-K','UBS','UDR','UE','UFI','UFS','UGI','UGIC','UGP','UHS','UHT','UI','UIS','UL','UMC','UMH','UMH-C','UMH-D','UNF','UNFI','UNH','UNM',
        'UNMA','UNP','UNVR','UP','UP.W','UPH','UPH.W','UPS','URI','USA','USAC','USB','USB-A','USB-H','USB-M','USB-P','USB-Q','USB-R','USDP','USFD','USM','USNA','USPH','USX',
        'UTF','UTI','UTL','UTZ','UVE','UVV','UWM.W','UWMC','UZA','UZD','UZE','UZF','V','VAC','VAL','VAL.W','VALE','VAPO','VBF','VCIF','VCRA','VCV','VEC','VEDL','VEEV','VEI',
        'VEL','VER','VER-F','VET','VFC','VGI','VGI.U','VGI.W','VGII','VGM','VGR','VHC','VHI','VIAO','VICI','VIPS','VIST','VIV','VKQ','VLO','VLRS','VLT','VMC','VMI','VMO','VMW',
        'VNCE','VNE','VNO','VNO-K','VNO-L','VNO-M','VNO-N','VNT','VNTR','VOC','VOY-B','VOYA','VPC.U','VPC.W','VPCC','VPG','VPV','VRS','VRT','VRTV','VSH','VST','VST.A','VSTO','VTA',
        'VTN','VTOL','VTR','VVI','VVNT','VVR','VVV','VYG.U','VYG.W','VYGG','VZ','VZIO','W','WAB','WAL','WALA','WAR.U','WAR.W','WARR','WAT','WBK','WBS','WBS-F','WBT','WCC',
        'WCC-A','WCN','WD','WDH','WDI','WEA','WEC','WEI','WELL','WES','WEX','WF','WFC','WFC-A','WFC-C','WFC-L','WFC-O','WFC-Q','WFC-R','WFC-X','WFC-Y','WFC-Z','WFG','WGO','WH',
        'WHD','WHG','WHR','WIA','WIT','WIW','WK','WLK','WLKP','WLL','WM','WMB','WMC','WMK','WMS','WMT','WNC','WNS','WOR','WOW','WPC','WPC.S','WPC.T','WPC.U','WPC.W','WPCA',
        'WPCB','WPF','WPF.U','WPF.W','WPG','WPG-H','WPG-I','WPM','WPP','WRB','WRB-E','WRB-F','WRB-G','WRB-H','WRE','WRI','WRK','WSM','WSO','WSR','WST','WTI','WTM','WTRG',
        'WTRU','WTS','WTTR','WU','WWE','WWW','WY','X','XEC','XFL-A','XFLT','XHR','XIN','XL','XOM','XPEV','XPO','XPO.U','XPO.W','XPOA','XRX','XYF','XYL','Y','YAC','YAC.U',
        'YAC.W','YALA','YELP','YETI','YEXT','YMM','YOU','YPF','YRD','YSG','YTPG','YUM','YUMC','ZBH','ZEN','ZEPP','ZETA','ZEV','ZEV.W','ZH','ZIM','ZIP','ZME','ZNH','ZTO','ZTR',
        'ZTS','ZUO','ZYME','SIXH','SIXL','SIXA','SXQG','SIXS','PFLD','SPDV','DMDV','EEMD','HDGE','SENT','DWMC','DWSH','DBLV','DWEQ','DWAW','DWUS','CWS','BEDZ','FWDB','MINC',
        'YOLO','MSOS',
        'QPX','QPT','EATZ','HOLD','VEGA','VICE','AADR','WLDR','GLIF','DIVA','BTAL','CHEP','ENFR','AMLP','AZAA','AZAJ','AZAL','AZAO','AZBA','AZBJ',
        'AZBL','AZBO','VMOT','FRDM','WIZ','BOB','SNUG','IMOM','QMOM','IVAL','QVAL','ALFA','SMCP','ACES','DTEC','EDOG','EQL','IDOG','SBIO','RDOG','SDOG','AVIG','AVMU','AVEM',
        'AVDE','AVDV','AVSF','AVUS','AVUV','KORP','TAXF','FDG','FLV','LVOL','MID','QINT','QPFF','QGRO','VALQ','ESGA','BATT','SWAN','ISWN','XBUY','IBUY','JGLD','CNBS',
        'BLOK','DIVO','DALT','ADFI','AESR','AFIF','ADME','ARKF','ARKG','ARKQ','ARKK','IZRL','ARKX','PRNT','ARKW','GYLD','DWCR','DWAT','QVM','ARCM','YPS','FLEU','VQT','ATMP',
        'CAPE','FFEU','TAPR','RODI','WIL','BFOR','BMED','BFTR','BTEK','HYMU','INMU','DYNF','LCTU','LCTD','BNE','BMLP','BKAG','BKEM','BKHY','BKIE','BKSB','BKLC','BKMC','BKSE','TDSC',
        'TDSD','TDSE','TDSA','TDSB','TOKE','EYLD','FYLD','GAA','GMOM','BLDG','FAIL','GVAL','SYLD','SOVB','TRTY','KOIN','EKAR','KNG','UAUD','UCHF','UEUR','UGBP','UJPY','DAUD',
        'DCHF','DEUR','DGBP','DJPY','GCE','OCIO','DIAL','XCEM','ECON','INCO','MUST','RECS','REVS','ESGN','ESGS','CCOR','FEUL','FLGE','GLDI','MLPO','SLVO','MLTI','AMJL','REML',
        'USOI','MLPC','DIVC','MLPE','DFNL','DINT','DUSA','DWLD','DAG','DAGXF','AGATF','AGF','ADZ','BDD','BDDXF','BOM',
        'BOMMF','BOS','DYY','DYYXF','DEE','DPU','DDP','OLO','OLOXF','SZOXF','FIEG','DGP','DZZ','DGZ','MIDE','SMLE','ESCR','EURZ','DEEF','ASHR','ASHS','HYUP','HAUZ','ESEB','ESHY',
        'JPN','HYDW','ACSG','CN','HDAW','ASHX','EASG','HDEF','EMSG','KOKU','USSG','RVNU','DEUS','QARP','SNPE','SHYL','HYLB','CRUZ','IBBJ','FIVG','HDRO','SPAK','PSY','QTUM',
        'DMRL','DMRS','DMRE','DMRI','DFAE','DFAI','DFAC','DFAU','DFUS','DFAS','DFAT','CCON','DYHG','NIFE','HIPR','QQQE','WFH','HJEN','MOON','WWOW','BMLP','EVGBC','EVSTC',
        'EVLMC','DOD','FUE','GRU','WMW','RJA','RJI','RJN','RJZ','EEH',
        'IEMD','IEMV','REDV','LIV','EOPS','FEDX','LUXE','AMER','DEFN','REC','EMQQ','ENTR','AIIQ','ERSX','AIEQ',
        'MJ','ITEQ','ETHO','HACK','SILJ','IPAY','VALT','AWAY','GERM','GAMR','IVES','DSTX','DSTL','CHGX','HYLD','FDVV','FCOR','FDRR','FGRO','FIGB','FLTB','FDLO','FMAG','FDMO',
        'FDIS','FSTA','FENY','FNCL','FHLC','FIDU','FTEC','FMAT','FREL','FCOM','FUTY','ONEQ','FPFD','FQAL','FPRO','FSST','FBND','FLRG','FVAL','FDWM','FBCG','FBCV','FDHY','FIDI',
        'FIVA','FLDR','FMIL','FSMD','FCPI','FDEV','FSMO','AFLG','AFMC','AFSM','FBT','FPA','FAUS','BICK','FBZ','FCAL','FCAN','FTCS','BUFR','BUFD','IGLD','QDEC','QMAR','YDEC',
        'YMAR','FAPR','FAUG','FDEC','FFEB','FJAN','FJUL','FJUN','FMAR','FMAY','FNOV','FOCT','FSEP','DFEB','DJUL','DMAR','DMAY','DNOV','DOCT','DAUG','DJUN','DAPR','DJAN','DSEP',
        'DDEC','FCEF','FCA','SKYY','FXD','FXG','FDTS','RNDM','FDT','FGD','FDN','FDM','DWPP','FVC','FV','IFV','DDIV','DVLU','DALI','EDOW','FDNI','FDD','ECLN','FEM','RNEM','FEMS',
        'FEMB','FXN','FTSM','ERM','TERM','FEP','FEUZ','XPND','FXO','FFR','FGM','FXH','PRME','FTHI','HYLS','FHK','HSMV','HDMV','HUSV','NFTY','FXR','FTRI','LEGR','NXTG','ILDR',
        'FPEI','FPXI','FICS','FPXE','FPX','FNI','FLM','FAN','FIW','FCG','FJP','FEX','FTC','RNLC','FTA','FLN','LGOV','FTLS','FTLB','LMBS','LDSF','FCTR','FMB','FXZ','FMK','FNX',
        'FNY','RNMC','FNK','FDL','FAB','FAD','MDIV','MMLG','MCEF','FMHI','QABA','ROBT','FTXO','CIBR','GRID','QCLN','FTXG','CARZ','FTXN','FTXH','FTXD','RDVY','FTXL','TDIV','FTXR',
        'QQEW','QQXT','QTEC','FMNY','EMLP','FPE','AIRR','RFAP','RFDI','RFEM','RFEU','FID','FRI','FTSL','FSMB','FYX','FYC','RNSC','FYT','SDVY','FKO','FCVT','FDIV','FSZ','EFIX',
        'EPRE','DEED','UCON','FIXD','FXL','TUSA','FUMB','FKU','RNDV','FXU','FVL','MARB','FVD','DVOL','BNDC','LKOR','SKOR','QLVD','MBSD','QLVE','GQRE','HYGV','TDTT','TDTF','IQDE',
        'IQDY','IQDF','GUNR','TILT','TLTD','TLTE','QDEF','QDYN','QDF','RAVI','ASET','ESGG','NFRA','ESG','QLC','QLV','FLAG','FFSG','FFTG','FFHG','FFTI','BUYZ','XDAT','FLAX',
        'FLAU','FLBR','FLCA','FLCH','FLEE','FLEH','FLFR','FLGR','FLHK','FLIN','FLIY','FLJP','FLJH','FLLA','FLMX','FLRU','FLSA','FLZA','FLKR','FLSW','FLTW','FLGB','HELX',
        'IQM','FLHY','FLMI','FLIA','FLCO','FLMB','FLBL','FTSD','FLSP','FLUD','FLCB','FLLV','FLGV','FLQE','FLQD','FLQG','FLQH','FLQL','FLQM','FLQS','GDMA','KLDW','AUSF','ONOF',
        'AGNG','DRIV','POTX','CHB','CHIQ','CHIE','CHIX','CHII','KEJI','CHIM','AQWA','CTEC','CLOU','KRMA','COPX','BUG','VPN','DAX','EBIZ','EDUT','EWEB','EMBD','FINX','BOSS',
        'ARGT','ASEA','GREK','GXF','NORW','PGAL','AIQ','GNOM','GOEX','BFIT','GXG','SNSR','LIT','LNGR','MILN','MLPX','MLPA','CHIC','CHIS','CHIH','CHIK','CHIL','CHIR','CHIU',
        'PAK','EFAS','QYLD','QYLG','EMFM','NGE','RNRG','BOTZ','RYLD','QDIV','HSPX','CATH','XYLG','XYLD','CEFA','SIL','SOCL','SDIV','DIV','ALTY','SDEM','SRET','SPFF','TFIV',
        'TFLT','EDOC','GXTG','GURU','URA','PAVE','PFFD','PFFV','HERO','YLCO','GHYB','GSST','GCOR','GTIP','GSIG','GIGB','GEM','GSIE','GSJY','GSLC','GSSC','GSEU','GSEW','GVIP',
        'GINN','JUST','GSEE','GSID','GSUS','GBIL','HIPS','XOUT','GSC','FRLG','HCRB','HLGE','RODM','RODE','ROAM','ROSC','ROUS','HMOP','HTAB','HSRT','HTRB','SNLN','INFL','HOMZ',
        'HTUS','NACP','SDGA','WOMN','TBJL','DBJA','DBOC','DSJA','DSOC','XDQQ','QTAP','FFTY','BOUT','LDRS','BUFF','TFJL','LOUP','IJAN','IJUL','IAPR','EAPR','EJAN','EJUL',
        'NJUL','NAPR','NJAN','NOCT','KAPR','KJAN','KOCT','KJUL','BMAY','BAPR','BMAR','BFEB','BJAN','BDEC','BNOV','BOCT','BAUG','BJUL','BJUN','BSEP','PMAY','PAPR','PMAR',
        'PFEB','PJAN','PDEC','PNOV','POCT','PSEP','PAUG','PJUL','PJUN','UMAY','UAPR','UMAR','UFEB','UJAN','UDEC','UNOV','UOCT','USEP','UAUG','UJUL','UJUN','EPRF','TSJA','TSOC',
        'XBAP','XDSQ','XDAP','XTAP','BIBL','IBD','FEVR','GLRY','BLES','WWJD','ISMD','RISN','RIDV','BSCQ','BSJO','XLG','RPG','RPV','RCD','RHS','RYE','RSP','RYF','RYH','RGI',
        'RTM','RYT','RYU','RFG','RFV','RZG','RZV','BSCL','BSCM','BSCR','BSJL','BSJM','BSCN','BSJN','BSCO','BSCP','BSJP','CQQQ','DEF','DJD','GSY','CZA','RYJ','EWRE','CGW','EWMC',
        'EWSC','TAN','CSD','CUT','GTO','PLW','PSR','PPA','PSMB','ADRE','BAB','BSMP','BSML','BSAE','BSMM','BSBE','BSMN','BSCE','BSMO','BSDE','BSJQ','BSMQ','BSJR','BSMR','BSCS',
        'BSJS','BSMS','BSCT','BSMT','BSCU','BSMU','PKW','PCEF','PSMC','DBA','DBB','DBC','DBE','DBV','DGL','DBO','DBP','DBS','UDN','UUP','PEY','PFM','PYZ','PEZ','PSL','PIZ',
        'PIE','PXI','PFI','PTH','PRN','DWAS','PDP','PTF','PUI','PBE','PKB','IDHQ','PXE','PBJ','PWB','PWV','PEJ','PBS','PXQ','PXJ','PJP','PSI','PSJ','PCY','BKLN','PGF','IVDG',
        'IDLB','PXF','PDN','PXH','PRF','PRFZ','PHB','PFIG','PGHY','PBD','PSP','PIO','PGJ','PSMG','IHYF','PIN','PWZ','PZA','PZT','IPKW','PICB','IMFL','PID','IIGD','IIGV',
        'KBWB','KBWD','KBWY','KBWP','KBWR','PSMM','GBLD','ERTH','QQQM','IBBQ','PNQI','QQQJ','SOXQ','PGX','PBTP','PBDM','PBEE','PBUS','PBSM','PBND','QQQ','ISDX','ISEM','IUS',
        'IUSS','IVRA','USEQ','EQAL','USLB','OMFL','OMFS','EQWL','IDHD','XSHQ','XSHD','XMLV','PBP','PHDG','SPVU','EWCO','SPGP','SPHB','SPHD','SPHQ','SPLV','SPMV','SPMO','RWL',
        'SPVM','XRLV','XSLV','EEMO','EELV','IDLV','IDMO','RWK','XMMO','XMHQ','XMVM','RWJ','PSCD','PSCC','PSCE','PSCF','PSCH','PSCI','PSCT','PSCM','XSMO','PSCU','XSVM','RDIV',
        'IVSG','CLTL','IVLC','VRIG','VRP','PVI','PHO','PBW','PWC','CVY','PGDDF','JJATF','JJUFF','NIB','JJOFF','DJP','JJCTF','BALTF','JJETF','JJGTF','JJMTF','LD','COWTF','GAZZF',
        'JJNTF','PGMFF','JJPFF','JJSSF','SGGFF','JJTFF','BWVTF','EROTF','GBBEF','AYTEF','JEMTF','GRNTF','XXVFF','JYNFF','MFLAF','EMLBF','ROLAF','RTLAF','SFLAF','INPTF','ICITF',
        'BCM','OLEM','XVZ','OILNF','GSP','IMLP','JJA','JJU','JO','JJC','BAL','JJE','JJG','JJM','COW','GAZ','JJN','PGM','JJP','JJS','SGG','JJT','VXZ','VXX','OIL','DTYS','DTYL',
        'DTUS','DTUL','DFVS','DFVL','FLAT','DLBS','DLBLF','STPP','GBB','GBUG','GRN','BTYS','SBUG','IQIN','IQSI','IQSU','CLRG','CSML','AGGP','GRES','HART','QED','QLS','MCRO','QMN',
        'QAI','MMIN','MMIT','MNA','CPI','HYLV','ULTR','ROOF','SHYG','SLQD','IBCE','GOVZ','IMTB','EPHE','QLTA','DVYA','STIP','TLH','SHY','TLT','IEI','IEF','AGZ','AGG','CMBS',
        'GNMA','GBF','GVI','MBB','SHV','TIP','GOVT','HYBB','LQDB','USHY','USIG','IDAT','ICF','ICVT','DGRO','IAGG','ILTB','IEFA','IEMG','IEUR','IPAC','IXUS','IVV','ITOT','ISTB',
        'IUSB','USRT','HEZU','IHAK','IDV','DVY','IYT','IYM','IAI','IYK','IYC','IYE','IYF','IYG','IYH','IHF','ITB','IYJ','IAK','IHI','IEO','IEZ','IHE','IYR','IAT','IYW','IYZ',
        'IYY','IDU','HYDB','IGEB','SMMV','MIDF','FIBR','CEMB','DVYE','EMHY','LEMB','SUSB','HYXF','DMXF','EMXF','EUSB','EAOA','EAOK','EAOR','EAOM','SUSL','ESML','EAGG','SUSC',
        'SX7EEX.DE','IECS','IEDI','IEFN','IEHS','IEIH','IEME','IETC','XT','STLC','STLG','STMB','STSB','STLV','EMGF','ACWF','INTF','ISCF','LRGF','SMLF','FLOT','FOVL','IFEU',
        'IFGL','REM','REZ','FXI','IDNA','HYXU','BGRN','GHYG','REET','IGE','IGN','IGV','IGM','LQD','GSG','HDV','IBHF','IBDM','IBMJ','IBTA','IBDN','IBMK','IBTB','IBDO','IBML',
        'IBTD','IBDP','IBTE','IBDQ','IBTF','IBDR','IBTG','IBDS','IBTH','IBDT','IBTI','IBDU','IBTJ','IBDV','IBTK','IBMI','IBDL','HYXE','HYG','EWY','LQDH','IGIB','IGRO','ISVL',
        'EMB','JPXN','DSI','ILF','ICSH','IGLB','ILCG','JKD','JKE','JKF','JKG','JKH','JKI','IMCB','IMCG','IMCV','IYLD','JKJ','JKK','JKL','ISCB','ISCG','ISCV','ILCB','ILCV',
        'ACWI','ACWX','CRBN','AAXJ','ACWV','EPU','AGT','EWA','EWO','EWK','EWZ','EWZS','BKF','EWC','ECH','CNYA','MCHI','ECNS','ICOL','EDEN','ESGD','EFA','EFAV','SCZ','ESGE',
        'EEM','EEMA','EEMV','EEMS','EMXC','EZU','EUFN','EUMV','IEUS','EFNL','EWQ','FM','EWG','EWGS','VEGI','FILL','RING','SDG','PICK','SLVP','EFG','EWH','INDA','SMIN','EIDO',
        'IDEV','IMTM','IQLT','ISZE','IVLU','EIRL','EIS','EWI','EWJE','EWJ','JPMV','SCJ','EWJV','TOK','EWM','EWW','EWN','ENZL','ENOR','EPP','EPOL','QAT','ERUS','KSA','EWS','EZA',
        'EWP','EWD','EWL','EWT','THD','TUR','UAE','EWU','EWUS','ESGU','SUSA','EUSA','USMV','MTUM','QUAL','SIZE','VLUE','EFV','URTH','IBB','SOXX','IRBO','IWB','IWF','AMCA','IWD',
        'IWM','IWO','IWN','IWV','IUSG','IUSV','IWC','IWP','IWR','IWS','IWY','IWL','IWX','OEF','IVW','IVE','AOA','AIA','CMF','AOK','EMIF','IEV','IOO','ICLN','RXI','KXI','IXC','IXG',
        'IXJ','EXI','IGF','MXI','IXN','IXP','WOOD','JXI','AOR','INDY','IPFF','IJK','IJH','IJJ','AOM','MUB','NYF','SUB','IJT','IJR','IJS','PFF','WPS','ISHG','IGOV','IDRV','NEAR',
        'MEAR','IGSB','JD','TFLO','IFRA','ITA','DIVB','FALN','SVAL','TECB','IWFH','BYLD','LDEM','IBHA','IBHB','IBHC','IBHD','IBHE','IBMM','IBMN','IBMO','IBMQ','SGOV','USXF',
        'XVV','XJH','XJR','KWT','IBDD','IBMP','JAAA','JSML','JMBS','VNLA','JSMD','OLD','JHSC','JHMS','JHCB','JHCS','JHMC','JHMD','JHEM','JHME','JHMF','JHMH','JHMI','JHML',
        'JHMA','JHMM','JHMT','JHMU','AMJ','BBSA','BBCA','BBAX','BBEU','BBIN','BBJP','BBMC','BBRE','BBUS','BBSC','JCTR','JCPB','JIGB','JPHY','JPME','JPSE','JPIN','JPUS','JEMA',
        'JEPI','JPGB','JIG','JMUB','JSCP','JAGG','JPST','JMST','JDIV','JMIN','JMOM','JQUA','JVAL','JPMB','JPEM','KBND','KBA','KCCB','KFVG','KBUY','KFYP','KWEB','KARS',
        'KMED','KEMQ','KTEC','KURE','KALL','KGRN','KESG','KEMX','OBOR','KSTR','LSAF','CACG','YLDE','CFCV','LRGE','INFR','LVHI','LVHD','SQLV','WINC','CNCR','CHNA','SECT','BIZD',
        'BBH','BRF','XMPT','CBON','CNXT','EGPT','HYEM','EMAG','EMLC','EVX','ANGL','BJK','GRNB','HYD','IDX','ITM','IHY','FLTR','ISRA','GDXJ','SMOG','DURA','GOAT','MOTI','MOAT',
        'MORT','MAAX','CRAK','OIH','PPH','PFXF','REMX','RAAX','RTH','RSXJ','HAP','SMH','SHYD','SMB','SLX','GDX','RSX','FRAK','ESPO','VNM','CNY','URR','DRR','INR','LFEQ','AFK',
        'MOO','MLN','NLR','IDIV','XDIV','FNGS','BNKD','NRGD','GDXD','BNKU','NRGU','GDXU','MJO','MJJ','FNGZ','FNGO','FNGD','FNGU','GNAF','MLPY','TMFC','MFMS','MXDU','RBIN','RBUS',
        'LSST',
        'EQOP','VNMC','VNSE','NETL','NUAG','NUEM','NUDM','NULG','NULV','NUMG','NUMV','NUSC','NUBD','NUSA','NURE','OEUR','OGIG','OSCV','OUSM','OUSA','OVB',
        'OVF','OVLH','OVL','OVM','OVT','OVS','USAI','SRVR','INDS','VIRS','HERD','SZNE','AFTY','ICOW','ECOW','GCOW','PBUG','ALTL','PALC','PAMC','VETS','LSLT','SLT','PSCW','PSCX',
        'PSFM','PSFD','PSFF','PSMR','PSMD','PTNQ','PTMC','PTLC','PTEU','TRND','PTIN','PTBD','COWZ','BUL','PEXL','CALF','PWS','FLRT','PAB','PHYL','PQIN','PQLC','PQSG','PQSV',
        'PULS','HYS','STPZ','LTPZ','ZROZ','TIPZ','MINT','EMNT','MUNI','CORP','LDUR','MFEM','MFDX','MFUS','RAFE','SMMU','BOND','PIFI','MAGA','TCTL','YLD','BTEC','PDEV','PXUS',
        'IG','GENY','PSET','PY','PREF','PQDI','PSC','USI','PLRG','USMC','PLTL','TOLZ','EQRR','PEX','IGHG','ALTS','EFAD','EMDV','EUDV','ANEW','QQQA','ONLN','PAWZ','SMDV','TMDV',
        'NOBL','REGL','TDV','EMSH','TQQQ','UTES','IPOS','IPO','RVRS','RFCI','RFUN','RFDA','RFFC','RIGS','ROBO','THNQ','HTEC','RJA','RJZ','DEEP','MVP','SUBZ','BETZ',
        'NERD','SPXB','SPXE','SPXN','SPXV','SPXT','SDY','CEFS','SCHK','SCHJ','SCHI','SCHE','FNDE','FNDF','FNDC','FNDB','FNDX','FNDA','SCHR','SCHY','SCHF','SCHC','SCHQ','SCHO',
        'SCHZ','SCHB','SCHD','SCHX','SCHG','SCHV','SCHM','SCHH','SCHA','SCHP','PFIX','QQC','QQD','SPYC','SPD','SPUC','SVOL','VCLO','VFIN','VPOP','VCAR','DFND','LEAD','SPQQ',
        'BLCN','SPBO','SPEU','SPHY','SPTI','SPMB','SPGM','SPIP','SRLN','RBND','TIPX','BIL','CWB','EMHC','EBND','JNK','IBND','BWX','FLRN','SJNK','BWZ','BILS','WIP','XLY','XLP',
        'DWFI','EMTL','STOT','TOTL','RWO','DIA','RWX','RWR','XLE','FEZ','SMEZ','XITK','XLF','DGT','XLV','XLI','XLB','SYE','SYG','SYV','CWI','LOWC','EFAX','QEFA','EEMX','QEMM',
        'QUS','QWLD','TFI','SHM','MBND','HYMB','SPAB','SPDW','SPEM','SPIB','SPLG','SPLB','SPTL','SPMD','SPYG','SPYD','SPYV',
        'SPTM','SPSM','SPSB','SPTS','XLRE',
        'ONEV','ONEO','ONEY','MMTM','VLU','MDYG','MDYV','SPYB','SPY','SPYX','SLY','SLYG','SLYV','XAR','KBE','XBI','KCE','GXC','EDIV','EWX','WDIV','GII','GNR','XHE','XHS','XHB',
        'KIE','DWX','GWX','MDY','NANR','XES','KRE','XNTK','XWEB','XME','XOP','XPH','XRT','XSD','XSW','XTH','XTL','XTN','SHE','GAL','INKM','RLY','ULST','LGLV','SMLV','XLK','XLU',
        'PSK','XLC','CNRG','ROKT','FITE','SIMS','KOMP','HAIL','ZCAN','ZDEU','ZHOK','ZJPN','ZGBR','FISR','XLSR','EFIV','SPSK','SPUS','SPRE','GLDB','HNDL','ROMO','SSPY','SMDY',
        'SSLY','SYUS','ZIG','AWTM','TPAY','EBLU','TPYP','TTAI','DFNV','DFHY','TTAC','FIEE','FIHD','FBGX',
        'MLPS','LBDC','MLPZ','BDCL','MLPQ','MLPL','AMNA','AMTR',
        'AMUB','AMU','MLPI','MLPB','MLPG','UCIB','UBN','UBG','UBM','UBC','PTM','USV','UCI','PYPE','XVIX','DVHI','DJCI','MRRL','HDLV','HDLV','SMHD','SMHD','RWXL','DVYL','DVYL',
        'SDYL','SDYL','LRET','LRET','CEFL','CEFL','DVHL','DVHL','MORL','MORL','LMLP','LMLP','WTID','WTIU','VQTS','SPGH','OILX','BDCS','MLPW','BDCZ','FMLP','FFIU','GOAU','JETS',
        'GLCN','DAPP','MIG','GLIN','MBBB','BUZZ','EINC','VCR','VDC','VIG','VWOB','VWO','VDE','VSGX','ESGV','VCEB','VEA','VGK','EDV','VXF','VFH','VEU','VSS','VNQI','VUG','VHT',
        'VYM','VIS','VGT','BIV','VCIT','VGIT','VIGI','VYMI','VV','BLV','VCLT','VGLT','VAW','MGC','MGK','MGV','VO','VOT','VOE','VMBS','VPL','VNQ','VONE','VONG','VONV','VTWO',
        'VTWG','VTWV','VTHR','VOO','VOOG','VOOV','IVOO','IVOG','IVOV','VIOO','VIOG','VIOV','BSV','VCSH','VGSH','VTIP','VB','VBK','VBR','VTEB','VOX','BND','VTC','VXUS','BNDX',
        'VTI','BNDW','VT','VFLQ','VFMV','VFMO','VFMF','VFQY','VFVA','VUSB','VPU','VTV','EXIV','EVIX','DGAZ','DWTIF','DGLD','DSLV','DWT','UWT','UGLD','UGAZF','UGAZ','USLVF',
        'TVIX','TVIXF','ZIV','VIIX','ULBR','DLBR','UTRN','CIZ','VSDA','CEY','CID','CIL','QQQN','SHLD','VTRN','CFO','CFA','CSF','CDC','CDL','VSMV','CSA','CSB','UITB',
        'USTB','UEVM','UIVM','USVM','ULVM','VBND','VUSE','VIDI','PPTY','PFFR','PFFA','BBC','BBP','VABS','BLHY','NFLT','VPC','VRAI','SEIX','JOET','VWID',
        'VSL','WBIT',
        'WBIN','WBIE','WBIL','WBIF','WBIG','WBIY','WBIH','WBII','WBIR','NTSX','HYIN','AGGY','AGND','USFR','HYZD','SHAG','CXSE','WCLD','WCBR','DWM','DTH','DTN','EPS','EMCB',
        'DGS','RESE','DEM','DGRE','NTSE','XSOE','EUDG','DFE','SFIG','SFHY','WFIG','WFHY','DEW','DNL','DRW','DHS','EPI','IXSE','AGZD','DOO','NTSI','RESD','DOL','DIM','IQDG',
        'DLS','DFJ','DLN','DON','EZM','PLAT','MTGP','EES','DTD','DES','RESP','USMF','QSY','DGRW','DGRS','YYY']
        for m in member_list:
            print(timezone.now()) #take this out
            print(m + "\n")
            url = "https://www.marketwatch.com/investing/stock/" + m + "/"
            page = requests.get(url).text
            soup = BeautifulSoup(page, "lxml")
            summary_entries = [entry.text for entry in soup.find_all('span', {'class':"primary"} or {'class':"primary is-na"})]
            prices = [entry.text for entry in soup.find_all('td', {'class':"table__cell u-semi"})]
            num_entries = len(summary_entries)

            if(Member.objects.filter(ticker=m).exists()):
                object = Member.objects.get(ticker=m)
                object.last_updated = timezone.now()
                object.save()
                print(str(object.ticker) + " " + str(object.price) + "\n")
                if(num_entries == 22):
                    if "$" in str(prices[0]):
                        t1 = summary_entries[14]
                        t2 = summary_entries[15]
                        the_price = prices[0]
                        print(str(the_price) + "\n")
                        eps_temp = str(summary_entries[15]).replace('$',"")
                        if((str(t1) == "N/A")and(str(t2) == "N/A")):
                            object.price = str(the_price).replace("$","").replace(",","")
                        elif(str(t1) == "N/A"):
                            object.price = str(the_price).replace("$","").replace(",","")                           
                            object.eps=eps_temp.replace(",","")
                        elif(str(t2) == "N/A"):
                            object.price = str(the_price).replace("$","").replace(",","")                          
                            object.pe_ratio=str(summary_entries[14]).replace(",","")
                        else:
                            object.price = str(the_price).replace("$","").replace(",","")
                            object.pe_ratio=str(summary_entries[14]).replace(",","")
                            object.eps=eps_temp.replace(",","")
                        object.save()
                        print(m + " was updated successfully \n")
                elif(len(summary_entries) >= 14 and not (len(prices) == 0)):
                    if("/" in str(summary_entries[14]) and len(prices) > 0):
                        if "$" in str(prices[0]):
                            object.price = str(prices[0]).replace("$","").replace(",","")
                            object.save()

                        print(m + " was updated with only price and ticker\n")
                else:
                        print(m + " was found but had unexpected html format, not updated in the database\n")
            else:
                if(num_entries == 22):
                    #prev_close = summary_entries[11]
                    #open = summary_entries[12]
                    #bid = summary_entries[13]
                    #ask = summary_entries[14]
                    #volume = summary_entries[15]
                    #avg_volume = summary_entries[16]
                    #mkt_cap = summary_entries[17]
                    #beta_5y_monthly = summary_entries[18]
                    #pe_ratio = summary_entries[19]
                    #eps = summary_entries[20]
                    #y_target = summary_entries[21]
                    # print(
                    # "Previous close: " + prev_close + "\n" + 
                    # "Open: " + open + "\n" + 
                    # "Bid: " + bid + "\n" + 
                    # "Ask: " + ask + "\n" + 
                    # "Bolume: " + volume + "\n" + 
                    # "Average volume: " + avg_volume + "\n" + 
                    # "Market cap: " + mkt_cap + "\n" + 
                    # "Beta (5Y monthly): " + beta_5y_monthly + "\n" + 
                    # "PE ratio: " + pe_ratio + "\n" + 
                    # "EPS: " + eps + "\n" + 
                    # "1 year target: " + y_target + "\n")

                    if Member.objects.filter(ticker=m).exists():
                        pass
                        print(m + " was repeated in the list\n")
                    else:
                        if "$" in str(prices[0]):
                            t1 = summary_entries[14]
                            t2 = summary_entries[15]
                            the_price = prices[0]
                            eps_temp = str(summary_entries[15]).replace('$',"")
                            if((str(t1) == "N/A")and(str(t2) == "N/A")):
                                Member.objects.create(
                                    price = str(the_price).replace("$","").replace(",",""),
                                    ticker=m,
                                    last_updated = timezone.now()
                                )
                            elif(str(t1) == "N/A"):
                                Member.objects.create(
                                    price = str(the_price).replace("$","").replace(",",""),                            
                                    ticker=m,
                                    eps=eps_temp.replace(",",""),
                                    last_updated = timezone.now()
                                )
                            elif(str(t2) == "N/A"):
                                Member.objects.create(
                                    price = str(the_price).replace("$","").replace(",",""),                            
                                    ticker=m,
                                    pe_ratio=str(summary_entries[14]).replace(",",""),
                                    last_updated = timezone.now()
                                )
                            else:
                                Member.objects.create(
                                    price = str(the_price).replace("$","").replace(",",""),
                                    ticker=m,
                                    pe_ratio=str(summary_entries[14]).replace(",",""),
                                    eps=eps_temp.replace(",",""),
                                    last_updated = timezone.now()
                                )
                            print(m + " was added successfully \n")
                elif(len(summary_entries) >= 14 and not (len(prices) == 0)):
                    if("/" in str(summary_entries[14]) and len(prices) > 0):
                        if "$" in str(prices[0]):
                            Member.objects.create(
                                price = str(prices[0]).replace("$","").replace(",",""),
                                ticker=m,
                                last_updated = timezone.now()
                            )
                            print(m + " was added to the database with only price and ticker\n")
                else:
                    print(m + " had unexpected html format, not added to the database\n")
        for profile in Profile.objects.all():
            profile.total = 0
            print("Computing profile total for: " + profile.user.username + "\n")
            for asset in profile.assets.all():
                for member in Member.objects.all():
                    if(member.ticker == asset.name):
                        asset.last_updated = member.last_updated
                        asset.save()
                        print(asset.last_updated)
                        profile.total += (member.price * asset.quantity)
                        print(str(asset.quantity) + " shares of " + asset.name + " added to the profile total\n")
            print("Done computing profile total for: " + profile.user.username + "\n")
            print("Total for " + profile.user.username + " is: " + str(profile.total))
            profile.save()
                
        end = time.perf_counter()
        print("time: " + str((end-start)))
        self.stdout.write( 'Completed') 