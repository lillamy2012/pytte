pass=zBLOf2@7
user=Elin.Axelsson

#wget --auth-no-challenge --http-user=$user --http-password=$pass http://ngs.csf.ac.at/#sequencedSamples/group/berger -O seq.tab


awk -F $'\t' '{if(NR>1 && $10!~"Failed") print $1"_"$11,$48,$49,$51, $52}' seq.tab | sort | uniq > flowWlane.tab

awk -F $'\t' '{if(NR>1 && $10!~"Failed") print $1"_"$11}' seq.tab | sort | uniq > uniqFl.tab


while read fl path rest ; do
    full=$(ls /Users/elin.axelsson/berger_group/lab/Raw/multiplexed | grep $fl)
    full2=$(basename "$path")
    if [ "$full" == "$full2" ]
    then
        echo $fl $rest $full
    fi

done < flowWlane.tab

#> test.tab