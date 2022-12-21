import pandas as pd

def berechne_monatliche_Annuitaet(kreditsumme, zinssatz, tilgung):
    """ Berechnet die _monatliche_ Annuität.
        Jährliche_Rate = (nominalzins + tilgungssatz) * Kreditsumme
        Monatliche_Rate = Jährliche_Rate / 12
    """ 
    return round((zinssatz + tilgung) * kreditsumme / 12, 2)


def tilgungsplan(kreditsumme, zinssatz, tilgung, monate):
    """
    Erstellt den Tilgungsplan und gibt ihn als DataFrame zurück
    """

    tilgplan = pd.DataFrame(columns=['Monat', 'Rate', 'Zinsen', 'Tilgung', 'Restschuld'])
    annuitaet = berechne_monatliche_Annuitaet(kreditsumme, zinssatz, tilgung)
    print(f'\n{annuitaet} EUR monatliche Annuität\n')
    # Am Anfang entspricht die Restschuld der Kreditsumme
    restschuld = kreditsumme
    
    for monat in range(1, monate+1):
        zinsen = restschuld * (zinssatz / 12 )
        tilgung = restschuld if restschuld < annuitaet else annuitaet - zinsen    
        rate = zinsen + tilgung
        restschuld = restschuld - tilgung
        
        zeile = pd.DataFrame([{'Monat':monat, 'Rate':rate, 'Zinsen':zinsen,
                               'Tilgung':tilgung, 'Restschuld':restschuld}])
        
        tilgplan = pd.concat([tilgplan, zeile])

    tilgplan['Jahr'] = ((tilgplan['Monat'] - 1 ) // 12 ) + 1
   
    tilgplan=tilgplan.set_index(['Monat'])
    return tilgplan


#Beispiel mit S=250K, 2,5% Zins und 5% Tilgung
df = tilgungsplan(250000, 0.025, 0.05, 250)

print( f'{round(df["Zinsen"].sum(),2)} EUR Gesamtzinsen\n')

print(df) # Ausgabe am Bildschirm
df.to_excel('annuitaetendarlehen-04.xlsx')
df.to_html('annuitaetendarlehen-04.html', float_format='%10.2f')
