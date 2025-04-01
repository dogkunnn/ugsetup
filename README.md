<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>คัดลอกคำสั่ง Delta</title>
</head>
<body>
    <h2>📋 คัดลอกคำสั่ง</h2>
    <button onclick="copyToClipboard()">คัดลอก</button>
    <script>
        function copyToClipboard() {
            const text = 'su -c "cd /storage/emulated/0/Download && export PATH=$PATH:/data/data/com.termux/files/usr/bin && export TERM=xterm-256color && python c.py"';
            navigator.clipboard.writeText(text).then(() => {
                alert("✅ คัดลอกคำสั่งเรียบร้อย!");
            });
        }
    </script>
</body>
</html>
