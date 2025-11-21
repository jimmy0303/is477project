import pandas as pd
import sys

osint_path = sys.argv[1]
egrid_path = sys.argv[2]
eia_path = sys.argv[3]
out_path = sys.argv[4]

osint = pd.read_csv(osint_path)
egrid = pd.read_csv(egrid_path)
eia = pd.read_csv(eia_path)

# Very simplified merge placeholder
osint["dummy_region"] = "SRVC"
egrid["dummy_region"] = "SRVC"

merged = osint.merge(egrid, on="dummy_region", how="left")

merged.to_csv(out_path, index=False)
