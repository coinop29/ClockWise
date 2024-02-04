# # from flask import Flask, render_template, Response
# # from flask_socketio import SocketIO, emit
# # import face_recognition
# # import cv2
# # import pandas as pd
# # import numpy as np
# # import os
# # import datetime
# #
# # app = Flask(__name__)
# # socketio = SocketIO(app)
# #
# # video = cv2.VideoCapture(0)  # Initialize your video capture device
# #
# # csv_file = 'known_faces.csv'
# # df = pd.read_csv(csv_file) if os.path.exists(csv_file) else pd.DataFrame(
# #     columns=['username', 'face_encoding', 'last_seen'])
# #
# #
# # def save_known_faces():
# #     df.to_csv(csv_file, index=False)
# #
# #
# # def gen_frame():
# #     global df
# #     update_threshold = datetime.timedelta(seconds=30)  # Update last seen time only if the last update was longer ago than this threshold
# #
# #     while True:
# #         _, frame = video.read()
# #         face_locations = face_recognition.face_locations(frame)
# #         face_encodings = face_recognition.face_encodings(frame, face_locations)
# #
# #         for face_encoding, face_location in zip(face_encodings, face_locations):
# #             if not df.empty:
# #                 face_encodings_as_arrays = [np.array(eval(encoding)) for encoding in df['face_encoding'].tolist()]
# #                 distances = face_recognition.face_distance(face_encodings_as_arrays, face_encoding)
# #                 best_match_index = np.argmin(distances) if len(distances) > 0 else None
# #
# #                 if best_match_index is not None and distances[best_match_index] <= 0.6:
# #                     username = df.at[best_match_index, 'username']
# #                     last_seen_time = datetime.datetime.strptime(df.at[best_match_index, 'last_seen'], '%Y-%m-%d %H:%M:%S')
# #                     current_time = datetime.datetime.now()
# #
# #                     time_difference = current_time - last_seen_time
# #
# #                     if time_difference > update_threshold:
# #                         df.at[best_match_index, 'last_seen'] = current_time.strftime('%Y-%m-%d %H:%M:%S')
# #
# #                     top, right, bottom, left = face_location
# #                     cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
# #                     font = cv2.FONT_HERSHEY_DUPLEX
# #                     cv2.putText(frame, f'last seen: {last_seen_time.strftime("%Y-%m-%d %H:%M:%S")}',
# #                                 (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
# #
# #                     socketio.emit('last_seen_update', {
# #                         'username': username,
# #                         'last_seen': last_seen_time.strftime('%Y-%m-%d %H:%M:%S')
# #                     })
# #                 else:
# #                     # New face
# #                     new_face_id = f"face_{len(df) + 1}"
# #                     current_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# #                     new_row = pd.DataFrame({'username': [new_face_id], 'face_encoding': [str(face_encoding.tolist())],
# #                                             'last_seen': [current_time_str]})
# #                     df = pd.concat([df, new_row], ignore_index=True)
# #                     socketio.emit('last_seen_update', {
# #                         'username': new_face_id,
# #                         'last_seen': current_time_str
# #                     })
# #
# #                 save_known_faces()
# #             else:
# #                 # First face
# #                 new_face_id = f"face_1"
# #                 current_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# #                 df = pd.DataFrame({'username': [new_face_id], 'face_encoding': [str(face_encoding.tolist())],
# #                                    'last_seen': [current_time_str]})
# #                 socketio.emit('last_seen_update', {
# #                     'username': new_face_id,
# #                     'last_seen': current_time_str
# #                 })
# #
# #         ret, buffer = cv2.imencode('.jpg', frame)
# #         frame = buffer.tobytes()
# #         yield (b'--frame\r\n'
# #                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
# #
# #
# # @app.route('/video_feed')
# # def video_feed():
# #     return Response(gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')
# #
# #
# # @app.route('/')
# # def index():
# #     return render_template('index.html')
# #
# #
# # if __name__ == '__main__':
# #     socketio.run(app, debug=True)
# from flask import Flask, render_template, Response
# from flask_socketio import SocketIO, emit
# import face_recognition
# import cv2
# import pandas as pd
# import numpy as np
# import os
# import datetime
#
# app = Flask(__name__)
# socketio = SocketIO(app)
#
# video = cv2.VideoCapture(0)  # Initialize your video capture device
#
# csv_file = 'known_faces.csv'
# df = pd.read_csv(csv_file) if os.path.exists(csv_file) else pd.DataFrame(
#     columns=['username', 'face_encoding', 'last_seen'])
#
# def save_known_faces():
#     print("called")
#     df.to_csv(csv_file, index=False)
#
# def gen_frame():
#     global df
#     visible_faces = set()  # Set to keep track of faces that are currently visible
#
#     while True:
#         _, frame = video.read()
#         face_locations = face_recognition.face_locations(frame)
#         face_encodings = face_recognition.face_encodings(frame, face_locations)
#         current_visible_faces = set()  # Set to keep track of faces visible in the current frame
#
#         for face_encoding, face_location in zip(face_encodings, face_locations):
#             if not df.empty:
#                 face_encodings_as_arrays = [np.array(eval(encoding)) for encoding in df['face_encoding'].tolist()]
#                 distances = face_recognition.face_distance(face_encodings_as_arrays, face_encoding)
#                 best_match_index = np.argmin(distances) if len(distances) > 0 else None
#
#                 if best_match_index is not None and distances[best_match_index] <= 0.6:
#                     username = df.at[best_match_index, 'username']
#                     current_visible_faces.add(username)  # Add to current visible faces
#
#                     if username not in visible_faces:
#                         visible_faces.add(username)  # Add to visible faces
#
#                     top, right, bottom, left = face_location
#                     cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
#                     font = cv2.FONT_HERSHEY_DUPLEX
#                     cv2.putText(frame, f'username: {username}', (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
#                 else:
#                     # New face logic...
#                     new_face_id = f"face_{len(df) + 1}"
#                     current_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#                     new_row = pd.DataFrame({'username': [new_face_id], 'face_encoding': [str(face_encoding.tolist())],
#                                             'last_seen': [current_time_str]})
#                     df = pd.concat([df, new_row], ignore_index=True)
#                     socketio.emit('last_seen_update', {
#                         'username': new_face_id,
#                         'last_seen': current_time_str
#                     })
#             else:
#                 # First face logic...
#                 new_face_id = f"face_1"
#                 current_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#                 df = pd.DataFrame({'username': [new_face_id], 'face_encoding': [str(face_encoding.tolist())],
#                                    'last_seen': [current_time_str]})
#                 socketio.emit('last_seen_update', {
#                     'username': new_face_id,
#                     'last_seen': current_time_str
#                 })
#
#         # Update last_seen for faces that have left the camera's view
#         faces_no_longer_visible = visible_faces - current_visible_faces
#         for username in faces_no_longer_visible:
#             best_match_index = df[df['username'] == username].index[0]
#             current_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             df.at[best_match_index, 'last_seen'] = current_time_str
#
#             socketio.emit('last_seen_update', {
#                 'username': username,
#                 'last_seen': current_time_str
#             })
#
#         visible_faces = current_visible_faces  # Update the visible faces set for the next frame
#
#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#
#     save_known_faces()  # Save the known faces information
#
# @app.route('/video_feed')
# def video_feed():
#     return Response(gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
# if __name__ == '__main__':
#     socketio.run(app, debug=True)
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
import face_recognition
import cv2
import pandas as pd
import numpy as np
import os
import datetime

app = Flask(__name__)
socketio = SocketIO(app)

video = cv2.VideoCapture(0)  # Initialize your video capture device

csv_file = 'known_faces.csv'
df = pd.read_csv(csv_file) if os.path.exists(csv_file) else pd.DataFrame(
    columns=['username', 'face_encoding', 'last_seen'])

def save_known_faces():
    df.to_csv(csv_file, index=False)

def gen_frame():
    global df
    visible_faces = set()  # Set to keep track of faces that are currently visible

    while True:
        _, frame = video.read()
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        current_visible_faces = set()  # Set to keep track of faces visible in the current frame

        for face_encoding, face_location in zip(face_encodings, face_locations):
            if not df.empty:
                face_encodings_as_arrays = [np.array(eval(encoding)) for encoding in df['face_encoding'].tolist()]
                distances = face_recognition.face_distance(face_encodings_as_arrays, face_encoding)
                best_match_index = np.argmin(distances) if len(distances) > 0 else None

                if best_match_index is not None and distances[best_match_index] <= 0.6:
                    username = df.at[best_match_index, 'username']
                    current_visible_faces.add(username)  # Add to current visible faces

                    if username not in visible_faces:
                        visible_faces.add(username)  # Add to visible faces

                    top, right, bottom, left = face_location
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, f'username: {username}', (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
                else:
                    # New face logic...
                    new_face_id = f"face_{len(df) + 1}"
                    current_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    new_row = pd.DataFrame({'username': [new_face_id], 'face_encoding': [str(face_encoding.tolist())],
                                            'last_seen': [current_time_str]})
                    df = pd.concat([df, new_row], ignore_index=True)
                    save_known_faces()  # Save after adding a new face
                    socketio.emit('last_seen_update', {
                        'username': new_face_id,
                        'last_seen': current_time_str
                    })
            else:
                # First face logic...
                new_face_id = f"face_1"
                current_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                df = pd.DataFrame({'username': [new_face_id], 'face_encoding': [str(face_encoding.tolist())],
                                   'last_seen': [current_time_str]})
                save_known_faces()  # Save after adding the first face
                socketio.emit('last_seen_update', {
                    'username': new_face_id,
                    'last_seen': current_time_str
                })

        # Update last_seen for faces that have left the camera's view
        faces_no_longer_visible = visible_faces - current_visible_faces
        if faces_no_longer_visible:
            for username in faces_no_longer_visible:
                best_match_index = df[df['username'] == username].index[0]
                current_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                df.at[best_match_index, 'last_seen'] = current_time_str

                socketio.emit('last_seen_update', {
                    'username': username,
                    'last_seen': current_time_str
                })
            save_known_faces()  # Save after updating last_seen

        visible_faces = current_visible_faces  # Update the visible faces set for the next frame

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
