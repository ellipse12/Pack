#! /usr/bin/env bash
path="$HOME/.pack"
mkdir "$path"
cp pack.py "$path"
echo "export PATH=$path/pack:PATH" > "$HOME/.profile"
echo "#! /usr/bin/env bash" >> "$path/pack"
echo "dir=\"\$(dirname \"\$0\")\"" > "$path/pack"
echo "python3 \$dir/pack.py -f \$HOME/.pack/pack.toml \"\$@\""
echo "[pack]" >> $path/pack.toml
echo "Done!"
