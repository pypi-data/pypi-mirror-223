import src.BeyotekTools.speedlimit as speedlimit

speedLimit = speedlimit.limiter()

count = 0

while True:
    speedLimit.limit(1000)
    print(f" {count} Seconds")
    count+=1