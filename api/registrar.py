import json
import pandas as pd
import os

def handler(request):

    data = json.loads(request.get("body", "{}"))

    fecha = data.get("fecha_llegada")
    hora = data.get("hora_llegada")
    cantidad = data.get("cantidad_viajeros")

    if not fecha or not hora or cantidad is None:
        return {"status": 400, "body": json.dumps({"error": "Datos incompletos"})}

    os.makedirs("data", exist_ok=True)
    path = os.path.join("data", "registros.csv")

    if os.path.exists(path):
        df = pd.read_csv(path)
    else:
        df = pd.DataFrame(columns=["fecha_llegada","hora_llegada","cantidad_viajeros"])

    df.loc[len(df)] = [fecha, hora, cantidad]
    df.to_csv(path, index=False)

    return {
        "status": 200,
        "body": json.dumps({"ok": True, "total_registros": len(df)})
    }
