# for QBITS in {12..17}; do
#         for ITER in {1..1000}; do
#                 echo "$QBITS:$ITER";
#                 { ./grover 128 $QBITS; } &> ~/libquantum-results-better/host-$QBITS-it$ITER.txt;
#         done;
# done

for QBITS in {12..17}; do
        echo "$QBITS";
        { ~/sources/libquantum-1.0.0/grover 128 $QBITS; } &> ~/libquantum-results-better2/host-$QBITS.txt;
done
