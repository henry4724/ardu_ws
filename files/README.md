# Bird-Scare

# ROS2 Source command
source /opt/ros/humble/setup.bash

# ROS2 And Ardupilot SITL
source /opt/ros/humble/setup.bash
cd ~/ardu_ws/
colcon build --packages-up-to ardupilot_sitl
source install/setup.bash
ros2 launch ardupilot_sitl sitl_dds_udp.launch.py transport:=udp4 synthetic_clock:=True wipe:=False model:=quad speedup:=1 slave:=0 instance:=0 defaults:=$(ros2 pkg prefix ardupilot_sitl)/share/ardupilot_sitl/config/default_params/copter.parm,$(ros2 pkg prefix ardupilot_sitl)/share/ardupilot_sitl/config/default_params/dds_udp.parm sim_address:=127.0.0.1 master:=tcp:127.0.0.1:5760 sitl:=127.0.0.1:5501

# Usefull MAVProxy Commands
mode guided
arm throttle
takeoff 40

# BashRC Files
nano ~/.bashrc

# Gazebo SITL Wild Thumper
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:\
$HOME/Documents/SITL_Models/Gazebo/models:\
$HOME/Documents/SITL_Models/Gazebo/worlds

gz sim -v4 -r wildthumper_runway.sdf

sim_vehicle.py -v Rover -f rover-skid --model JSON  --console --map


# Gazebo SITL with Rover 
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:\
$HOME/Documents/Bird-Scare/rover_sim/model:\
$HOME/Documents/Bird-Scare/rover_sim/world

cd Documents/Bird-Scare
gz sim rover_sim/world/rover_runway.sdf -r

sim_vehicle.py -v Rover -f rover-skid --model JSON --map --console -l "-38.70198362535839,177.90832136419021,0,0" --add-param-file=/home/henry/Documents/params.txt -w


# MavProxy Commands
mavproxy.py --console --map --aircraft test --master=:14550 
param set ARMING_MAGTHRESH 1000 
wp load /home/henry/Documents/testmission.waypoints
param set SERVO1_FUNCTION 0
param show SERVO1_FUNCTION
servo set 1 1500


# Gazebo ROS2 Examples
cd ~/ardu_ws
source ./install/setup.bash
colcon build --packages-up-to ardupilot_ros ardupilot_gz_bringup

source ~/ardu_ws/install/setup.sh
ros2 launch ardupilot_gz_bringup iris_maze.launch.py

source ~/ardu_ws/install/setup.sh
ros2 launch ardupilot_gz_bringup wildthumper_playpen.launch.py

source ~/ardu_ws/install/setup.sh
ros2 launch ardupilot_gz_bringup rover_vineyard.launch.py

mavproxy.py --console --map --aircraft test --master=:14550


chassis_link:
front_right_wheel_link:
front_left_wheel_link:
back_right_wheel_link:
back_left_wheel_link:
RPLiDar_link:
imu_link:


# NAV2 
ros2 topic pub /goal_pose geometry_msgs/PoseStamped "{
  header: {
    frame_id: 'map'
  },
  pose: {
    position: {
      x: 1.0,
      y: 2.0,
      z: 0.0
    },
    orientation: {
      x: 0.0,
      y: 0.0,
      z: 0.0,
      w: 1.0
    }
  }
}"


