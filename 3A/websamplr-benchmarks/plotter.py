import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd

# df = pd.read_csv("benchmark.csv")
# df["websamplr_memory_usage"] = df["websamplr_memory_usage"].map(lambda x: x / 2**20)  # on Mb
# df["samplr_memory_usage"] = df["samplr_memory_usage"].map(lambda x: x / 2**20)  # on Mb
# 
# ax = df['websamplr_cpu_percent'].plot(legend="WebSamplr")
# ax = df['samplr_cpu_percent'].plot(legend="Samplr")
# ax.yaxis.set_major_formatter(mtick.PercentFormatter())
# 
# wscpup = list()
# scpup = list()
# sum1, sum2 = 0, 0
# 
# for i, (v1, v2) in enumerate(
#     zip(df["websamplr_cpu_percent"], df["samplr_cpu_percent"])
# ):
#     sum1 += v1
#     sum2 += v2
#     if i % 7 == 0:
#         wscpup.append(sum1/5)
#         scpup.append(sum2/5)
#         sum1 = 0
#         sum2 = 0
# 
# 
# 
# fig, ax = plt.subplots()
# plt.plot(wscpup)
# plt.plot(scpup)
# plt.legend(['WebSamplr', 'Samplr'])
# 
# # ax.yaxis.set_major_formatter(mtick.PercentFormatter())
# plt.ylabel('% CPU')
# plt.xlabel('time(s)')
# plt.show()
# 
# 
# ax = df['websamplr_memory_usage'].plot(legend="WebSamplr")
# ax = df['samplr_memory_usage'].plot(legend="Samplr")
# plt.ylabel('RSS memory in MB')
# plt.xlabel('time(s)')
# plt.show()


# df = pd.read_csv("network_benchmarks.csv")

# df['latencies'].plot(legend="WebSamplr")
# print(len(df['latencies']))
# plt.show()
# df['bandwidth'].plot(legend="Samplr")
# print(len(df['bandwidth']))
# plt.show()


df = pd.read_csv("power_usage.csv", delimiter=';')
samplr = []
websamplr = []
usage_ms = []
print(df)
import numpy as np
for usage in df['usage']:
    measure, unity = usage.strip().split(' ')
    if unity == 'us/s':
        usage_ms.append(float(measure) / 1000)
    else:
        usage_ms.append(float(measure))
df.insert(0, 'fmt_usage', usage_ms)
print(df)

for desc in df['description']:
    if 'websamplr' in desc:
        websamplr.append(True)
        samplr.append(False)
    else:
        websamplr.append(False)
        samplr.append(True)

print(df[websamplr]['fmt_usage'])
print(df[samplr]['fmt_usage'])

print(df[websamplr]['fmt_usage'].mean(skipna=True))
print(df[samplr]['fmt_usage'].mean(skipna=True))
# 
# df[websamplr]['fmt_usage'].rename('WebSamplr Usage').plot(legend='WebSamplr')
# df[samplr]['fmt_usage'].rename('Samplr Usage').plot(legend='Samplr')
# 
# plt.ylabel('Usage in ms/s')
# plt.xlabel('time (s)')
# plt.show()
# print(df[websamplr]['fmt_usage'].mean())
# print(df[samplr]['fmt_usage'].mean())
# 
