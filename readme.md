# Simple model of SCARA cylindric robot

![](https://github.com/BorisAnimal/dynamics-labs/blob/master/media/scara-3d.png)

## Dependencies

Complete pack of ROS Melodic and some control staff:

```bash
sudo apt install ros-melodic-joint-state-publisher-gui ros-melodic-ros-control ros-melodic-ros-controllers
```
## How to run

#### Rviz 
```bash
roslaunch scara rviz.launch 
```
#### Control code
```bash
python scripts/control.py
```

## URDF tree structure
![](https://github.com/BorisAnimal/dynamics-labs/blob/master/media/urdf-tree.png)
