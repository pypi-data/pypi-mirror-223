import src.BeyotekTools.speedlimit as SpeedLimit

count = 0

while True:
    SpeedLimit.speedlimit(1000)
    print(f" {count} Seconds")
    count+=1