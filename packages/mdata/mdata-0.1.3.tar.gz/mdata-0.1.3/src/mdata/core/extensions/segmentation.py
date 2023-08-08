"""
per object, specify list of time intervals
design decision:
    segments as split points = fully dividing timespan and thus containing "dead-zones" - can be modeled around by e.g. regarding only every second segment as real
    segments as possibly non-touching intervals, dead-zones explicitly modeled
    what about observations outside defined segments? disallow this?
replace multiplicity? or derive it from segment definitions?
"""