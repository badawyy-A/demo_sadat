

from .pose_model import process_video_pose_estimation

#Use a Savgol filter to smooth the data.
from scipy.signal import savgol_filter

# (Push-ups)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, find_peaks

# done
class PushupAnalyzer:
    def __init__(self, video_path, window_length=5, poly_order=3):
        
        try:
            self.df, self.FPS = process_video_pose_estimation(video_path)
            if self.df.empty:
                print("⚠️ Warning: The DataFrame is empty! Check process_video_pose_estimation.")
        except Exception as e:
            print(f"Error processing video: {e}")
        
        self.window_length = window_length
        self.poly_order = poly_order
        self.keypoints = [col for col in self.df.columns if col.startswith('kp_')]
        self.peaks = None
        self.valleys = None
        self.initialize_columns()

        self.reps = 0

    def initialize_columns(self):
        self.df['pushup_stage'] = 'In-Process'
        self.df['VA_Validation'] = "NF"
        self.df['pushup_duration'] = 0.0
        self.df['frames_count'] = 0.0
        self.df['pushup_speed'] = "NF"
        self.df['pushup_cycle_duration'] = 0.0
        self.df['pushup_cycle_speed'] = "NF"

    def apply_smoothing(self):
        for keypoint in self.keypoints:
            self.df[f"{keypoint}_smooth"] = savgol_filter(self.df[keypoint], window_length=self.window_length, polyorder=self.poly_order)

    @staticmethod
    def calculate_angle(a, b, c):
        a, b, c = np.array(a), np.array(b), np.array(c)
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        return 360 - angle if angle > 180 else angle

    def calculate_angles(self):
        self.df['elbow_angle'] = self.df.apply(lambda row: self.calculate_angle(
            [row['kp_x5_smooth'], row['kp_y5_smooth']],
            [row['kp_x7_smooth'], row['kp_y7_smooth']],
            [row['kp_x9_smooth'], row['kp_y9_smooth']]
        ), axis=1)
        
        self.df['hip_Alignment_angle'] = self.df.apply(lambda row: self.calculate_angle(
            [row['kp_x5_smooth'], row['kp_y5_smooth']],
            [row['kp_x11_smooth'], row['kp_y11_smooth']],
            [row['kp_x13_smooth'], row['kp_y13_smooth']]
        ), axis=1)

    def detect_up_down_positions(self):
        self.peaks, _ = find_peaks(self.df['elbow_angle'], prominence=7)
        self.valleys, _ = find_peaks(-self.df['elbow_angle'], prominence=20)
        
        frames_diff_peak_valley = self.peaks - self.valleys
        if  self.valleys[0] < self.peaks[0] and self.valleys[0] > (frames_diff_peak_valley.sum() / len(frames_diff_peak_valley)):
            self.peaks = np.insert(self.peaks, 0, 0)
        
        self.df.loc[self.peaks, 'pushup_stage'] = 'Up'
        self.df.loc[self.valleys, 'pushup_stage'] = 'Down'

    def plot(self):
        """Visualize detected peaks and valleys."""
        plt.figure(figsize=(10, 6))
        plt.plot(self.df['elbow_angle'], label='Elbow Angle')
        plt.plot(self.peaks, self.df['elbow_angle'][self.peaks], "x", markersize=10, label="Peaks")
        plt.plot(self.valleys, self.df['elbow_angle'][self.valleys], "o", markersize=10, label="Valleys")
        plt.xlabel("Frame")
        plt.ylabel("Angle (degrees)")
        plt.title("Peaks of Elbow Angle Over Time")
        plt.legend()
        plt.grid(True)
        plt.show()
        
        
    def check_performance(self, check_type):
        if check_type == "elbow":
            threshold_depth = (self.df['elbow_angle'].max() - self.df['elbow_angle'].min()) * 0.4
            max_valid_angle = self.df['elbow_angle'].max() - threshold_depth

            self.df["VA_Validation"] = self.df.apply(
                lambda row: "good depth" if row["pushup_stage"] == "Down" and row['elbow_angle'] <= max_valid_angle
                else "poor depth" if row["pushup_stage"] == "Down" else "NF",
                axis=1
            )
        elif check_type == 'hip':
            self.df['Core_feedback'] = self.df['hip_Alignment_angle'].apply(
                lambda x: 'Core engaged' if 160 <= x <= 180 else ('Core not engaged' if x < 160 else None)
            )

    def calculate_durations(self):
        prev_stage, start_frame = None, None
        durations, frames = [], []

        for i, row in self.df.iterrows():
            current_stage, frame = row['pushup_stage'], row['frame_idx']
            if current_stage == "In-Process":
                continue

            if prev_stage is None:
                prev_stage, start_frame = current_stage, frame
                continue

            if current_stage != prev_stage:
                frames_count = frame - start_frame
                duration = frames_count / self.FPS
                frames.append((i, frames_count))
                durations.append((i, duration))
                start_frame, prev_stage = frame, current_stage

        for i, duration in durations:
            self.df.at[i, 'pushup_duration'] = duration
            self.df.at[i, 'pushup_speed'] = "Too Slow" if duration > 2 else "Too Fast" if duration < 1 else "Optimal Speed"
        
        for i, frames_count in frames:
            self.df.at[i, 'frames_count'] = frames_count

    def pushup_cycle_speed(self):
        pushup_cycles, start_frame_idx, up_to_down_frames, prev_stage = [], None, None, None

        for i, row in self.df.iterrows():
            current_stage, frames_count, frame_idx = row['pushup_stage'], row['frames_count'], row['frame_idx']
            if current_stage == "In-Process":
                continue

            if prev_stage is None:
                prev_stage = current_stage
                continue

            if prev_stage == "Up" and current_stage == "Down":
                start_frame_idx = frame_idx
                up_to_down_frames = frames_count  # Store frames from Up to Down

            elif prev_stage == "Down" and current_stage == "Up" and start_frame_idx is not None:
                down_to_up_frames = frames_count  # Frames from Down to Up
                total_cycle_frames = up_to_down_frames + down_to_up_frames  # Sum both 
                cycle_duration = (total_cycle_frames * 2) / self.FPS
                pushup_cycles.append((i, cycle_duration))
                start_frame_idx = None

            prev_stage = current_stage

        for i, duration in pushup_cycles:
            self.df.at[i, 'pushup_cycle_duration'] = duration
            self.df.at[i, 'pushup_cycle_speed'] = "Too Slow" if duration > 4 else "Too Fast" if duration < 2 else "Optimal Speed"

    def process(self):
        self.apply_smoothing()
        self.calculate_angles()
        self.detect_up_down_positions()
        self.plot()
        self.check_performance("elbow")
        self.calculate_durations()
        self.check_performance("hip")
        self.pushup_cycle_speed()  
        self.reps = len(self.df[self.df['pushup_cycle_duration'] != 0])
        return self.reps 

# Usage
"""
video_path = "pushups/Mod_Push Ups.mp4"
pushup_analyzer = PushupAnalyzer(video_path)
reps, duration = pushup_analyzer.process()
print(reps, duration)
"""
# (Curl-ups)

# done
class CurlUpsTest:
    def __init__(self, video_path, FPS=30):

        try:
            self.df, self.FPS = process_video_pose_estimation(video_path)
            if self.df.empty:
                print("⚠️ Warning: The DataFrame is empty! Check process_video_pose_estimation.")
        except Exception as e:
            print(f"Error processing video: {e}")
        
        self.df['current_stage'] = 'In-Process'
        self.df['frames_count'] = 0.0
        self.df['duration'] = 0.0
        self.df['cycle_duration'] = 0.0
        self.peaks = None
        self.valleys = None

    @staticmethod
    def determine_closer_side(row, left_kp_x_col, right_kp_x_col):
        left_x = row[left_kp_x_col]
        right_x = row[right_kp_x_col]
        
        if pd.isna(left_x) or pd.isna(right_x):
            return "ambiguous"
        if left_x < right_x:
            return "right"
        elif right_x < left_x:
            return "left"
        else:
            return "ambiguous"

    def preprocess(self):
        self.df['closer_side'] = self.df.apply(
            self.determine_closer_side, axis=1, left_kp_x_col='kp_x3', right_kp_x_col='kp_x4'
        )
        
        keypoints = [col for col in self.df.columns if col.startswith('kp_')]
        for keypoint in keypoints:
            self.df[f"{keypoint}_smooth"] = savgol_filter(self.df[keypoint], window_length=5, polyorder=3)

    @staticmethod
    def calculate_angle(a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        if angle >180.0:
            angle = 360-angle
        return angle

    def calculate_angles(self):
        side = self.df['closer_side'].max()
        if side == "right":
            self.df['hip_Alignment_angle'] = self.df.apply(lambda row: self.calculate_angle(
                [row['kp_x5_smooth'], row['kp_y5_smooth']],
                [row['kp_x11_smooth'], row['kp_y11_smooth']],
                [row['kp_x13_smooth'], row['kp_y13_smooth']]
            ), axis=1)
        else:
            self.df['hip_Alignment_angle'] = self.df.apply(lambda row: self.calculate_angle(
                [row['kp_x6_smooth'], row['kp_y6_smooth']],
                [row['kp_x12_smooth'], row['kp_y12_smooth']],
                [row['kp_x14_smooth'], row['kp_y14_smooth']]
            ), axis=1)

    def detect_up_down_positions(self):
        self.peaks, _ = find_peaks(self.df['hip_Alignment_angle'], prominence=7)
        self.valleys, _ = find_peaks(-self.df['hip_Alignment_angle'], prominence=20)
        
        min_len = min(len(self.peaks), len(self.valleys))
        peaks_e, valleys_e = self.peaks[:min_len], self.valleys[:min_len]

        
        frames_diff_peak_valley = peaks_e - valleys_e
        
        if  self.valleys[0] < self.peaks[0] and self.valleys[0] >= (frames_diff_peak_valley.sum() / len(frames_diff_peak_valley)):
            self.peaks = np.insert(self.peaks, 0, 0)
        
        self.df.loc[self.peaks, 'current_stage'] = 'Down'
        self.df.loc[self.valleys, 'current_stage'] = 'Up'
        
    def plot(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.df['hip_Alignment_angle'], label='hip_Alignment_angle')
        plt.plot(self.peaks, self.df['hip_Alignment_angle'][self.peaks], "x", markersize=10, label="Peaks")
        plt.plot(self.valleys, self.df['hip_Alignment_angle'][self.valleys], "o", markersize=10, label="Valleys")
        plt.legend()
        plt.grid(True)
        plt.show()

    def duration_speed_comment(self):
        prev_stage, start_frame, durations, frames = None, None, [], []
        
        for i, row in self.df.iterrows():
            current_stage, frame = row['current_stage'], row['frame_idx']
            
            if current_stage == "In-Process":
                continue
            
            if prev_stage is None:
                prev_stage, start_frame = current_stage, frame
                continue
            
            if current_stage != prev_stage and (current_stage != "in-progress") and prev_stage != "in-progress":
                frames_count = frame - start_frame
                duration = frames_count / self.FPS
                frames.append((i, frames_count))
                durations.append((i, duration))
                
                start_frame = frame  # Reset start frame for new stage
                prev_stage = current_stage
        
        for i, frames_count in frames:
            self.df.at[i, 'frames_count'] = frames_count
        
        for i, duration in durations:
            self.df.at[i, 'duration'] = duration

    def pushup_cycle_speed(self):
        cycles, start_frame_idx, up_to_down_frames, prev_stage = [], None, None, None
        
        for i, row in self.df.iterrows():
            current_stage = row['current_stage']
            frames_count = row['frames_count']  # Frames between current and previous stage
            frame_idx = row['frame_idx']            
            
            if current_stage == "In-Process":
                continue
            
            if prev_stage is None:
                prev_stage = current_stage
                continue
            
            # Detect Up → Down transition (start of cycle)
            if prev_stage == "Down" and current_stage == "Up":
                start_frame_idx = frame_idx
                down_to_up_frames = frames_count  # Store frames from Up to Down

            # Detect Down → Up transition (end of cycle)
            elif prev_stage == "Up" and current_stage == "Down" and start_frame_idx is not None:
                up_to_down_frames = frames_count  # Frames from Down to Up
                total_cycle_frames = up_to_down_frames + down_to_up_frames  # Sum both transitions
                cycle_duration = total_cycle_frames / self.FPS
                cycles.append((i, cycle_duration))
                start_frame_idx = None

            prev_stage = current_stage
        
        for i, duration in cycles:
            self.df.at[i, 'cycle_duration'] = duration

    def process(self):
        self.preprocess()
        self.calculate_angles()
        self.detect_up_down_positions()
        self.plot()
        self.duration_speed_comment()
        self.pushup_cycle_speed()
        return len(self.df[self.df['cycle_duration'] != 0])

# Usage example:
"""video_path = "curl/curl_g.mp4"
curlups = CurlUpsTest(video_path)
reps, total_duration = curlups.process()
print(reps, total_duration)
"""

# speed test (distance & duration)

