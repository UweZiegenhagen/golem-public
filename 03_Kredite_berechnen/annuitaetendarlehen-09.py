import pandas as pd

def berechne_monatliche_Annuitaet(kreditsumme, zinssatz, tilgung):
    """ Berechnet die _monatliche_ Annuität.
        Jährliche_Rate = (nominalzins + tilgungssatz) * Kreditsumme
        Monatliche_Rate = JÃ¤hrliche_Rate / 12
    """ 
    return round((zinssatz + tilgung) * kreditsumme / 12, 2)


def tilgungsplan(kreditsumme, zinssatz, tilgung, monate):
    """
    Erstellt den Tilgungsplan und gibt ihn als DataFrame zurück
    """

    tilgplan = pd.DataFrame(columns=['Monat', 'Rate', 'Zinsen', 'Tilgung', 'Restschuld'])
    annuitaet = berechne_monatliche_Annuitaet(kreditsumme, zinssatz, tilgung)
    print(f'\n{annuitaet} EUR monatliche AnnuitÃ¤t\n')
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


df1 = tilgungsplan(20000, 0.0519, 1/6, 72)

zins1 = round(df1["Zinsen"].sum(),2)

ratensumme1 = round(df1["Rate"].sum(),2)

print(df1)
print( f'{zins1} EUR Gesamtzinsen\n')
print( f'{ratensumme1} EUR Gesamtkosten\n')


#print(df) # Ausgabe am Bildschirm
df1.to_excel('annuitaetendarlehen-09.xlsx')
df1.to_clipboard(decimal=',')

#df2.to_html('annuitaetendarlehen-04.html', float_format='%10.2f')
