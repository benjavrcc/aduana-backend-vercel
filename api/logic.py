import pandas as pd

def pesos_horarios_pred():
    horas = pd.DataFrame({"hora": range(24)})
    horas["PESO_HORA"] = horas["hora"].apply(
        lambda h: 0.5 if h in range(0,6) else 
                  1.5 if h in range(6,12) else
                  2.5 if h in range(12,19) else
                  1.0
    )
    horas["p_hora"] = horas["PESO_HORA"] / horas["PESO_HORA"].sum()
    return horas
