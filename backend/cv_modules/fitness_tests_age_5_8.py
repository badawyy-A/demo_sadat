from pose_model import process_video_pose_estimation
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import time
import cv2
import numpy as np
import time

# Coordination (Plate Tapping Test)

# done
class PlateTappingTest:
    def __init__(self, video_path):
        #self.df , self.fps = process_video_pose_estimation(video_path)  # Work on a copy to avoid modifying the original DataFrame
        try:
            self.df, self.fps = process_video_pose_estimation(video_path)
            if self.df.empty:
                print("⚠️ Warning: The DataFrame is empty! Check process_video_pose_estimation.")
        except Exception as e:
            print(f"Error processing video: {e}")
        #self.df, self.fps = pd.DataFrame(), 0

        self.peaks = None
        self.valleys = None
        self.starting_tap = None
        self.total_duration = 0

    def detect_peaks_and_valleys(self):
        """Find peaks (left taps) and valleys (right taps) in the angle data."""
        self.peaks, _ = find_peaks(self.df['kp_x10'], prominence=16, height=250, distance=5)
        self.valleys, _ = find_peaks(-self.df['kp_x10'], prominence=70)
        
        # Assign positions based on detected peaks and valleys
        self.df['position'] = 'on-move'
        self.df.loc[self.valleys, 'position'] = 'right'
        self.df.loc[self.peaks, 'position'] = 'left'

    def plot_peaks(self):
        """Visualize detected peaks and valleys."""
        plt.figure(figsize=(18, 10))
        plt.plot(self.df['kp_x10'], label='kp_x10')
        plt.plot(self.peaks, self.df['kp_x10'][self.peaks], "x", markersize=10, label="Peaks")
        plt.plot(self.valleys, self.df['kp_x10'][self.valleys], "x", markersize=10, label="Valleys")
        plt.xlabel("Frame")
        plt.ylabel("Angle (degrees)")
        plt.title("Peaks of 'kp_x10' Over Time")
        plt.legend()
        plt.grid(True)
        plt.show()

    def filter_positions(self):
        """Eliminate incorrect consecutive tap classifications."""
        frames_to_reset = []
        last_position = None  
        df_filtered = self.df[self.df['position'] != 'on-move']

        for i, row in df_filtered.iterrows():
            if last_position is None:
                last_position = row["position"]
                prev_row = row
                continue
                
            if row["position"] == last_position:
                if row['kp_x10'] > prev_row['kp_x10']:
                    frames_to_reset.append(prev_row['frame_idx'])
                else:
                    frames_to_reset.append(row['frame_idx'])
                    
            prev_row = row
            last_position = row["position"]
                    
        self.df.loc[frames_to_reset, 'position'] = 'on-move'

    def find_starting_tap(self):
        """Identify whether the test starts with the left or right hand."""
        first_tap = self.df[self.df['position'] != 'on-move'].iloc[0]
        self.starting_tap = first_tap['position']
        #print(f"\nThe tapping starts with the {self.starting_tap} hand.")

    def detect_cycles(self):
        """Detect and count full tapping cycles with their duration."""
        self.df['cycle_status'] = 'in-progress'
        self.df['frame_count'] = 0
        self.df['duration_sec'] = 0
        self.df['cycle'] = 0  

        indices = self.df[self.df['position'] != 'on-move'].index.tolist()
        cycle_count = 0

        for i in range(2, len(indices)):  
            prev_tap = self.df.loc[indices[i-2], 'position']
            mid_tap = self.df.loc[indices[i-1], 'position']
            curr_tap = self.df.loc[indices[i], 'position']

            if prev_tap == self.starting_tap and mid_tap != self.starting_tap and curr_tap == self.starting_tap:
                cycle_count += 1
                self.df.loc[indices[i], 'cycle_status'] = 'completed-cycle'
                self.df.loc[indices[i], 'frame_count'] = self.df.loc[indices[i], 'frame_idx'] - self.df.loc[indices[i-2], 'frame_idx']
                self.df.loc[indices[i], 'duration_sec'] = self.df.loc[indices[i], 'frame_count'] / self.fps
                self.df.loc[indices[i], 'cycle'] = cycle_count  

    def run_test(self):
        """Execute all steps of the plate tapping test."""
        print("Columns in DataFrame:", self.df.columns)
        self.detect_peaks_and_valleys()
        #self.plot_peaks()
        self.filter_positions()
        self.find_starting_tap()
        self.detect_cycles()
        self.total_duration = self.df['duration_sec'].sum().round(2)

        return self.total_duration

# Example usage:
"""video_path = "plate-tapping/plate_21.mp4"
test = PlateTappingTest(video_path)
result = test.run_test()
print(result)
"""



# Balance (Flamingo Balance Test)



# to be updated
"""class FlamingoBalance:
    def __init__(self, video_path, threshold_time=0.05):
        self.video_path = video_path
        self.df, self.fps = self.process_video_pose_estimation(video_path)
        

    def balance_loss(self, pose_row, prefered_foot):
        left_ankle_y = pose_row.get('kp_y15')
        left_hip_y = pose_row.get('kp_y11')
        left_knee_y = pose_row.get('kp_y13')

        right_ankle_y = pose_row.get('kp_y16')
        right_hip_y = pose_row.get('kp_y12')
        right_knee_y = pose_row.get('kp_y14')
        # to continue

    
    def count_falls(self):
        continue
"""


# another approch
class FlamingoBalance:
    def __init__(self, video_path):
        #self.df , self.fps = process_video_pose_estimation(video_path)  # Work on a copy to avoid modifying the original DataFrame
        try:
            self.df, self.fps = process_video_pose_estimation(video_path)
            if self.df.empty:
                print("⚠️ Warning: The DataFrame is empty! Check process_video_pose_estimation.")
        except Exception as e:
            print(f"Error processing video: {e}")

        self.peaks = None
        self.falls = 0
        # plot kp_y15
        self.prominence_value = 0.15 * (self.df['kp_y15'].max() - self.df['kp_y15'].min())  # 15% of range
        self.height_value = np.percentile(self.df['kp_y15'], 85)  # Peaks above the 85th percentile


    def detect_peaks_and_valleys(self):
        """Find peaks (left taps) and valleys (right taps) in the angle data."""
        self.peaks, _ = find_peaks(self.df['kp_y15'], prominence= self.prominence_value,height= self.height_value)
        
        # Assign positions based on detected peaks and valleys
        self.df['state'] = 'balance'
        self.df.loc[self.peaks, 'state'] = 'fall'

    def plot_peaks(self):
        """Visualize detected peaks and valleys."""
        plt.figure(figsize=(18, 10))
        plt.plot(self.df['kp_y15'], label='kp_y15')
        plt.plot(self.peaks, self.df['kp_y15'][self.peaks], "x", markersize=10, label="Peaks")
        plt.xlabel("Frame")
        plt.ylabel("Angle (degrees)")
        plt.title("Peaks of 'kp_y15' Over Time")
        plt.legend()
        plt.grid(True)
        plt.show()

    
    def process(self):
        """Get Falls Count."""
        self.detect_peaks_and_valleys()
        self.plot_peaks()
        self.falls = len(self.df[self.df['state'] == 'fall'])

        return self.falls

# Example usage:
"""flamingo_balance = FlamingoBalance(video_path="flamingo/f11_e.mp4")
fall_count = flamingo_balance.process()
print(f"Total Falls: {fall_count}")"""
