import pandas as pd

def berechne_monatliche_Annuitaet(kreditsumme, zinssatz, tilgung):
    """ Berechnet die _monatliche_ Annuität.
        Jährliche_Rate = (nominalzins + tilgungssatz) * Kreditsumme
        Monatliche_Rate = Jährliche_Rate / 12
    """ 
    return round(kreditsumme * (zinssatz + tilgung) / 12, 2)


def tilgungsplan(kreditsumme, zinssatz, tilgung, monate, sondertilgung, wartezeit):
    """
    Erstellt den Tilgungsplan als Excel
    """

    tilgplan = pd.DataFrame(columns=['Monat', 'Rate', 'Zinsen', 'Tilgung', 
                                  'Sondertilgung', 'Restschuld'])
    annuitaet = berechne_monatliche_Annuitaet(kreditsumme, zinssatz, tilgung)
    print(f'{annuitaet=}\n')
    # Am Anfang entspricht die Restschuld der Kreditsumme
    restschuld = kreditsumme
    
    for monat in range(1, monate+1):
        zinsen = restschuld * (zinssatz / 12 )
        tilgung = restschuld if restschuld < annuitaet else annuitaet - zinsen    
        rate = zinsen + tilgung
        restschuld = restschuld - tilgung
        
        wert_sondertilgung = 0.0
        
        # Sondertilgung berücksichtigen im Dezember
        if monat % 12 == 0 and restschuld > sondertilgung and monat > wartezeit:
            restschuld = restschuld - sondertilgung
            wert_sondertilgung = sondertilgung
        elif monat % 12 == 0 and restschuld <= sondertilgung and monat > wartezeit:
            wert_sondertilgung = restschuld
            restschuld = 0        
       
        
        zeile = pd.DataFrame([{'Monat':monat, 'Rate':rate, 'Zinsen':zinsen,
                               'Tilgung':tilgung, 'Sondertilgung': wert_sondertilgung,  
                               'Restschuld':restschuld}])
        
        tilgplan = pd.concat([tilgplan, zeile])
            

    tilgplan['Jahr'] = ((tilgplan['Monat'] - 1 ) // 12 ) + 1
    tilgplan=tilgplan.set_index(['Monat'])
    return tilgplan


df1 = tilgungsplan(247000, 0.0234, 0.015, 320, 2500+12*241.88, 119)
df2 = tilgungsplan(45000, 0.0245, 0.04, 320, 2500,0)


df1=df1.add_suffix('_gr') # große Tranche 
df2=df2.add_suffix('_kl') # kleine Tranche

df = pd.concat([df1,df2],axis=1)
df = df.drop('Jahr_kl',axis=1) # Feld ist überflüssig
df['Gesamtrate'] = df['Rate_gr'] + df['Rate_kl']
df['Gesamt-Restschuld'] = df['Restschuld_gr'] + df['Restschuld_kl']

df.to_excel('annuitaetendarlehen-06.xlsx')
