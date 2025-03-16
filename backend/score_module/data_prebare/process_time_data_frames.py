import pandas as pd 
import json 
import numpy as np


class process_time_data:
    def __init__(self,df:pd.DataFrame):
        self.df = df
        self.df.columns = ['Age' , 'L1' , 'L2' , 'L3' , 'L4' , 'L5' , 'L6' , 'L7' ]
    

    def Split(self , df:pd.DataFrame):
        for i in df.columns[1:]:
            df[f'{i}_min'] = df[i].str.split(pat='to').str[1]
            df[f'{i}_max'] = df[i].str.split(pat='to').str[0]
            df.drop(columns=[i] , inplace=True)

        return df
    
    def handle_str_values(self , df:pd.DataFrame):
        for i in df.columns[1:]:
            df[i] = df[i].astype(str).str.replace("\n", " ", regex=True)
            df[i] = df[i].astype(str).str.replace("<", "")
            df[i] = df[i].astype(str).str.replace("m", " ")
            df[i] = df[i].astype(str).str.replace("s", " ")
            df[i] = df[i].astype(str).str.replace("ms", "")
            df[i] = df[i].astype(str).str.replace(r"\s+", ",", regex=True)
            df[i] = df[i].str.replace(r"^\s*,|,\s*$", "", regex=True)

        return df
    
    def convert_to_ms(self , time_arr):
        try:
            m = int(time_arr[0]) * 60 * 1000  
            s = int(time_arr[1]) * 1000       
            ms = int(time_arr[2])             
            return m + s + ms
        except (ValueError, IndexError):
            return None  # Return None if the value is invalid
        
    
    def apply_convert(self , df):
        time_columns = [col for col in df.columns if col != 'Age']

        # Apply conversion to all columns
        for col in time_columns:
            df[col] = (
                df[col]
                .astype(str)  # Ensure it's a string
                .str.split(",")  # Convert to a list
                .apply(lambda x: self.convert_to_ms([i.strip() for i in x if i.strip()]) if len(x) == 3 else None)  # Clean and convert
            )
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
        self.df.drop(columns=['L7_min'] , inplace=True)
        self.df = self.handle_str_values(self.df)
        self.df = self.apply_convert(self.df)
        self.json = self.dataframe_to_json(self.df , path)

        return self.json



plate = pd.read_csv('plate_1.csv')
run = pd.read_csv('run_0.csv')
speed = pd.read_csv('speed_table.csv')

plate_object = process_time_data(plate)
plate_json = plate_object.process('plate.json')

print(plate_json)

run_object = process_time_data(run)
run_json = run_object.process('run.json')

print(run_json)

speed_object = process_time_data(speed)
speed_json = speed_object.process('speed.json')

print(plate_json)