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


df1 = tilgungsplan(20000, 0.0519, 1/6, 72, 12*200, 0)

df1.to_clipboard(decimal=',')
