#! /usr/bin/env bash
path="$HOME/.pack"
mkdir "$path"
cp pack.py "$path"
echo "export PATH=$path:\$PATH" >> "$HOME/.profile"
echo "#! /usr/bin/env bash" > "$path/pack"
echo "dir=\"\$(dirname \"\$0\")\"" >> "$path/pack"
echo "cd \"\$dir\"" >> "$path/pack"
echo "python3 \$dir/pack.py \"\$@\"" >> "$path/pack"
echo "[pack]" > $path/pack.toml
chmod u+x "$path/pack"
echo "Done!"
