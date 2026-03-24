import spidev


class selectSoil_moisture :

  def __init__(self):
  # Open Spi Bus
  # SPI 버스 0과 디바이스 0을 열고
  # 최대 전송 속도를 1MHz로 설정
    self.mositure_channel = 7
    self.spi = spidev.SpiDev()
    self.spi.open(0,0) # open(bus, device)
    self.spi.max_speed_hz = 1000000 # set transfer speed

# To read SPI data from MCP3008 chip
# Channel must be 0~7 integer
  def readChannel(self): 
    val = self.spi.xfer2([1, (8+ self.mositure_channel)<<4, 0])
    data = ((val[1]&3) << 8) + val[2]
    return data

# 0~1023 value가 들어옴. 1023이 수분함량 min값
  def convertPercent(self, data):
    return 100.0 - round(((data*100)/float(1023)),1)

  def run(self, conn):
    val = self.readChannel()
    percent= self.convertPercent(val)
    if (val != 0) : # filtering for meaningless num
      print(percent,"%")
      
    with conn.cursor() as cursor : 
      sql = "INSERT INTO namuwiki.SOIL_MOISTURE(SOIL_MOISTURE_VALUE) VALUES (%s)"
      cursor.execute(sql, (percent,))

