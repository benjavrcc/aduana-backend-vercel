import json
import pandas as pd
import os

def handler(request):
    path = os.path.join("data", "registros.csv")

    if not os.path.exists(path):
        return {"status": 200, "body": json.dumps({"total_registros": 0, "registros": []})}

    df = pd.read_csv(path)

    return {
        "status": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "total_registros": len(df),
            "registros": df.to_dict(orient="records")
        })
    }
