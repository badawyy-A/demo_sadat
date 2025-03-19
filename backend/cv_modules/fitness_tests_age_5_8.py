from .pose_model import process_video_pose_estimation
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import time
import cv2
import numpy as np
import json

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
        self.df['duration_sec'] = self.df['duration_sec'].astype(float)  # Convert column to float

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
        self.total_duration = ((self.df['duration_sec'].sum()) * 1000).round(2)

        return self.total_duration

"""# Example usage:
video_path = "test_videos/plate_g.mp4"
test = PlateTappingTest(video_path)
result = test.run_test()
print(result)"""


# another approch
"""class FlamingoBalance:
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
        #Find peaks (left taps) and valleys (right taps) in the angle data.
        self.peaks, _ = find_peaks(self.df['kp_y15'], prominence= self.prominence_value,height= self.height_value)
        
        # Assign positions based on detected peaks and valleys
        self.df['state'] = 'balance'
        self.df.loc[self.peaks, 'state'] = 'fall'

    def plot_peaks(self):
        #Visualize detected peaks and valleys.
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
        # Get Falls Count.
        self.detect_peaks_and_valleys()
        self.plot_peaks()
        self.falls = len(self.df[self.df['state'] == 'fall'])

        return self.falls"""

class FlamingoBalance:
    def __init__(self,threshold_time=0.05):

        self.start_time = None
        self.total_time = 0  
        self.balance_loss_counter = 0  
        self.in_balance = False
        self.threshold_time = threshold_time

    def balance_loss(self, pose_row, prefered_foot):
        left_ankle_y = pose_row.get('kp_y15')
        left_hip_y = pose_row.get('kp_y11')
        left_knee_y = pose_row.get('kp_y13')

        right_ankle_y = pose_row.get('kp_y16')
        right_hip_y = pose_row.get('kp_y12')
        right_knee_y = pose_row.get('kp_y14')

        if None in (left_ankle_y, left_hip_y, left_knee_y, right_ankle_y, right_hip_y, right_knee_y):
            return round(self.total_time, 2), self.balance_loss_counter

        if prefered_foot == "Right":
            supporting_ankle_y, supporting_knee_y, supporting_hip_y = right_ankle_y, right_knee_y, right_hip_y
            lifted_ankle_y, lifted_knee_y, lifted_hip_y = left_ankle_y, left_knee_y, left_hip_y
        else:
            supporting_ankle_y, supporting_knee_y, supporting_hip_y = left_ankle_y, left_knee_y, left_hip_y
            lifted_ankle_y, lifted_knee_y, lifted_hip_y = right_ankle_y, right_knee_y, right_hip_y

        ##The first condition for the side view videos and the second one for front view videos
        in_balance_now = (lifted_ankle_y < supporting_ankle_y) and (lifted_ankle_y < lifted_knee_y) or ( (lifted_ankle_y < supporting_ankle_y) and abs(lifted_ankle_y - lifted_knee_y) < 50 )

        if in_balance_now:
            if not self.in_balance:  
                self.start_time = time.time()  
            self.in_balance = True
        else:
            if self.in_balance:
                elapsed_time = time.time() - self.start_time if self.start_time else 0
                if elapsed_time >= self.threshold_time:
                    self.total_time += elapsed_time  
                    self.balance_loss_counter += 1  
                self.in_balance = False
                self.start_time = None  

        if self.in_balance and self.start_time:
            return round(self.total_time + (time.time() - self.start_time), 2), self.balance_loss_counter
        
        return round(self.total_time, 2), self.balance_loss_counter



class FlamingoBalance_Score:
    def __init__(self, video_path):
        
        try:
            self.pose_df, self.FPS = process_video_pose_estimation(video_path)
            if self.pose_df.empty:
                print("⚠️ Warning: The DataFrame is empty! Check process_video_pose_estimation.")
        except Exception as e:
            print(f"Error processing video: {e}")
        self.video_path = video_path
        #self.pose_csv_path = pose_csv_path
        self.output_path = 'output_balance_kid4.avi'
        self.flamingo_balance_test = FlamingoBalance()

        # Load CSV data
        #self.pose_df = pd.read_csv(self.pose_csv_path)
        self.loss = 0
        
        # Initialize video capture
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            raise FileNotFoundError("Error: Could not open video file.")
        
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        
        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(self.output_path, fourcc, self.fps, (self.frame_width, self.frame_height))
        self.frames_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))


    def annotate_frame(self, frame, frame_idx):
        pose_frame_data = self.pose_df[self.pose_df['frame_idx'] == frame_idx]

        pose_row = pose_frame_data.iloc[0]

            
        # Get real-time balance tracking
        total_time, loss_count = self.flamingo_balance_test.balance_loss(pose_row, "Right")
        
        if frame_idx == self.frames_count -1:
            self.loss = loss_count
            

        return frame    
    
    def process(self):
        frame_idx = 0
        while True:
            ret, frame = self.cap.read()
            if frame_idx == self.frames_count:
                break
            frame = self.annotate_frame(frame, frame_idx)
            self.out.write(frame)
            frame_idx += 1

        self.cap.release()
        
        cv2.destroyAllWindows()
        return self.loss

# Usage
# "E:/manar/data_science/fixedinternship/CV/club_city_project/flamingo/f11_e.mp4"  girl
# "E:/manar/data_science/fixedinternship/CV/club_city_project/flamingo/flagb.mp4"  boy

"""video_annotator = FlamingoBalance_Score(
    video_path = "E:/manar/data_science/fixedinternship/CV/club_city_project/flamingo/f11_e.mp4"
)
fall_count = video_annotator.process()
print("fall_count: ",fall_count)"""

