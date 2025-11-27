import json
import pandas as pd
from datetime import datetime, date
import os

from api.logic import pesos_horarios_pred
from api.daily_logic import calcular_E_dia


def handler(request):

    fecha = request.get("query", {}).get("fecha", None)

    if fecha is None:
        return {"status": 400, "body": json.dumps({"error": "Falta parámetro fecha"})}

    try:
        f = datetime.strptime(fecha, "%Y-%m-%d").date()
    except:
        return {"status": 400, "body": json.dumps({"error": "Formato inválido"})}

    MESES_ES = [
        "enero","febrero","marzo","abril","mayo","junio",
        "julio","agosto","septiembre","octubre","noviembre","diciembre"
    ]
    mes_nombre = MESES_ES[f.month - 1]

    path = os.path.join("data", "predicciones_2025.csv")
    df = pd.read_csv(path)
    df["MES"] = df["MES"].str.lower().str.strip()

    fila = df[(df["MES"] == mes_nombre) & (df["ANIO"] == f.year)]

    if fila.empty:
        return {"status": 404, "body": json.dumps({"error": "No hay predicción para ese mes"})}

    E_mes = float(fila["PREDICCION"].iloc[0])

    FERIADOS = [
        date(2025,1,1),
        date(2025,4,18),
        date(2025,5,1)
    ]

    E_dia, _ = calcular_E_dia(E_mes, fecha, FERIADOS)

    horas = pesos_horarios_pred()
    horas["pred_hora"] = E_dia * horas["p_hora"]

    resp = {
        "fecha": fecha,
        "mes": mes_nombre,
        "anio": f.year,
        "E_mes": round(E_mes),
        "E_dia": round(E_dia),
        "horas": horas.to_dict(orient="records")
    }

    return {
        "status": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(resp)
    }
