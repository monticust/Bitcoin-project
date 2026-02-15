import socket

seedList = ["seed.bitcoin.sipa.be","dnsseed.bluematt.me","dnsseed.bitcoin.dashjr.org","seed.bitcoinstats.com","bitseed.xf2.org","seed.bitcoin.jonasschnelli.ch",]


for seedHostName in seedList:
    
     

    try:
        seedIp= socket.gethostbyname(seedHostName)
        print (seedHostName,seedIp)

    except: 
        print (seedHostName,'couldnt get an ip address')