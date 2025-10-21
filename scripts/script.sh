pythonPath="$HOME/.sortME/main.py"
echo "Sort This Directory ? "
read buffer
DIRECTORY="$HOME"

export CURRENTDIRECTORY="$(pwd)"

if [[ "$buffer" == "y" ]] ; then
    DIRECTORY=$(pwd)
else
    echo "Enter The Directory for Sorting :: "
    read D
    DIRECTORY=D
fi

LSOUTPUT=$(ls -1 "$DIRECTORY" 2>/dev/null | tr '\n' ' ')
json=$(echo "$LSOUTPUT" | python ../src/main.py)
echo "File Structure is as Follows :: "
echo "$json"
