import pandas as pd
import cv2
from ultralytics import YOLO

#done
def estimate_foot_position(ankle_x, ankle_y, knee_y):
    """
    Estimate the position of the two feet
    kp17 -> right foot
    kp18 -> left foot
    """
    if ankle_x is None and ankle_y is None or knee_y is None:
        return None, None

    leg_length = abs(knee_y - ankle_y)
    offset = int(leg_length * 0.3)
    foot_y = ankle_y + offset
    foot_x = ankle_x

    return foot_x, foot_y

# done
def create_pose_dataframe(results, frame_idx=0):
    """
    Creates a Pandas DataFrame from YOLOv8 pose estimation tracking results.

    Args:
        results: Output from YOLOv8 pose estimation model's track function.
                 Assumes it's a list of objects where each object contains
                 detection information (boxes, keypoints, track_id).
        frame_idx (int, optional): Frame index. Defaults to 0.

    Returns:
        pandas.DataFrame: DataFrame containing frame index, person ID,
                          bounding box, and keypoint coordinates.
    """

    frame_indices = []
    x1_list = []
    y1_list = []
    x2_list = []
    y2_list = []
    kp_x_lists = [[] for _ in range(17)]
    kp_y_lists = [[] for _ in range(17)]
    kp_x17_list, kp_y17_list = [], []  # Right Foot
    kp_x18_list, kp_y18_list = [], []  # Left Foot

    if results and results.boxes:
        for res in results:
            if res.boxes and res.keypoints and res.boxes.cls[0] == 0: #cls[0]--> class id 0 for person detection
                box = res.boxes.xyxy[0]
                keypoints = res.keypoints.xy[0]
                track_id = res.boxes.id.cpu().numpy()[0] if res.boxes.id is not None else -1

                frame_indices.append(frame_idx)
                x1_list.append(box[0].item())
                y1_list.append(box[1].item())
                x2_list.append(box[2].item())
                y2_list.append(box[3].item())

                for i in range(17):
                    kp_x_lists[i].append(keypoints[i][0].item())
                    kp_y_lists[i].append(keypoints[i][1].item())

                # Estimate right foot (Keypoints 15=Right Ankle, 13=Right Knee)
                foot_x17, foot_y17 = estimate_foot_position(keypoints[16][0].item(), keypoints[16][1].item(), keypoints[14][1].item())
                kp_x17_list.append(foot_x17)
                kp_y17_list.append(foot_y17)

                # Estimate left foot (Keypoints 16=Left Ankle, 14=Left Knee)
                foot_x18, foot_y18 = estimate_foot_position(keypoints[15][0].item(), keypoints[15][1].item(), keypoints[13][1].item())
                kp_x18_list.append(foot_x18)
                kp_y18_list.append(foot_y18)

    else:
        print(f"No person detected in frame{frame_idx} or empty results.")
        return pd.DataFrame()
    
    data = {
        "frame_idx": frame_indices,
        "x1": x1_list,
        "y1": y1_list,
        "x2": x2_list,
        "y2": y2_list,
    }

    for i in range(17):
        data[f"kp_x{i}"] = kp_x_lists[i]
        data[f"kp_y{i}"] = kp_y_lists[i]

    # Add estimated foot positions
    data["kp_x17"] = kp_x17_list
    data["kp_y17"] = kp_y17_list
    data["kp_x18"] = kp_x18_list
    data["kp_y18"] = kp_y18_list

    df = pd.DataFrame(data)
    return df


# done
def process_video_pose_estimation(video_path, model_path="yolo11x-pose.pt"):
    """
    Processes a video to perform pose estimation and tracking, and saves/returns results as a Pandas DataFrame.

    Args:
        video_path (str): Path to the input video file.
        output_csv_path (str, optional): Path to save the output CSV file. Defaults to "pose_results.csv".

    Returns:
        pandas.DataFrame: DataFrame containing pose estimation results for the video.
    """
    model = YOLO(model_path)
    
    
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise IOError("Error: Cannot open video file.")
    except IOError as e:
        print(e)
        return pd.DataFrame() # Return empty DataFrame in case of error
    
    
    if not cap.isOpened():
        print("Error: Cannot open video file.")
        return pd.DataFrame()

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    frame_index = 0
    all_frames_df = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        try:
            results = model.track(frame, conf=0.1, iou = 0 , persist=True, classes=[0], verbose=True, pose=True)
        except Exception as e:
            print(f"Error processing frame {frame_index}: {e}")
            continue

        df_current_frame = create_pose_dataframe(results[0], frame_index)

        if not df_current_frame.empty:
            all_frames_df.append(df_current_frame)

        frame_index += 1

    cap.release()
    cv2.destroyAllWindows()

    if all_frames_df:
        final_df = pd.concat(all_frames_df, ignore_index=True)
        return final_df, fps
    else:
        print("No pose data extracted from the video.")
        return pd.DataFrame(), fps

      # <--- REPLACE THIS WITH DESIRED OUTPUT CSV PATH

# video_file = "test_videos/run.mp4"  # <--- REPLACE THIS WITH YOUR VIDEO PATH

# pose_df, FPS = process_video_pose_estimation(video_file)

# print(pose_df.info())
# print(pose_df.columns)




