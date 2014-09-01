f=$(find . -name "*.pdf")

for i in $f ; do
convert $i $i.jpg
done