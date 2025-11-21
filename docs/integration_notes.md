# Integration Notes

## Overview
This file documents challenges and observations during the integration of:
- OSINT AI data center coordinates
- eGRID subregion boundaries
- EIA generator-level capacity data

---

## 1. Geospatial Boundary Issues
- Several AI data centers lie close to subregion borders.
- Two Amazon facilities in Virginia map ambiguously to both RFCE and SRVC.
- Google Council Bluffs facility overlaps between MRO and SPP polygons depending on precision.

**Solution:**  
Using polygon containment with a 4-decimal-place precision reduces ambiguity. Manual review required for 6 sites.

---

## 2. Inconsistent Region Identifiers
- eGRID uses "SRVC", "RFCW", etc.
- EIA balancing authorities use different codes.

**Solution:**  
Created a lookup table (to be finalized) that maps:
- eGRID → EIA BA → State-level grouping

---

## 3. Missing Coordinates in OSINT Data
- 8% of entries lacked coordinates.
- Geocoding filled most but left 3 entries unresolved due to vague addresses.

**Solution:**  
Flag remaining entries in `osint_ai_centers.csv` under column `geocode_status`.

---

## 4. Outliers in Capacity (MW)
- One data center incorrectly listed as 6000 MW.
- Corrected to 600 MW.

**Solution:**  
Outlier detection via IQR on `estimated_power_MW`.

---

## 5. Data Join Logic
Integration pipeline order:

1. OSINT dataset cleaned  
2. Geocode missing entries  
3. Convert to GeoDataFrame  
4. Spatial join with eGRID polygons  
5. Merge with EIA generator capacity  
6. Produce final integrated dataset  

---

## To-Do
- Finalize region lookup table
- Add confidence score for geocoding
- Add automated mismatch detector for border cases
