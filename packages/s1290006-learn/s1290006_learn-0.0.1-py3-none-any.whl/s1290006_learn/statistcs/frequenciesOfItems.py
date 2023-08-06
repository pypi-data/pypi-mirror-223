import pandas as pd

class frequenciesOfItems():
    def frequenciesOfItems(self):
        col_names = ['header{0:02d}'.format(i) for i in range(503)]
        df = pd.read_csv("./PM24HeavyPollutionRecordingSensors.csv", names=col_names)
        df["header00"] = df["header00"].str.strip("['")
        df["header00"] = df["header00"].str.strip("']")
        countdf = df.value_counts(subset=['header00'], sort=True)
        return countdf
    
if __name__ == "__main__":
    freq = frequenciesOfItems()
    print(freq.frequenciesOfItems())
