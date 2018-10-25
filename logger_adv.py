#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import TransformStamped

class Logger():
    def __init__(self):
        rospy.loginfo("To stop logging CTRL + C")
        rospy.on_shutdown(self.shutdown)
        self.loop_rate = rospy.Rate(20)
        # rospy.loginfo("copying data")
        self.fo = open("Space_Platform_270418_2100.txt", "w")
        self.posedata = ''
        self.prevposedata = ''
        self.jointdata = ''
        self.prevjointdata = ''
        rospy.Subscriber("jointfeed", String, self.jointcallback)
        rospy.Subscriber("/vicon/SpaceMarker/SpaceMarker", TransformStamped, self.posecallback)

    def jointcallback(self, data):
        #rospy.loginfo(rospy.get_caller_id() + "I heard joint %s", data.data)
        self.jointdata = data.data

    def posecallback(self, data):
        #rospy.loginfo(rospy.get_caller_id() + "I heard pose %s", data.data)
        self.posedata = " "+ str(data.transform.translation.x)+" "+str(data.transform.translation.y)+" "+str(data.transform.translation.z)+" "+str(data.transform.rotation.x)+" "+str(data.transform.rotation.y)+" "+str(data.transform.rotation.z)+" "+str(data.transform.rotation.w)+" "

    def start(self):
        while not rospy.is_shutdown():
            data_string = str(rospy.get_time()) + " : " + self.posedata + " "  + self.jointdata +  "\n"
            self.fo.write(data_string)
            log_message = "Data logged at " + str(rospy.get_time())
            self.jointdata = ''
            self.posedata = ''
            rospy.loginfo(log_message)
            self.loop_rate.sleep()

    def shutdown(self):
        rospy.loginfo("Stop Logging")
        self.fo.close()
        rospy.sleep(1)


if __name__ == '__main__':
    rospy.init_node('logger', anonymous=True)
    log_node = Logger()
    log_node.start()
