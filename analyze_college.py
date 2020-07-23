import numpy as np
import pandas as pd

def _get_data():
  cols = ["Name",\
          "Enrollment",\
          "State","Ranking List","Rank","Rank Pct Rank","Undergraduate Admit Rate","Undergraduate Admit Rate Pct Rank","Average Monthly Search Volume","Average Monthly Search Volume Pct Rank",\
          "Credential Score","Student Life Grade","Student Life Score","Experience Score","15-Year NPV","15-Year NPV PCT Rank","30-Year NPV","30-Year NPV PCT Rank","Instructional Wages per Full-Time Student",\
          "Instructional Wages per Full-Time Student PCT Rank",\
          "Eduation Score","Average Undergraduate Tuition","Average Undergraduate Tuition Score","Value-to-Cost Ratio","Endowment per Full Time Student","Endowment per Full Time Student Pct Rank",\
          "Percentage of International Students","Percentage of International Students PCT Rank","Vulnerability Score","Prof G Categorization"]

  data = np.genfromtxt('college_data.dat',delimiter=';',dtype=None,encoding='utf-8')
  df = pd.DataFrame(data)
  return df
#df.applymap(lambda x: x.decode() if isinstance(x, bytes) else x)

if __name__ == '__main__':
  df = _get_data()
  print(df[df.f28 == 'Perish'].to_string())
  print(df[df.f28 == 'Struggle'].to_string())
  print(df[df.f28 == 'Thrive'].to_string())

  sname = ' '
  while sname != "":
    sname = input("Give School (return to end): ")
    if sname == "": break
    print(df[df.f0.str.contains(sname)].to_string())

