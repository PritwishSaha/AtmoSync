# AtmoSync Commodity Storage Rules
#
# These are initial analytical assumptions for the project.
# They should be validated against authoritative cold-chain
# references before being presented as real operational limits.


COMMODITY_RULES = {

    "Banana": {
        "temperature_min": 13.0,
        "temperature_max": 14.0,
        "humidity_min": 85.0,
        "humidity_max": 95.0
    },

    "Mango": {
        "temperature_min": 10.0,
        "temperature_max": 13.0,
        "humidity_min": 85.0,
        "humidity_max": 90.0
    },

    "Tomato": {
        "temperature_min": 10.0,
        "temperature_max": 12.0,
        "humidity_min": 85.0,
        "humidity_max": 95.0
    },

    "Avocado": {
        "temperature_min": 5.0,
        "temperature_max": 13.0,
        "humidity_min": 85.0,
        "humidity_max": 95.0
    }
}


def get_rules(commodity):
    """
    Return storage rules for a commodity.
    """

    return COMMODITY_RULES.get(commodity)