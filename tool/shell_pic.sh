echo $1;
rm -rf $1/img/output;
mkdir $1/img/output;
echo "output:"$1
echo "resize photos"
cd $1/img
find . -type f -name "*.jpg"|xargs -I {} convert -resize 1240x1240 {} output/{}
echo "compress photos"
cd output
find . -type f -name "*.jpg"|xargs -I {} jpegoptim  -m80 {}


