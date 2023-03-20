import pandas as pd

a = [1,2,3,4,5,6,7,8,9,10]

# pandas save as csv
df = pd.DataFrame(a)
df.to_csv('test.csv', index=False)

