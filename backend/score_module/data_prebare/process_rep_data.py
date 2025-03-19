import pandas as pd 
import json 
import numpy as np


class process_rep_data:
    def __init__(self,df:pd.DataFrame):
        self.df = df
        self.df.columns = ['Age' , 'L1' , 'L2' , 'L3' , 'L4' , 'L5' , 'L6' , 'L7' ]
    

    def Split(self , df:pd.DataFrame):
        for i in df.columns[1:]:
            df[f'{i}_min'] = df[i].str.split(pat='to').str[0]
            df[f'{i}_max'] = df[i].str.split(pat='to').str[1]
            df.drop(columns=[i] , inplace=True)

        return df
    
    def handle_str_values(self, df: pd.DataFrame):
        for i in df.columns[1:]:
            df[i] = df[i].astype(str).str.replace("\n", "", regex=True)
            df[i] = df[i].astype(str).str.replace("<", "")
            df[i] = df[i].astype(str).str.replace("times", "")
            df[i] = df[i].astype(str).str.replace(">", "")  # Remove ">"
            df[i] = df[i].astype(str).str.strip()  # Remove leading/trailing spaces
        return df
            
    
    def convert_to_int(self, df):
        for i in df.columns:
            try:
                df[i] = pd.to_numeric(df[i], errors='coerce')  # Convert invalid values to NaN
                df[i] = df[i].fillna(0).astype(int)  # Fill NaNs with 0 and convert to int
            except Exception as e:
                print(f"Error converting column {i} to int: {e}")
        return df

    def dataframe_to_json(self, df, filename="structured_data.json"):
        structured_data = {}

        for _, row in df.iterrows():
            age = int(row["Age"])  # Convert age to int for better readability
            structured_data[age] = {}  # Initialize age group

            # Process columns dynamically
            for col in df.columns[1:]:
                category, range_type = col.rsplit("_", 1)  # Extract category and type (min/max)
                if category not in structured_data[age]:
                    structured_data[age][category] = {}

                value = row[col]

                # Ensure all values are JSON serializable
                if isinstance(value, (np.int64, np.float64)):
                    value = value.item()  # Convert to native Python type

                structured_data[age][category][range_type] = value

        # Save to JSON file
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(structured_data, f, indent=4)

        print(f"JSON file saved as: {filename}")

        return structured_data
    
    def process(self , path):

        self.df = self.Split(self.df)
        self.df.drop(columns=['L7_max'] , inplace=True)
        self.df.rename(columns={'L7_min':'L7_max'} , inplace=True)
        self.df = self.handle_str_values(self.df)
        self.df = self.convert_to_int(self.df)
        self.json = self.dataframe_to_json(self.df , path)

        return self.json



#balance = pd.read_csv('balance_1.csv')
curl_up = pd.read_csv('curlup_0.csv')
pushUp = pd.read_csv('pushup_0.csv')

"""balance_object = process_rep_data(balance)
balance_json = balance_object.process('balance.json')

print(balance_json)"""

curl_up_object = process_rep_data(curl_up)
curl_up_json = curl_up_object.process('curl_up.json')

print(curl_up_json)

pushUp_object = process_rep_data(pushUp)
push_up_json = pushUp_object.process('pushUp.json')

print(push_up_json)