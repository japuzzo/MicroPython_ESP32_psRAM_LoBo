import machine, network, utime
tmo = 0

# Local NTP server to your country
#Worldwide	pool.ntp.org
#Asia	asia.pool.ntp.org
#Europe	europe.pool.ntp.org
#North America	north-america.poo
#South America	south-america.pool.ntp.org
#Oceania	oceania.pool.ntp.org
#United States us.pool.ntp.org
ntps = "pool.ntp.org"

# to try different AP (WiFi Access Points) put AP name followed by password
# use as many pairs as you need this will try one by one to connect to AP
# login = {'ap1': 'ap1-password', 'ap2': 'ap2-password', 'ap3': 'ap3-password'}

# If you want to try just one you can do:
login = {'ap': 'password'}

# Set login to false to go directly to AP mode:
# login = False

# AP mode settings
ap_essid='micropython'
ap_channel=11

if login:
    print("Starting WiFi ...")
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    print(sta.scan())
    for ap, pas in login.items():
        sta.connect(ap,pas)
        print("Trying",ap)
        tmo = 20
        while not sta.isconnected():
            utime.sleep_ms(250)
            tmo -= 1
            if tmo == 0:
                sta.disconnect()
                break

# Enable next line to see how many tries it took to connext
# print("tmo=",tmo)

if tmo > 0:
    current_ip=sta.ifconfig()
    print("WiFi Connected to [", ap, "] with IP=",current_ip[0])
    rtc = machine.RTC()
    print("Synchronize time from NTP server ...")
    rtc.ntp_sync(server=ntps)
    tmo = 100
    while not rtc.synced():
        utime.sleep_ms(100)
        tmo -= 1
        if tmo == 0:
            break
    if tmo > 0:
        utime.sleep_ms(500)
        t = rtc.now()
        print("Time set to",utime.strftime("%c"))
        print("")

# If there was NO AP login then start board in Access Point mode
# You can then connect to this board as an AP when no AP login is available
if tmo == 0:
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ap_essid, channel=ap_channel)
    ap_ip = ap.ifconfig()
    print("WiFi started in AP mode as [", ap_essid, "] at IP=", ap_ip[0])

# Start up Telnet server for remote REPL connection
if network.telnet.start():
    print ("Telnet Started")

# Start up FTP server for remote file upload and download
if network.ftp.start():
    print ("FTP Started")
