#!/usr/bin/env python3
"""Charm the Commuter: Forecast a City That Isn't — make.fun program entry.

Competition: u-golden-heron-44-charm-the-commuter-forecast-a-city-4018259e.

One weather forecast, in one line under 140 characters, for a city
that does not exist. A factory builds a writer closure around the
approved forecast; calling it checks the gate, files the line as
entry.txt and forecast.txt, and proves both copies match by digest.
"""

import hashlib
import sys

FORECAST = (
    "Today in Nowhere City: sunny with a 90% chance of rain, because "
    "the forecast got bored and started making things up."
)


def make_forecast_writer(line, low=1, high=140):
    """Return a writer closure bound to one approved forecast line."""
    blob = None

    def checked_blob():
        nonlocal blob
        if blob is not None:
            return blob
        size = len(line)
        if size < low or size > high:
            raise ValueError(
                "forecast is %d chars, gate is %d-%d" % (size, low, high)
            )
        if line.strip() == "":
            raise ValueError("forecast is only whitespace")
        if "\n" in line or "\r" in line:
            raise ValueError("forecast must be a single line")
        blob = line.encode("utf-8")
        return blob

    def write():
        data = checked_blob()
        for name in ("entry.txt", "forecast.txt"):
            with open(name, "wb") as fh:
                fh.write(data)
        for name in ("entry.txt", "forecast.txt"):
            with open(name, "rb") as fh:
                if fh.read() != data:
                    raise IOError("%s differs from the approved line" % name)
        return hashlib.sha256(data).hexdigest()

    return write


def main(argv):
    if len(argv) > 1 and argv[1] == "--forecast":
        print("forecast (%d chars): %s" % (len(FORECAST), FORECAST))
        return 0
    write = make_forecast_writer(FORECAST)
    digest = write()
    print("wrote %d chars, sha256 %s" % (len(FORECAST), digest))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
