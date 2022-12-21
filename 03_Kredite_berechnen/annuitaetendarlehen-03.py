import pandas as pd

def berechne_jaehrliche_Annuitaet(kreditsumme, zinssatz, tilgung):
    """ Berechnet die _jährliche_ Annuität.
        Jährliche_Rate = (nominalzins in proz + tilgungssatz in proz) * Kreditsumme
        Quelle: https://de.wikipedia.org/wiki/Annuit%C3%A4tendarlehen
    """ 

    return round((zinssatz + tilgung) * kreditsumme, 2)

    
def tilgungsplan(kreditsumme, zinssatz, tilgung, jahre):
    """
    Erstellt den Tilgungsplan
    """

    tilgplan = pd.DataFrame(columns=['Jahr', 'Rate', 'Zinsen', 'Tilgung', 'Restschuld'])
    annuitaet = berechne_jaehrliche_Annuitaet(kreditsumme, zinssatz, tilgung)
    print(f'{annuitaet=}\n')
    
    # Am Anfang entspricht die Restschuld der Kreditsumme
    restschuld = kreditsumme
    
    for jahr in range(1, jahre+1):
        zinsen = restschuld * zinssatz
        tilgung = restschuld if restschuld <= annuitaet else annuitaet - zinsen    
        rate = zinsen + tilgung

        restschuld = restschuld - tilgung
        zeile = pd.DataFrame([{'Jahr':jahr, 'Rate':rate, 'Zinsen':zinsen, 
                               'Tilgung':tilgung, 'Restschuld':restschuld}])
        
        tilgplan = pd.concat([tilgplan, zeile])

    tilgplan=tilgplan.set_index(['Jahr']) 
    return tilgplan
    

df = tilgungsplan(120000, 0.1, 0.25, 4)
print(df)
df.to_excel('annuitaetendarlehen-03.xlsx')
