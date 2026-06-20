# Position On The Full Controlled Release

The full local package contains AOI boundaries, community names, provider-derived identifiers or metadata when present, and remote-sensing image chips. These components are useful for reproducible research, but they create privacy, licensing, and misuse risks if placed in an unrestricted public repository.

## Recommended Release Model

Do not publish the full raw package as an unrestricted GitHub repository.

Instead, maintain a separate controlled-access repository or landing page containing:

- dataset card
- data-use agreement
- access-request form
- file manifest and checksums
- ethics policy
- examples using synthetic or open OSM/GEE data
- instructions for approved users to obtain encrypted archives

The archives themselves should be distributed only after review under a non-commercial DUA, using access-controlled storage rather than public GitHub downloads.

## Minimum DUA Restrictions

Approved users must agree not to:

- redistribute raw AOI geometries, names, addresses, provider IDs, or imagery
- attempt resident or compound re-identification beyond approved research needs
- use the data for surveillance, targeting, policing, commercial real-estate profiling, or geofencing
- publish precise coordinates, polygons, or per-compound sensitive metadata
- combine the data with resident-level or household-level records

Approved outputs should be aggregate, privacy-preserving, and clearly scoped to research use.

