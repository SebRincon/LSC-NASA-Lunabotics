## Simulator Usage

#### Setup 
Run `catkin_make` under the catkin_ws
Run `source devel/setup.bash`

#### Run simulator

Run `roslaunch rover_sim gazebo.launch`
- This Starts up the gazebo simulator

Run `rostopic pub -r 1 /cmd_demo geometry_msgs/Twist  '{linear:  {x: 0.3, y: 0.0, z: 0.0}, angular: {x: 0.0,y: 0.0,z: 0.0}}'`
- This command will publish a `geometry_msgs/Twist` message to the topic `/cmd_demo` 
- The message has to be in json format : ` '{linear:  {x: 0.3, y: 0.0, z: 0.0}, angular: {x: 0.0,y: 0.0,z: 0.0}}' `
- The command will make the rover move at a velocity of 0.3 in the x direction

#### Stop Movement
Run `rostopic pub -r 1 /cmd_demo geometry_msgs/Twist  '{linear:  {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0,y: 0.0,z: 0.0}}'`