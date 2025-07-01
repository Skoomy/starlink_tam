# starlink_tam


## 1. Context & Purpose

`The aim`: build a top-down model to estimate Starlink’s total addressable market (TAM), based on both supply (bandwidth capacity) and demand (willingness to pay), while allowing transparent adjustments of assumptions.


## 2. Core model inputs

- **Supply‑Side Inputs**
	•	Constellation size: number of satellites in orbit (e.g. 12,000; SpaceX has requested up to 42,000).
	•	Bandwidth per satellite: Mbps capacity that each satellite can deliver.
	•	Oversubscription ratio: accounts for the fact not all users are online simultaneously.
	•	Minimum bandwidth threshold: ensures a baseline quality of service.

- **Demand‑Side Inputs**
	•	Price tolerance: modeled as a percent of monthly GDP (~2%) that consumers are willing to pay for broadband service.
	•	Local broadband speeds: Starlink will either match current average speeds or default to the minimum threshold.
	•	Willingness to pay vs GDP: allows comparability across countries and income levels().


## 3. Modeling Mechanics

**Supply Calculation:**
	1.	Country’s share of global land surface determines share of satellites overhead.
	2.	Multiply satellites × bandwidth per satellite gives total bandwidth available per country.

**Demand Estimation:**
	1.	Divide available bandwidth by required average bandwidth per customer.
	2.	Multiply by the oversubscription ratio to get number of potential customers per market.

**Revenue Projection:**
	•	Annual revenue = number of customers × 2% of that country’s average monthly GDP (price point).

**Sanity Check**
	- Compare implied market penetration vs total population and especially rural population.
	- Exclude countries with unrealistic adoption potential or regulatory hurdles().


## 5. Limitations and Strategic Implications

    Model draws only on residential demand; mobility (maritime, aviation, ships) is excluded but noted as a potential major upside due to lack of terrestrial competition in open oceans().
	Model outputs are highly sensitive to:
		 - Satellite count & bandwidth capability
	    - Oversubscription efficiency
	    - Subscriber willingness to pay relative to income
	    - Regulatory and adoption risk especially in developing markets or rural regions.

## References

https://medium.com/@skorusARK/modeling-the-addressable-market-for-starlink-ff1409066589
