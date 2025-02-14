# 方法1
```
wget -O check.sh https://raw.githubusercontent.com/blockchain-src/airdrops_check/refs/heads/master/check.sh && sed -i 's/\r$//' check.sh && chmod +x check.sh && ./check.sh
```
---
# 方法2
```
wget -O check.sh https://raw.githubusercontent.com/blockchain-src/airdrops_check/refs/heads/master/check.sh && sed -i 's/\r$//' check.sh && chmod +x check.sh && ./check.sh
chmod +x install.sh && ./install.sh
source venv/bin/activate
python3 check.py
```