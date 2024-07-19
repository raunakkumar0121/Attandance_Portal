import streamlit as st
import csv
from datetime import datetime
import cv2
from PIL import Image
import numpy as np
import os

# Function to mark attendance and save to CSV
def mark_attendance(enrollment_number, first_name, last_name):
    # Append attendance record to CSV file
    with open('attendance_records.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([enrollment_number, first_name, last_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    st.success(f"Attendance marked for {first_name} {last_name} (Enrollment: {enrollment_number})")

    # Option to capture image from webcam
    st.header("Capture Image from Webcam")
    
    # Initialize webcam capture
    cap = cv2.VideoCapture(0)
    
    if st.button("Capture Image", key='capture_button'):
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # Convert frame from BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Convert to PIL Image
                pil_image = Image.fromarray(frame_rgb)
                
                # Display captured image
                st.image(pil_image, caption='Captured Image', use_column_width=True)
                
                # Save image to disk (optional)
                image_path = f"captured_image_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
                pil_image.save(image_path)
                
                st.success(f"Image captured and saved as {image_path}")
                
                # Option to delete or modify the captured image
                delete_option = st.checkbox("Delete Image")
                modify_option = st.checkbox("Modify Image")
                
                if delete_option:
                    os.remove(image_path)
                    st.warning("Image deleted.")
                
                if modify_option:
                    # Provide options to modify the image (example: rotate, resize, etc.)
                    rotation_angle = st.slider("Rotation Angle", -180, 180, 0)
                    if st.button("Apply Rotation"):
                        modified_image = pil_image.rotate(rotation_angle)
                        st.image(modified_image, caption='Modified Image', use_column_width=True)
                        modified_image.save(image_path)  # Save modified image

    # Release the webcam
    cap.release()

# Function to capture image from webcam and save
def capture_image():
    st.header("Capture Image from Webcam")
    
    # Initialize webcam capture
    cap = cv2.VideoCapture(0)
    
    if st.button("Capture Image", key='capture_button'):
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # Convert frame from BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Convert to PIL Image
                pil_image = Image.fromarray(frame_rgb)
                
                # Display captured image
                st.image(pil_image, caption='Captured Image', use_column_width=True)
                
                # Save image to disk (optional)
                image_path = f"captured_image_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
                pil_image.save(image_path)
                
                st.success(f"Image captured and saved as {image_path}")
                
                # Option to delete or modify the captured image
                delete_option = st.checkbox("Delete Image")
                modify_option = st.checkbox("Modify Image")
                
                if delete_option:
                    os.remove(image_path)
                    st.warning("Image deleted.")
                
                if modify_option:
                    # Provide options to modify the image (example: rotate, resize, etc.)
                    rotation_angle = st.slider("Rotation Angle", -180, 180, 0)
                    if st.button("Apply Rotation"):
                        modified_image = pil_image.rotate(rotation_angle)
                        st.image(modified_image, caption='Modified Image', use_column_width=True)
                        modified_image.save(image_path)  # Save modified image

    # Release the webcam
    cap.release()

# Function to view attendance records from CSV
def view_attendance():
    try:
        with open('attendance_records.csv', 'r') as file:
            reader = csv.reader(file)
            attendance_records = list(reader)
            
        # Display attendance records in a table
        st.write("### Attendance Records")
        if attendance_records:
            # Format data for table display
            formatted_records = []
            for record in attendance_records:
                formatted_record = {
                    "Enrollment Number": record[0],
                    "First Name": record[1],
                    "Last Name": record[2],
                    "Date & Time": record[3]
                }
                formatted_records.append(formatted_record)
            
            # Display as a table
            st.table(formatted_records)
            
            # Modify attendance option
            modify_option = st.selectbox("Select an option", ["", "Edit Attendance", "Delete Attendance"])
            if modify_option == "Edit Attendance":
                edit_index = st.number_input("Enter the index of the record to edit", min_value=1, max_value=len(attendance_records))
                if st.button("Edit"):
                    edit_record = attendance_records[edit_index - 1]
                    st.write(f"Editing record: {edit_record}")
                    # Provide fields to edit (if needed)
                    # Example: You can update the attendance data structure based on requirements
            elif modify_option == "Delete Attendance":
                delete_index = st.number_input("Enter the index of the record to delete", min_value=1, max_value=len(attendance_records))
                if st.button("Delete"):
                    deleted_record = attendance_records.pop(delete_index - 1)
                    # Rewrite the CSV file without the deleted record
                    with open('attendance_records.csv', 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerows(attendance_records)
                    st.warning(f"Deleted record: {deleted_record}")
                    st.success("Attendance record deleted successfully.")

        else:
            st.write("No attendance records found.")
    
    except FileNotFoundError:
        st.write("No attendance records found.")

# Streamlit UI code
def main():
    st.set_page_config(page_title="Amity University Attendance Portal", page_icon=":bar_chart:", layout='wide')

    st.title("Amity University Attendance Portal")
    st.sidebar.header("Navigation")
    menu = ["Mark Attendance", "View Attendance", "Capture Image"]
    choice = st.sidebar.selectbox("Menu", menu)

    st.sidebar.markdown("---")

    if choice == "Mark Attendance":
        st.header("Mark Attendance")
        st.info("Enter student details to mark attendance.")
        enrollment_number = st.text_input("Enter Enrollment Number")
        first_name = st.text_input("Enter First Name")
        last_name = st.text_input("Enter Last Name")
        if st.button("Mark Attendance"):
            mark_attendance(enrollment_number, first_name, last_name)
    
    elif choice == "View Attendance":
        st.header("View Attendance")
        view_attendance()
    
    elif choice == "Capture Image":
        capture_image()

if __name__ == '__main__':
    main()

