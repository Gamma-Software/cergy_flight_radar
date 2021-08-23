#!/bin/bash
cd "$(dirname "${BASH_SOURCE[0]}")"

git add flights_over_cergy.csv
git commit -m "Update flight database over cergy"
git push git@github.com:Gamma-Software/cergy_flight_radar.git develop
echo 'database pushed'
