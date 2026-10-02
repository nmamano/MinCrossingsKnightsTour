# kill my band/band2 processes above 6.5 GB RSS (KT Edge Searcher)
while true; do
  for pid in $(pgrep -u nil -x band2) $(pgrep -u nil -x band); do
    rss=$(ps -o rss= -p $pid 2>/dev/null | tr -d ' ')
    if [ -n "$rss" ] && [ "$rss" -gt 6800000 ]; then kill $pid; echo "$(date) killed $pid rss=$rss" >> watchdog.log; fi
  done
  pgrep -u nil -f q_ext.sh > /dev/null || pgrep -u nil -x band2 > /dev/null || exit 0
  sleep 5
done
