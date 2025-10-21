pythonPath="$HOME/.sortME/main.py"
echo "Sort This Directory ? "
read buffer
DIRECTORY="$HOME"

if [[ "$buffer" == "y" ]] ; then
    DIRECTORY=$(pwd)
else
    echo "Enter The Directory for Sorting :: "
    read "$DIRECTORY"
fi

LSOUTPUT=$(ls -1 "$DIRECTORY" 2>/dev/null | tr '\n' ' ')
JSONOUTPUT=$(echo "$LSOUTPUT" | python main.py)
echo "$JSONOUTPUT"
echo "$JSONOUTPUT" | jq -r '.read.files[]'
