nohup sh -c '
for i in `seq 1 10`;
do time python3 ano.py $i;
done ;
'&