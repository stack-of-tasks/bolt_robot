from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    arg_world_filename = PathJoinSubstitution(
        [FindPackageShare("gazebo_ros2_control_bolt"), "world", "bolt_world.world"]
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [PathJoinSubstitution([FindPackageShare("gazebo_ros"), "launch", "gazebo.launch.py"])]
        ),
        launch_arguments={
            "verbose": "false",
            "pause": "true",
            "world": arg_world_filename,
        }.items(),
    )

    # Get URDF via xacro
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [
                    FindPackageShare("ros2_description_bolt"),
                    "urdf",
                    "system_bolt_description.urdf.xacro",
                ]
            ),
            " use_sim:=true",
        ]
    )

    robot_description = {"robot_description": robot_description_content}

    node_robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[robot_description],
    )

    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=["-topic", "robot_description", "-entity", "bolt", "-x 0", "-y 0", "-z 1"],
        output="screen",
    )
    spawn_controller = Node(
        package="controller_manager",
        executable="spawner.py",
        arguments=["joint_state_broadcaster"],
        output="screen",
    )

    spawn_controller_p = Node(
        package="controller_manager",
        executable="spawner.py",
        arguments=["position_controller"],
        output="screen",
    )

    spawn_controller_v = Node(
        package="controller_manager",
        executable="spawner.py",
        arguments=["velocity_controller"],
        output="screen",
    )

    spawn_controller_e = Node(
        package="controller_manager",
        executable="spawner.py",
        arguments=["effort_controller"],
        output="screen",
    )

    spawn_controller_kp = Node(
        package="controller_manager",
        executable="spawner.py",
        arguments=["kp_controller"],
        output="screen",
    )

    spawn_controller_kd = Node(
        package="controller_manager",
        executable="spawner.py",
        arguments=["kd_controller"],
        output="screen",
    )



    return LaunchDescription(
        [
            gazebo,
            node_robot_state_publisher,
            spawn_entity,
            spawn_controller,
            # spawn_controller_pveg,
            spawn_controller_p
            spawn_controller_v 
            spawn_controller_e 
            spawn_controller_kp 
            spawn_controller_kd 
        ]
    )
