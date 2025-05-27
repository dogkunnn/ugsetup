### for UserID.py 
```js
su -c "cd /storage/emulated/0/Download && export PATH=$PATH:/data/data/com.termux/files/usr/bin && export TERM=xterm-256color && python namepack.py"
```
### Termux boot
#### setup
```sh
mkdir -p ~/.termux/boot
echo '#!/bin/bash
su -c "export PATH=\$PATH:/data/data/com.termux/files/usr/bin && export TERM=xterm-256color && cd /storage/emulated/0/Download && python ./Rejoin.py" <<EOF
1
180
EOF' > ~/.termux/boot/abcd.sh
```
#### delete 
```js
rm ~/.termux/boot/abcd.sh
```
