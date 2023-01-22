"""
Vergleich der Tilgungspläne bei 1% Sollzins bzw. 4% Zollzins

"""
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
df1 = tilgungsplan(250000, 0.01, 0.05, 500)
df2 = tilgungsplan(205000, 0.04, 0.05, 500)

zins1 = round(df1["Zinsen"].sum(),2)
zins2 = round(df2["Zinsen"].sum(),2)

ratensumme1 = round(df1["Rate"].sum(),2)
ratensumme2 = round(df2["Rate"].sum(),2)



print( f'{zins1} EUR Gesamtzinsen\n')
print( f'{zins2} EUR Gesamtzinsen\n')


print(f'Verh�ltnis der Zinsen2/Zinsen1: {round(zins2/zins1,2)}\n')


print( f'{ratensumme1} EUR Gesamtkosten\n')
print( f'{ratensumme2} EUR Gesamtkosten\n')


print(f'Verh�ltnis der Gesamtkosten: {round(ratensumme2/ratensumme1,2)}\n')



#print(df) # Ausgabe am Bildschirm
#df.to_excel('annuitaetendarlehen-04.xlsx')
#df.to_html('annuitaetendarlehen-04.html', float_format='%10.2f')
