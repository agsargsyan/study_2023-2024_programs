#Finish procedure
proc finish {} {
   global ns nf
   $ns flush-trace
   close $nf
   global tchan_
   #разделение данных мгновееной очереди и средней очереди
   set awkCode {
      {
	 if ($1 == "Q" && NF>2) {
	    print $2, $3 >> "output/temp.q";
	    set end $2
	 }
	 else if ($1 == "a" && NF>2)
	 print $2, $3 >> "output/temp.a";
      }
   }
	
   set f [open output/temp.queue w]
   puts $f "TitleText: RED"
   puts $f "Device: Postscript"

   if { [info exists tchan_] } {
      close $tchan_
   }

   exec rm -f output/temp.q output/temp.a 
   exec touch output/temp.a output/temp.q

   exec awk $awkCode output/all.q

   puts $f \"queue
   exec cat output/temp.q >@ $f
   puts $f \n\"ave_queue
   exec cat output/temp.a >@ $f
   close $f
   # вывод графиков в xgraph для быстрого просмотра
   exec xgraph -bb -tk -x time -t "TCPRenoCWND" output/WvsT &
   exec xgraph -bb -tk -x time -t "TCPRenoCWND_1" output/WvsT_1 &
   exec xgraph -bb -tk -x time -t "RTT" output/RTT &
   exec xgraph -bb -tk -x time -t "RTTVAR" output/RTTVAR &
   exec xgraph -bb -tk -x time -y queue output/temp.queue &
   #exec nam output/out.nam &
   exit 0
}



 
