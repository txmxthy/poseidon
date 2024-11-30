from typing import Dict, Any

def get_progress_bar_settings(desc: str, unit: str, color: str) -> Dict[str, Any]:
    """Get standardized progress bar settings."""
    return {
        "desc": desc,
        "unit": unit,
        "colour": color,
        "unit_scale": True,
        "unit_divisor": 1000,
        "bar_format": "{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]"
    }

# Predefined progress bar configurations
MESSAGE_COUNTER = {
    **get_progress_bar_settings("Counting messages", " msgs", "cyan"),
    "unit_scale": False
}

MESSAGE_PROCESSOR = {
    **get_progress_bar_settings("Processing messages", " msgs", "green")
}

VESSEL_ANALYZER = {
    **get_progress_bar_settings("Analyzing vessels", " vessels", "blue")
}

GEOJSON_CREATOR = {
    **get_progress_bar_settings("Creating GeoJSON features", " features", "magenta")
}