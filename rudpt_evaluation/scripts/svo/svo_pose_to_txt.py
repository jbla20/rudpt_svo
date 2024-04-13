import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped

def topic_to_txt(pose_topic, output_file):
    
    rospy.loginfo(f"Recording messages from topic {pose_topic} to {output_file}")
    rospy.loginfo("When recording is done, clean exit node by pressing ctrl + c")

    msgs_recv = 0 # Counter

    # Open csv-file (throw exception if it exists)
    with open(output_file, 'w') as txt_file:

        txt_file.write("# timestamp tx ty tz qx qy qz qw\n")
        
        def callback_pose(data : PoseWithCovarianceStamped):
            x = data.pose.pose.position.x
            y = data.pose.pose.position.y
            z = data.pose.pose.position.z
            qx = data.pose.pose.orientation.x
            qy = data.pose.pose.orientation.y
            qz = data.pose.pose.orientation.z
            qw = data.pose.pose.orientation.w
            timestamp = data.header.stamp.to_time()
            
            txt_file.write(f"{timestamp} {x} {y} {z} {qx} {qy} {qz} {qw}\n")

            nonlocal msgs_recv
            msgs_recv += 1
            
            rospy.logdebug(f"Received {msgs_recv} msgs")
            #print(f"Stored {msgs_recv} msgs", end='\r')

        # Specify subscribers
        rospy.Subscriber(pose_topic, PoseWithCovarianceStamped, callback_pose, queue_size=500)
        
        # spin() simply keeps python from exiting until this node is stopped
        rospy.spin()


def main():
    rospy.init_node('svo_to_txt')
    
    pose_topic = rospy.get_param("/svo_to_txt/pose_topic")
    output_file = rospy.get_param("/svo_to_txt/output_file")
    
    topic_to_txt(pose_topic, output_file)


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
    
    # pose_topic = "/svo/pose_imu" # Pose of imu for camera 0 (left cam). Message type is assumed to be geometry_msgs/PoseStamped
    # output_name = "2,1_2_2_1_eval_4.txt" # Name of .txt file to be created (with extension).
    # output_folder = "Data-collection/txt_data/RUD-PT" # Output folder to store csv-file

    # # topic_to_csv writes any messages received on the pose_topic into the csv. 
    # # OBS: If csv_name exists in folder, it will overwrite its contents 
    # topic_to_txt(pose_topic, output_name, output_folder)
