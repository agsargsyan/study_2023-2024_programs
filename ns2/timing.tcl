for {set r 0} {$r < $N} {incr r} {
	$ns at 0.0 "$ftp($r) start"
	$ns at 100.0 "$ftp($r) stop"
	$ns at 1.0 "plotMetric $tcp($r) $windowVsTime cwnd_"
	$ns at 1.0 "plotMetric $tcp(1) $rtt rtt_"
        $ns at 1.0 "plotMetric $tcp(1) $rttvar rttvar_"
}
$ns at 1.0 "plotMetric $tcp(1) $windowVsTime_1 cwnd_"
#$ns at 1.0 "plotMetric $tcp(1) $rtt rtt_"
#$ns at 1.0 "plotMetric $tcp(1) $rttvar rttvar_"
$ns at 100.0 "finish"

