#!/usr/bin/env bash

###############################################################################
# Starts/stops the Apollo modules DoppelTest exercises: routing, prediction,
# planning, and the simplified_planning node that republishes a trimmed
# ADCTrajectory on /apollo/planning/simplified (the full message is too large
# for the cyber bridge's single-recv framing).
#
# Installed into the Apollo checkout by scripts/install_apollo.sh and invoked
# from apollo/ApolloContainer.py. It is maintained here because the v7_mozart
# branch does not carry DoppelTest-specific scripts.
###############################################################################

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "${DIR}/.."

# Make sure supervisord has correct coredump file limit.
ulimit -c unlimited

source "${DIR}/apollo_base.sh"

function start() {
  ./scripts/routing.sh start
  ./scripts/prediction.sh start
  ./scripts/planning.sh start
  nohup /apollo/bazel-bin/modules/custom_nodes/simplified_planning &
}

function stop() {
  ps -ef | grep -E 'planning|routing|prediction|simplified_planning|cyber_bridge' | grep -v 'grep' | awk '{print $2}' | xargs -r kill -9
}

case $1 in
  start)
    start
    ;;
  stop)
    stop
    ;;
  restart)
    stop
    start
    ;;
  *)
    start
    ;;
esac
