export customer_hash=Example-413539ece39485afc35b4a469adfde0a279d2fd2

apt-get update 
apt-get install wget
cd /usr/share/keyrings 
wget https://collaboraoffice.com/downloads/gpg/collaboraonline-release-keyring.gpg && \
    
cat << EOF > /etc/apt/sources.list.d/collaboraonline.sources
Types: deb
URIs: https://www.collaboraoffice.com/repos/CollaboraOnline/23.05/customer-deb-$customer_hash
Suites: ./
Signed-By: /usr/share/keyrings/collaboraonline-release-keyring.gpg
EOF

apt-get update 
apt-get install collaboraofficebasis-python-script-provider -y
apt-get install collaboraofficebasis-pyuno -y